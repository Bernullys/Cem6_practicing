from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta, timezone
from typing import Annotated
from database_helpers import add_app_user_to_db, get_all_app_users, get_user

'''
Responsibilities of auth.py:
Hashing passwords securely using passlib.
Registering users (/register).
Logging in with credentials (/token endpoint).
Generating JWT tokens for secure session management.
Verifying tokens to protect private routes.
'''

# jwt token settings:
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Utility function to hash passwords:
def hash_password(plain_password):
    return pwd_context.hash(plain_password)

# Utility function to verify passwords:
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to authenticate users:
def authenticate_user(username: str, password: str):
    if get_all_app_users(username) == False:
        return False
    user = get_user(username)
    if not verify_password(password, user["password"]):
        return False
    return user # user is a dictionary with user data

# Pydantic BaseModel for app users:
class AppUserCreate(BaseModel):
    full_name: str = Field(..., max_length=50, min_length=3, description="Full name of the app user", example="Bernardo Dávila")
    email: EmailStr = Field(..., max_length=50, description="Email of the user", example="bernardoantoniod@gmail.com")
    username: str = Field(..., max_length=50, min_length=3, description="user name", example="Bernardo")
    password: str = Field(..., max_length=20, min_length=6, description="secret_password", example="0123456789")
    role: str = Field(..., max_length=50, description="Role of the user", example="admin")

# Pydantic BaseModel for the response message
class Message(BaseModel):
    message: str

# Pydantic BaseModel for the token response:
class Token(BaseModel):
    access_token: str
    token_type: str

# Pydantic BaseModel for the token data:
class TokenData(BaseModel):
    username: str | None = None

# instance of APIRouter to create endpoints here and then import them to main.py:
router = APIRouter()

# Password hashing context:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

# Function to create JWT token:
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# function to return the current user from the token:
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Register endpoint to create a new app user:
@router.post("/register/", response_model = Message)
def register_user(app_user: AppUserCreate):
    existing_app_users = get_all_app_users(app_user.username)
    if existing_app_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(app_user.password)
    
    app_user.password = hashed_password
    return add_app_user_to_db(app_user)

# Path function to create a new access token:
@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")