import React from 'react';
import './ErrorToast.css';

const ErrorToast = ({ error, onClose }) => {
  if (!error) return null;

  return (
    <div className="error-toast">
      <div className="error-content">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
          <circle cx="10" cy="10" r="9" />
          <path
            d="M10 6v4M10 14v1"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
        <div>
          <strong>Calculation failed</strong>
          <p>{error}</p>
        </div>
      </div>
      <button onClick={onClose} className="close-btn">
        ×
      </button>
    </div>
  );
};

export default ErrorToast;
