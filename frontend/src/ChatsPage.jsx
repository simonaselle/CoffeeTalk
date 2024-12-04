import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChatsPage.css';
import axios from 'axios'; // Import axios for HTTP requests

const ChatsPage = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const ws = useRef(null);
  const navigate = useNavigate();
  const [usersList, setUsersList] = useState([]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    ws.current = new WebSocket('ws://localhost:8000/ws/chat');

    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      ws.current.close();
    };
  }, []);

  useEffect(() => {
    // Scroll to the latest message
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  useEffect(() => {
    // Fetch the list of registered users
    axios.get('http://localhost:8000/users')
      .then(response => {
        setUsersList(response.data.users.filter(username => username !== user.username));
      })
      .catch(error => {
        console.error("Error fetching users:", error);
      });
  }, [user.username]);

  const sendMessage = () => {
    if (input.trim() === '') return;
    const message = {
      username: user.username,
      content: input,
    };
    ws.current.send(JSON.stringify(message));
    setInput('');
  };

  const formatTimestamp = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString(); // Converts UTC to local time
  };

  const handleHomeClick = () => {
    navigate('/'); // Navigate to the Home (Auth) page
  };

  return (
    <div className="background">
    {/* Home Button */}
    <button className="home-button" onClick={handleHomeClick}>
      🏠 Home
    </button>

      <div className="chat-container">
        {/* User List */}
        <div className="users-list">
          <h3>Online Users</h3>
          <ul>
            {usersList.map((username, idx) => (
              <li key={idx}>{username}</li>
            ))}
          </ul>
        </div>

        {/* Chat Interface */}
        <div className="chat-wrapper">
          <div className="chat-header">
            <h2>Welcome, {user.username}!</h2>
          </div>
          <div className="messages">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`message ${msg.username === user.username ? 'own-message' : ''}`}
              >
                <div className="message-content">
                  <strong>{msg.username}: </strong>
                  <span>{msg.content}</span>
                </div>
                <div className="timestamp">{formatTimestamp(msg.timestamp)}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              onKeyPress={(e) => {
                if (e.key === 'Enter') sendMessage();
              }}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatsPage;