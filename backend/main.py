from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class User(BaseModel):
    username: str
    password: str

# In-memory storage for demonstration purposes
users_db = {}

@app.post("/authenticate")
async def authenticate(user: User):
    # Save the user data in the in-memory storage
    users_db[user.username] = user.password
    return {"message": f"User {user.username} authenticated and saved successfully"}

@app.get("/users")
async def get_users():
    return users_db
