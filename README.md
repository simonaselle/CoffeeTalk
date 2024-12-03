# Coffee Talk: Messaging System 
---
## Project Overview 
***Coffee Talk*** is a real-time web based chat application. This project was designed to provide a private messaging platform where users can communicate via messaging system with one another.

## Built With
- FastAPI (Web framework for building APIs with Python) 
- CORSMiddleware (Handles cross-origin resource sharing) 
- React (JavaScript library for building user interfaces)
- Axios (sends HTTP requests; communicates with backend)
- Bcrypt Hashing (Provides secure password hashing)
- GitHub Copilot (Assisted with development productivity)
- ChatGPT (Assisted with project outline)

## Getting Started 
### Prerequisites 
Make sure you have the following installed on your machine: 
- **Backend**: Python 3.9+ & pip
- **Frontend**: Node.js & npm

### How to Run the Website on Your Local Machine 
#### Terminal 1: Backend Setup 
1. **Navigate to the Backend Directory and Activate a Virtual Environment**
```bash
cd CoffeeTalk/backend 
source venv/bin/activate # For Linux/macOS 
venv\Scripts\activate    # For Windows 
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt 
```

3. **Ensure users.txt Exists**
```bash
touch users.txt   # For Linux/macOS
echo. > users.txt # For Windows
```

4. **Set Permissions**
```bash
chmod 666 users.txt # For Linux/macOS
```

5. **Start the Backend Server**
```bash
uvicorn main:app --reload
```
--- 

***Open another terminal window to set up the frontend.***

---

#### Terminal 2: Frontend Setup 
1. **Navigate to the Frontend Directory**
```bash
cd CoffeeTalk/frontend # For Linux/macOS
cd CoffeeTalk\frontend # For Windows
```

2. **Install Frontend Dependencies**
```bash
npm install 
```

3. **Start the Frontend Development Server**
```bash
npm run dev 
```



## Usage 
Open your preferred web browser and click the link provided to you in the frontend terminal. Register a new account(if you don't have one already) by clikcing on the "New User" button. Here, you will create a username (how you would like your name displayed to other users) and a password. 

Once logged in, you'll have access to a web based chat application where you can connect with other users in real time. You will have the ability to create a chat and message with your friends! ***Coffee Talk*** ensures a safe messaging experience, and saved history so you can pick up right where you left off. 


## Credits 
1. **Group Members**:
- Daniel Hodowanec
- Simona Sellecchia 
2. **Resources**: 
- [Adam La Morre's Python Realtime Chat](https://www.youtube.com/watch?v=YDZPp0EnzEA)
- [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware)
- [How to create authentication using an external text file](https://stackoverflow.com/questions/55868424/how-to-create-authentication-using-an-external-text-file)
- [Hashing passwords with Python and Bcrypt](https://www.youtube.com/watch?v=hNa05wr0DSA)
- [Hashing Passwords in Python with BCrypt](https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/)
- **Duckett, Jon.** *HTML & CSS: Design and Build Websites*. Wiley, 2011. 
- [Axios in React: A Guide for Beginners](https://www.geeksforgeeks.org/axios-in-react-a-guide-for-beginners/#introduction-to-axios)