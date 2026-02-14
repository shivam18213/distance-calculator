import React from 'react';
import './Header.css';

const Header = ({ showHistory, onToggleView }) => {
  return (
    <header className="header">
      <div className="header-content">
        <h1>Distance Calculator</h1>
        <p className="subtitle">
          Prototype web application for calculating the distance between addresses.
        </p>
      </div>
      <button className="view-history-btn" onClick={onToggleView}>
        {showHistory ? (
          <>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M3 3h10v10H3z" />
            </svg>
            Back to Calculator
          </>
        ) : (
          <>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                d="M8 14A6 6 0 108 2a6 6 0 000 12z"
                stroke="currentColor"
                strokeWidth="1.5"
              />
              <path
                d="M8 5v3l2 2"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
            View Historical Queries
          </>
        )}
      </button>
    </header>
  );
};

export default Header;
