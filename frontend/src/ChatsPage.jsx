import React from 'react';
import { PrettyChatWindow } from 'react-chat-engine-pretty';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation

const ChatsPage = (props) => {
    const navigate = useNavigate(); // Initialize navigate

    const handleHomeClick = () => {
        navigate('/'); // Navigate to the Home (Auth) page
    };

    return (
        <div className="background">
            {/* Home Button */}
            <button className="home-button" onClick={handleHomeClick}>
                🏠 Home
            </button>

            <div className='chat-wrapper'>
                <PrettyChatWindow
                    projectId={import.meta.env.VITE_CHAT_ENGINE_PROJECT_ID}
                    username={props.user.username}
                    secret={props.user.secret}
                    style={{ height: '100vh' }} // Optional: Adjust height as needed
                />
            </div>
        </div>
    );
}

export default ChatsPage;