import React, { useState, useEffect, useRef } from 'react';
import './PrivateChat.css';

const PrivateChat = ({ user, recipient }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${recipient}?username=${user.username}`);

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
  }, [user.username, recipient]);

  useEffect(() => {
    // Scroll to the latest message
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = () => {
    if (input.trim() === '') return;
    const message = {
      content: input,
    };
    ws.current.send(JSON.stringify(message));
    setInput('');
  };

  const formatTimestamp = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString(); // Converts UTC to local time
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-header">
        <h2>Chat with {recipient}</h2>
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
  );
};

export default PrivateChat;