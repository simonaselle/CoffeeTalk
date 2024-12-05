import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChatsPage.css';
import axios from 'axios';
import PrivateChat from './PrivateChat'; // Import the PrivateChat component

const ChatsPage = ({ user }) => {
  const navigate = useNavigate();
  const [usersList, setUsersList] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);

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

  const handleUserClick = (username) => {
    setSelectedUser(username);
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
          <h3>Users</h3>
          <ul>
            {usersList.map((username, idx) => (
              <li key={idx} onClick={() => handleUserClick(username)}>
                {username}
              </li>
            ))}
          </ul>
        </div>

        {/* Chat Interface */}
        {selectedUser ? (
          <PrivateChat user={user} recipient={selectedUser} />
        ) : (
          <div className="no-chat-selected">
            <h2>Select a user to start chatting</h2>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatsPage;