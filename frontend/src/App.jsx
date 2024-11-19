import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AuthPage from './AuthPage';
import ChatsPage from './ChatsPage';
import AboutPage from './AboutPage'; // Import the AboutPage component
import './App.css';

function App() {
  const [user, setUser] = useState(undefined);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            !user ? (
              <AuthPage onAuth={(user) => setUser(user)} />
            ) : (
              <ChatsPage user={user} />
            )
          }
        />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Router>
  );
}

export default App;
