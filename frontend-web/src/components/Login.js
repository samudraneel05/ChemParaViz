import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (isRegister) {
      const result = await register(username, password, email);
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error);
      }
    } else {
      const result = await login(username, password);
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error);
      }
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>{isRegister ? 'Create Account' : 'Welcome Back'}</h1>
        <h2>ChemParaViz - Chemical Equipment Analytics</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          
          {isRegister && (
            <div className="form-group">
              <label>Email (Optional)</label>
              <input
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          )}
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" className="btn-primary">
            {isRegister ? 'Register' : 'Login'}
          </button>
        </form>
        
        <p className="toggle-auth">
          {isRegister ? 'Already have an account? ' : "Don't have an account? "}
          <span onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'Login' : 'Register'}
          </span>
        </p>
      </div>
    </div>
  );
};

export default Login;
