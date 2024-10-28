from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #can call this server from any other website 
from pydantic import BaseModel
from bcrypt import bcrypt

app = FastAPI()

# Allow all origins to access the server (frontend -> backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# File to store the data 
usersFile = "users.tdxt"

# 
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

class User(BaseModel):
    username: str
    password: str


@app.post("/authenticate")
async def authenticate(user: User):
    # Save the user data in the in-memory storage
    users_db[user.username] = user.password
    return {"message": f"User {user.username} authenticated and saved successfully"}

@app.get("/users")
async def get_users():
    return users_db
