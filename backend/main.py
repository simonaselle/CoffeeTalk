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
usersFile = "backend/users.txt"

# class to define the user model (username and password)
class User(BaseModel):
    username: str
    password: str

# creating a function to hash the password using user input and bcrypt
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #hash the password

# creating a function to verify the password with the hashed password
def verifyPassword(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# creating a function to save the user data in the file
def saveUser(user: User):
    with open(usersFile, "a") as f: #open the file in append; append mode is used to add the data to the end of the file
        f.write(f"{user.username},{hash_password(user.password).decode()}\n") # write the username and hashed password in the file

# creating a function to read the user data from the file (authenticating the user)
def authenticateUser(username: str, password: str):
    with open(usersFile, "r") as f: # opening the file in read mode 'r' 
        for line in f: # iterating through the file 
            storedUsername, storedHashedPassword = line.strip().split("") # reading the user's credentials and splitting with a space 
            if storedUsername == username and verifyPassword(password, storedHashedPassword.encode()): # check if the username and password match the stored credentials
                return True # return true if the user is authenticated
    return False # otherwise return false 

# need a register method to connect to the frontend 
@app.post("/register")
async def register(user: User): # register method that takes the user data
    if authenticateUser(user.username, user.password): # check if the user is already registered
        return {"message": "User already registered"} # if the user is already registered, return a message that the user is already registered
    else:
        saveUser(user) # save the user data in the file
        return {"message": f"User {user.username} registered successfully"} # return a message that the user is registered successfully

# authenticate method that connects to the frontend 
@app.post("/authenticate") # 
async def authenticate(user: User):
    if not authenticateUser(user.username, user.password): # check if the user is in the file and matches whats in the file 
        return {"message": "Invalid username or password"}
    else: 
        return {"message": f"User {user.username} authenticated and saved successfully"}

# getting the user that connects to the frontend 
@app.post("/users")
async def get_users():
    users = [] # empty list to store the users
    try: # use try block to handle the exception of not finding the file
        with open(usersFile, "r") as f: # open the file in read mode 'r'
            for line in f:
                username, _ = line.strip().split("") # split the username and password with a space 
                users.append(username) # append the username to the list
    except FileNotFoundError: # if the file is not found, pass
        pass 
    return {"users": users} # return the list of users
