import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Landing.css';

const Landing = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="landing-container">
      <div className="landing-content">
        <div className="landing-left">
          <h1 className="landing-title">
            Chemical Equipment
            <br />
            Parameter Visualizer
          </h1>
          <p className="landing-subtitle">
            Upload CSV files and get instant analytics with beautiful charts, 
            detailed statistics, and downloadable PDF reports.
          </p>
          <div className="landing-actions">
            <button className="btn-primary btn-large" onClick={() => navigate('/login')}>
              Get Started
            </button>
            <button className="btn-secondary btn-large" onClick={() => navigate('/login')}>
              Login
            </button>
          </div>
        </div>
        <div className="landing-right">
          <div className="dashboard-preview">
            <div className="preview-header">
              <div className="preview-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div className="preview-content">
              <img src="/demo.png" alt="Dashboard Preview" className="preview-image" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
