from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Handles Cross-Origin Resource Sharing
from pydantic import BaseModel  # For defining the request and response models meaning we can validate the data
import bcrypt # For hashing passwords
import os # For file operations meaning we can read and write to files
import logging # For logging the events that happen in the backend
from typing import List 
from datetime import datetime # For timestamping messages
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path to the users file
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
usersFile = os.path.join(BASE_DIR, "users.txt") 
messages_file = os.path.join(BASE_DIR, "messages.txt")

app = FastAPI()

# CORS configuration to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update if your frontend runs on a different URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for User
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
        raise HTTPException(status_code=500, detail="Internal Server Error")

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
                    storedUsername, stored_hashed_password = line.strip().split(",")
                    if storedUsername == username and verifyPassword(password, stored_hashed_password.encode('utf-8')):
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
        raise HTTPException(status_code=400, detail="User already registered")
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
        raise HTTPException(status_code=401, detail="Invalid username or password")

# Endpoint to get all registered users (optional)
@app.get("/users")
async def get_users():
    users = []
    try:
        with open(usersFile, "r") as f:
            for line in f:
                try:
                    username, _ = line.strip().split(",")
                    users.append(username)
                except ValueError:
                    # Skip lines that don't have the correct format
                    continue
        logger.info("Fetched list of registered users.")
    except FileNotFoundError:
        logger.warning("No users registered yet.")
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"users": users}

# ----------------------------
# WebSocket Chat Implementation
# ----------------------------

class ConnectionManager: # Manages WebSocket connections
    def __init__(self):
        self.active_connections: List[WebSocket] = [] # List to store active connections

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket connection closed. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        logger.info(f"Broadcasting message: {message}")
        disconnected_websockets = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to a client: {e}")
                disconnected_websockets.append(connection)
        for websocket in disconnected_websockets:
            self.disconnect(websocket)

manager = ConnectionManager() # Create an instance of ConnectionManager meaning we can manage WebSocket connections

# Function to save a message to the file
def save_message(message: dict):
    try:
        with open(messages_file, "a") as f:
            f.write(json.dumps(message) + "\n")
        logger.info(f"Message saved: {message}")
    except Exception as e:
        logger.error(f"Error saving message: {e}")

# Function to load all messages
def load_messages() -> List[dict]:
    messages = []
    try:
        with open(messages_file, "r") as f:
            for line in f:
                try:
                    message = json.loads(line.strip())
                    messages.append(message)
                except json.JSONDecodeError:
                    continue
        logger.info("Loaded chat history.")
    except FileNotFoundError:
        logger.warning("No chat history found.")
    except Exception as e:
        logger.error(f"Error loading messages: {e}")
    return messages

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send chat history to the connected client
        messages = load_messages()
        for message in messages:
            await websocket.send_json(message)

        while True:
            data = await websocket.receive_json()
            username = data.get("username")
            content = data.get("content")
            
            if not username or not content:
                logger.warning("Received invalid message format.")
                continue

            # Create message object with timestamp
            timestamp = datetime.utcnow().isoformat() + "Z"
            message = {
                "username": username,
                "content": content,
                "timestamp": timestamp
            }

            # Save the message
            save_message(message)

            # Broadcast the message to all connected clients
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Error in WebSocket communication: {e}")
        manager.disconnect(websocket)
