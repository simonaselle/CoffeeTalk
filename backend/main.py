from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #can call this server from any other website 
from pydantic import BaseModel
import bcrypt

app = FastAPI()

# Allow all origins to access the server (frontend -> backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# File to store the data (user credentials)
usersFile = "users.tdxt"

# class to define the user model (username and password)
class User(BaseModel):
    username: str
    password: str

# creating a function to hash the password using user input and bcrypt
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #hash the password

# creating a function to verify the password with the hashed password
def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@app.post("/authenticate")
async def authenticate(user: User):
    # Save the user data in the in-memory storage
    users_db[user.username] = user.password
    return {"message": f"User {user.username} authenticated and saved successfully"}

@app.get("/users")
async def get_users():
    return users_db
