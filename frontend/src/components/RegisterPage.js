import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './RegisterPage.css';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    const response = await fetch('http://localhost:5001/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    if (response.ok) {
      navigate('/login');
    } else {
      setError(data.error || 'Registration failed');
    }
  };

  return (
    <div className="register-container">
      <h2 className="register-title">Register</h2>
      <form className="register-form" onSubmit={handleRegister}>
        <input type="text" className="register-input" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input type="password" className="register-input" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" className="register-button">Register</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default RegisterPage;