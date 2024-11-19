import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const AuthPage = (props) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); // Initialize navigate

  const onSubmit = (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    if (isRegistering) {
      // Registration logic
      axios.post('http://localhost:8000/register', { username, password })
        .then((response) => {
          alert(response.data.message);
          setIsRegistering(false);
        })
        .catch((error) => {
          console.error("Registration failed:", error);
          setErrorMessage("Registration failed. User may already exist.");
        });
    } else {
      // Authentication logic
      axios.post('http://localhost:8000/authenticate', { username, password })
        .then((response) => {
          props.onAuth({ username, secret: password });
        })
        .catch((error) => {
          console.error("Authentication failed:", error);
          setErrorMessage("Invalid username or password.");
        });
    }
  };

  return (
    <div className="background">
      <div className="form-card">
        <h1 className="main-heading">
          {isRegistering ? 'Register' : 'Welcome to CoffeeTalk☕'}
        </h1>
        <form onSubmit={onSubmit}>
          <div className="form-subtitle">
            {isRegistering
              ? 'Create a new account.'
              : 'Set a Username and Password to get started. New User? Click "New User" to create an account.'}
          </div>

          <div className="auth">
            <input
              className="auth-input"
              name="username"
              placeholder="Username"
              required
            />
            <input
              className="auth-password"
              name="password"
              type="password"
              placeholder="Password"
              required
            />
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <button className="auth-button" type="submit">
              {isRegistering ? 'Register' : 'Enter'}
            </button>
            <button
              className="new-user-button"
              type="button"
              onClick={() => {
                setIsRegistering(!isRegistering);
                setErrorMessage('');
              }}
            >
              {isRegistering ? 'Back to Login' : 'New User'}
            </button>
            <button
              className="about-button"
              type="button"
              onClick={() => navigate('/about')} // Navigate to About page
            >
              About Creators
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AuthPage;