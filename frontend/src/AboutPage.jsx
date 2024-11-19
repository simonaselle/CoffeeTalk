import React from 'react';
import './AboutPage.css'; // Create this CSS file for styling

const AboutPage = () => {
  return (
    <div className="about-container">
      <h1>About the Creators</h1>
      <div className="creator">
        <img
          src="/assets/daniel.jpg" // Placeholder path for Daniel's image
          alt="Daniel Hodowanec"
          className="creator-image"
        />
        <h2>Daniel Hodowanec</h2>
        <p> 
          I'm a Computer Science major who enjoys HTML & CSS and system security. Simona 
          and I share an interest in cybersecurity, which is why we built this chat app. It’s more than just a 
          messaging tool—it’s a way to demonstrate the importance of protecting user data and passwords.
          </p>
          <p>
          Working on this project taught us a lot about integrating technologies, from setting up the front end 
          to managing authentication.
        </p>
      </div>
      <div className="creator">
        <img
          src="/assets/simona.jpg" // Placeholder path for Simona's image
          alt="Simona Sellecchia"
          className="creator-image"
        />
        <h2>Simona Sellecchia</h2>
        <p>
          I'm a Computer Science major with a passion for cybersecurity. My partner, Daniel, 
          and I worked together on each aspect of creating this chat app. We wanted to show people how easy it 
          can be to build a website, but also why user authentication is so important. 
          </p>
          <p>
          For this project, we used a text file (txt) to store usernames and hashed passwords (encrypted with bcrypt). 
          The cool part? The "salted" hashes make the passwords nearly impossible to guess—even if someone 
          got access to the file. Unless you're a *really* good hacker, of course!
        </p>
      </div>
    </div>
  );
};

export default AboutPage;