from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Allows cross-origin requests
from pydantic import BaseModel
import bcrypt
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path to the file where the user data will be stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
usersFile = os.path.join(BASE_DIR, "users.txt")

app = FastAPI()

# Allow requests from the frontend (adjust the origin if necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the User model
class User(BaseModel):
    username: str
    password: str

# Function to hash passwords
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify passwords
def verifyPassword(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Function to save a new user
def saveUser(user: User):
    try:
        with open(usersFile, "a") as f:
            f.write(f"{user.username},{hash_password(user.password).decode('utf-8')}\n")
        logger.info(f"User '{user.username}' saved successfully.")
    except Exception as e:
        logger.error(f"Error saving user '{user.username}': {e}")

# Function to check if a user exists
def checkUserExists(username: str) -> bool:
    try:
        with open(usersFile, "r") as f:
            for line in f:
                storedUsername, _ = line.strip().split(",")
                if storedUsername == username:
                    return True
    except FileNotFoundError:
        # No users have been registered yet
        return False
    except Exception as e:
        logger.error(f"Error checking if user exists: {e}")
    return False

# Function to authenticate a user
def authenticateUser(username: str, password: str) -> bool:
    try:
        with open(usersFile, "r") as f:
            for line in f:
                try:
                    storedUsername, storedHashedPassword = line.strip().split(",")
                    if storedUsername == username and verifyPassword(password, storedHashedPassword.encode('utf-8')):
                        return True
                except ValueError:
                    # Skip lines that don't have the correct format
                    continue
    except FileNotFoundError:
        # If the file doesn't exist, no users are registered yet
        return False
    except Exception as e:
        logger.error(f"Error authenticating user '{username}': {e}")
    return False

# Registration endpoint
@app.post("/register")
async def register(user: User):
    logger.info(f"Registration attempt for user: '{user.username}'")
    if checkUserExists(user.username):
        logger.warning(f"Registration failed: User '{user.username}' already exists.")
        return {"message": "User already registered"}
    else:
        saveUser(user)
        logger.info(f"User '{user.username}' registered successfully.")
        return {"message": f"User '{user.username}' registered successfully"}

# Authentication endpoint
@app.post("/authenticate")
async def authenticate(user: User):
    logger.info(f"Authentication attempt for user: '{user.username}'")
    if authenticateUser(user.username, user.password):
        logger.info(f"User '{user.username}' authenticated successfully.")
        return {"message": f"User '{user.username}' authenticated successfully"}
    else:
        logger.warning(f"Authentication failed for user '{user.username}'")
        return {"message": "Invalid username or password"}

# Endpoint to get all registered users (optional)
@app.get("/users")
async def get_users():
    users = []
    try:
        with open(usersFile, "r") as f:
            for line in f:
                username, _ = line.strip().split(",")
                users.append(username)
        logger.info("Fetched list of registered users.")
    except FileNotFoundError:
        logger.warning("No users registered yet.")
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
    return {"users": users}
