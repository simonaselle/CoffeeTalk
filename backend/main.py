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
def verifyPassword(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# creating a function to save the user data in the file
def saveUser(username: User):
    with open(usersFile, "a") as f: #open the file in append; append mode is used to add the data to the end of the file
        f.write(f"{username.username},{hash_password(username.password).decode()}\n") # write the username and hashed password in the file

# creating a function to read the user data from the file (authenticating the user)
def authenticateUser(username: User, password: str):
    with open(usersFile, "r") as f: # opening the file in read mode 'r' 
        for line in f: # iterating through the file 
            username, hashed_password = line.strip().split("") # reading the user's credentials and splitting with a space 
            if username == username.username and verifyPassword(password, hashed_password): # check if the username and password match
                return True
    return # otherwise return false 

@app.post("/authenticate")
async def authenticate(user: User):
    # Save the user data in the in-memory storage
    users_db[user.username] = user.password
    return {"message": f"User {user.username} authenticated and saved successfully"}

@app.get("/users")
async def get_users():
    return users_db
