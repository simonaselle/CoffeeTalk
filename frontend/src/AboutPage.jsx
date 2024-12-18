import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import danielImage from './assets/DanielPenn.jpg';
import simonaImage from './assets/simona2.jpeg';
import './AboutPage.css';

const AboutPage = () => {
  const navigate = useNavigate(); // Initialize navigate

  const handleBackClick = () => {
    navigate('/'); // Navigate to Home Page
  };

  return (
    <div className="about-container">
      {/* Back Button */}
      <button className="back-button" onClick={handleBackClick}>
        🏠Home
      </button>

      <h1>About the Creators</h1>
      <div className="content">
        {/* Left Column */}
        <div className="left-column">
          <div className="creator">
            <img
              src={danielImage}
              alt="Daniel Hodowanec"
              className="creator-image"
            />
            <h2>Hi, I'm Daniel Hodowanec!</h2>
          </div>
          <div className="creator">
            <img
              src={simonaImage}
              alt="Simona Sellecchia"
              className="creator-image"
            />
            <h2>Hi, I'm Simona Sellecchia!</h2>
          </div>
        </div>

        {/* Right Column */}
        <div className="right-column">
          <div className="app-info">
            <h2>Why We Created This App</h2>
            <p>
              Both of us share a keen interest in cybersecurity, and this project was a great opportunity to combine that with web development.
              Our goal was to demonstrate how simple it is to learn and build a functional chat app while emphasizing the importance of user authentication.
              We chose to use a text file (txt) to store usernames and hashed passwords encrypted with bcrypt. This approach allowed us to show how
              salted hashes protect passwords, making them incredibly difficult to crack—even if the data is exposed.
            </p>
            <p>
              Through this project, we hope to inspire others to explore coding while understanding the critical role cybersecurity plays
              in protecting user data. We also wanted to highlight how even basic implementations can introduce important security concepts!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;