import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from './AuthPage';
import ChatsPage from './ChatsPage';
import AboutPage from './AboutPage'; // Decide to keep this import
import LoginForm from './LoginForm';
import './App.css';

function App() {
  const [user, setUser] = useState(null);


  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route path="/chat" element={<ChatsPage user={user} />} />
        <Route path="/about" element={<AboutPage />} />
        {/* Redirect any other route to login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}


export default App;