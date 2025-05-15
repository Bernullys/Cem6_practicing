



---------------------------------------------------------------------------------------------------------------------
🔁 Step-by-step flow: How a JWT token is created in your auth.py
✅ 1. Frontend sends login credentials to /token
The frontend submits a POST request to:

POST /token
Content-Type: application/x-www-form-urlencoded

username=Bernardo&password=0123456789
Because you're using OAuth2PasswordRequestForm, FastAPI will automatically parse this form and give you:

form_data.username
form_data.password

🔐 2. login_for_access_token is called
This function handles the login:

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])
It calls:

user = authenticate_user(form_data.username, form_data.password)
🔍 3. authenticate_user checks credentials
Your function:

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

access_token = create_access_token(
    data={"sub": user.username}, 
    expires_delta=timedelta(minutes=30)
)
This calls:

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

return Token(access_token=access_token, token_type="bearer")
This returns:

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
The frontend stores this token (e.g., in localStorage) and uses it in headers like:

Authorization: Bearer <access_token>
⚠️ Important Fix
You have this right now:

SECRET_KEY = ""
You must set a secure secret key:

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
---------------------------------------------------------------------------------------------------------------------

Steps to create protected routes in the frontend/backend:

🛡️ STEP 1: Protect Routes in Your FastAPI Backend
Use Depends(get_current_user) to protect any route you want to make accessible only to authenticated users.

@router.get("/protected-data/")
async def get_protected_data(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"message": f"Hello {current_user['username']}, this is protected data!"}

This route can now only be accessed with a valid token.
get_current_user will decode the token, verify it, and return the user data.
If the token is invalid or missing, FastAPI will raise a 401 Unauthorized error.

🌐 STEP 2: Send the Token from the Frontend
When the user logs in, you receive the token. Save it to local storage (or memory):

// After login
localStorage.setItem("token", data.access_token)
🔐 STEP 3: Use the Token in Protected Requests
When making requests to protected routes from the frontend, include the token in the Authorization header:

const token = localStorage.getItem("token");
const response = await fetch("http://127.0.0.1:8000/protected-data/", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    }
});

🎯 STEP 4: Control the UI Based on Auth State
In your React app, manage a user or isAuthenticated state. Example:

const token = localStorage.getItem("token");
useEffect(() => {
    if (token) {
        setIsAuthenticated(true);
    } else {
        setIsAuthenticated(false);
    }
}, []);

You can then conditionally show parts of the UI based on that state:

{isAuthenticated ? <AppContent /> : <LoginOrRegister />}

🧹 BONUS: Logout Function

const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
};

Help Notes:

When you've already defined parameters (like room_id: int, data: RoomCreate, etc.), you can still add Depends(get_current_user) as an extra parameter. Just follow Python's rule: dependencies come after normal parameters.

✅ How to Modify Existing Functions
Suppose you have a function like this:

@router.post("/rooms/")
def create_room(room: RoomCreate):
    return save_room_to_db(room)

To protect it, add the user dependency as a new parameter:

@router.post("/rooms/")
def create_room(
    room: RoomCreate,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return save_room_to_db(room)
Or if you prefer not to use Annotated, this works too:

@router.post("/rooms/")
def create_room(
    room: RoomCreate,
    current_user=Depends(get_current_user)
):
    ...

✅ Another Example with Path and Body

@router.put("/devices/{device_id}")
def update_device(device_id: int, device_data: DeviceUpdate):
    ...
Make it:

@router.put("/devices/{device_id}")
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    ...

Summary
✔️ Leave your original parameters as-is.

➕ Just add current_user: Annotated[...] or current_user=Depends(...) as an extra argument.

📦 FastAPI will handle it for you behind the scenes — and reject requests with missing/invalid tokens.