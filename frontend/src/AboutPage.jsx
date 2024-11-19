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
        <p>Brief bio about Daniel goes here.</p>
      </div>
      <div className="creator">
        <img
          src="/assets/simona.jpg" // Placeholder path for Simona's image
          alt="Simona Sellecchia"
          className="creator-image"
        />
        <h2>Simona Sellecchia</h2>
        <p>Brief bio about Simona goes here.</p>
      </div>
    </div>
  );
};

export default AboutPage;