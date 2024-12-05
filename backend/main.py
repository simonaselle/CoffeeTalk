from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware  # Handles Cross-Origin Resource Sharing
from pydantic import BaseModel  # For defining the request and response models meaning we can validate the data
import bcrypt # For hashing passwords
import os # For file operations meaning we can read and write to files
import logging # For logging the events that happen in the backend
from typing import List, Dict
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

# Modify the ConnectionManager to handle rooms
class ConnectionManager: # Manages WebSocket connections
    def __init__(self):
        # Active connections per room
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.online_users: set = set()

    async def connect(self, websocket: WebSocket, room: str, username: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)
        self.online_users.add(username)
        # Send updated online users list to all clients

    def disconnect(self, websocket: WebSocket, room: str, username: str):
        self.active_connections[room].remove(websocket)
        if not self.active_connections[room]:
            del self.active_connections[room]
        self.online_users.discard(username)
        # Send updated online users list to all clients

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict, room: str):
        logger.info(f"Broadcasting message to room '{room}': {message}")
        disconnected_websockets = []
        for connection in self.active_connections.get(room, []):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to a client: {e}")
                disconnected_websockets.append(connection)
        for websocket in disconnected_websockets:
            self.disconnect(websocket, room)

manager = ConnectionManager() # Create an instance of ConnectionManager meaning we can manage WebSocket connections

# Function to save a message to the file for a specific room
def save_message(message: dict, room: str):
    try:
        room_messages_file = os.path.join(BASE_DIR, f"messages_{room}.txt")
        with open(room_messages_file, "a") as f:
            f.write(json.dumps(message) + "\n")
        logger.info(f"Message saved in room '{room}': {message}")
    except Exception as e:
        logger.error(f"Error saving message in room '{room}': {e}")

# Function to load all messages for a specific room
def load_messages(room: str) -> List[dict]:
    messages = []
    room_messages_file = os.path.join(BASE_DIR, f"messages_{room}.txt")
    try:
        with open(room_messages_file, "r") as f:
            for line in f:
                try:
                    message = json.loads(line.strip())
                    messages.append(message)
                except json.JSONDecodeError:
                    continue
        logger.info(f"Loaded chat history for room '{room}'.")
    except FileNotFoundError:
        logger.warning(f"No chat history found for room '{room}'.")
    except Exception as e:
        logger.error(f"Error loading messages for room '{room}': {e}")
    return messages

# WebSocket endpoint for private messaging with query parameter 'room'
@app.websocket("/ws/chat/{recipient}")
async def websocket_endpoint(websocket: WebSocket, recipient: str, username: str = Query(...)):
    room = "_".join(sorted([username, recipient]))  # Unique room ID for the conversation
    await manager.connect(websocket, room, username)
    try:
        # Load and send chat history for this room
        messages = load_messages(room)
        for message in messages:
            await websocket.send_json(message)

        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            if not content:
                logger.warning("Received invalid message format.")
                continue

            timestamp = datetime.utcnow().isoformat() + "Z"
            message = {
                "username": username,
                "content": content,
                "timestamp": timestamp,
                "recipient": recipient
            }

            # Save the message to file
            save_message(message, room)

            # Broadcast the message to this room
            await manager.broadcast(message, room)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room, username)
    except Exception as e:
        logger.error(f"Error in WebSocket communication: {e}")
        manager.disconnect(websocket, room, username)

@app.get("/online-users")
async def get_online_users():
    return {"online_users": list(manager.online_users)}