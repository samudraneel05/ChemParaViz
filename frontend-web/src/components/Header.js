import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Header.css';

const Header = ({ showDashboardTitle = false }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <header className="app-header">
      <h1 onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
        {showDashboardTitle ? 'ChemParaViz Dashboard' : 'ChemParaViz'}
      </h1>
      <div className="user-info">
        {user ? (
          <>
            <span>Welcome, {user.username}!</span>
            <button onClick={handleLogout} className="btn-logout">Logout</button>
          </>
        ) : (
          <button onClick={handleLogin} className="btn-login">Login</button>
        )}
      </div>
    </header>
  );
};

export default Header;
