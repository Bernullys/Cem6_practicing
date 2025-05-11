



---------------------------------------------------------------------------------------------------------------------------------------------
🔁 Step-by-step flow: How a JWT token is created in your auth.py
✅ 1. Frontend sends login credentials to /token
The frontend submits a POST request to:

bash
Copiar
Editar
POST /token
Content-Type: application/x-www-form-urlencoded

username=Bernardo&password=0123456789
Because you're using OAuth2PasswordRequestForm, FastAPI will automatically parse this form and give you:

python
Copiar
Editar
form_data.username
form_data.password
🔐 2. login_for_access_token is called
This function handles the login:

python
Copiar
Editar
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])
It calls:

python
Copiar
Editar
user = authenticate_user(form_data.username, form_data.password)
🔍 3. authenticate_user checks credentials
Your function:

python
Copiar
Editar
def authenticate_user(username: str, password: str):
    if get_all_app_users(username) == False:
        return False
    user = get_user(username)
    if not verify_password(password, user[3]):
        return False
    return user
🔹 get_user(username) retrieves user data (e.g., from SQLite).
🔹 user[3] is the hashed password in the database.
🔹 verify_password() compares the hashed and plain password using passlib.

✅ If successful, it returns the user (a list or dict with user fields).

🔏 4. JWT token is created
If authenticate_user returns a user:

python
Copiar
Editar
access_token = create_access_token(
    data={"sub": user.username}, 
    expires_delta=timedelta(minutes=30)
)
This calls:

python
Copiar
Editar
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
What this does:

Claim	Value
sub	user.username
exp	Expiration time (now + 30 mins)

🔑 It uses your SECRET_KEY to sign the token using HS256.

📦 5. JWT is returned to the client
Back in login_for_access_token:

python
Copiar
Editar
return Token(access_token=access_token, token_type="bearer")
This returns:

json
Copiar
Editar
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
The frontend stores this token (e.g., in localStorage) and uses it in headers like:

makefile
Copiar
Editar
Authorization: Bearer <access_token>
⚠️ Important Fix
You have this right now:

python
Copiar
Editar
SECRET_KEY = ""
You must set a secure secret key:

python
Copiar
Editar
SECRET_KEY = "super_secret_key_123"  # Example — store securely in real apps!
If this is empty, the token will be invalid and decoding will always fail.

✅ Summary
Here’s the token creation flow in plain terms:

User submits login form to /token.

FastAPI checks if the user exists and password is correct.

If valid, it encodes a JWT with sub=username and an expiration.

It signs the token with your secret key.

Token is returned to the frontend.

Frontend includes this token in future API requests.
------------------------------------------------------------------------------------------------------------------------------------------------