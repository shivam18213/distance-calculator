import React from 'react';
import './CalculatorForm.css';

const CalculatorForm = ({
  source,
  destination,
  unit,
  loading,
  distance,
  onSourceChange,
  onDestinationChange,
  onUnitChange,
  onSubmit,
}) => {
  const getDisplayDistance = () => {
    if (!distance) return '';

    if (unit === 'miles') {
      return `${distance.distance_miles} mi`;
    } else if (unit === 'kilometers') {
      return `${distance.distance_km} km`;
    } else {
      return `${distance.distance_miles} mi   ${distance.distance_km} km`;
    }
  };

  return (
    <form onSubmit={onSubmit} className="calculator-form">
      <div className="form-row">
        <div className="form-group">
          <label>Source Address</label>
          <input
            type="text"
            value={source}
            onChange={(e) => onSourceChange(e.target.value)}
            placeholder="Input address"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Destination Address</label>
          <input
            type="text"
            value={destination}
            onChange={(e) => onDestinationChange(e.target.value)}
            placeholder="Input address"
            required
            disabled={loading}
          />
        </div>

        <div className="unit-group">
          <label>Unit</label>
          <div className="radio-group">
            <label className="radio-label">
              <input
                type="radio"
                name="unit"
                value="miles"
                checked={unit === 'miles'}
                onChange={(e) => onUnitChange(e.target.value)}
              />
              <span>Miles</span>
            </label>
            <label className="radio-label">
              <input
                type="radio"
                name="unit"
                value="kilometers"
                checked={unit === 'kilometers'}
                onChange={(e) => onUnitChange(e.target.value)}
              />
              <span>Kilometers</span>
            </label>
            <label className="radio-label">
              <input
                type="radio"
                name="unit"
                value="both"
                checked={unit === 'both'}
                onChange={(e) => onUnitChange(e.target.value)}
              />
              <span>Both</span>
            </label>
          </div>
        </div>

        <div className="distance-display">
          <label>Distance</label>
          <div className="distance-value">{getDisplayDistance()}</div>
        </div>
      </div>

      <button
        type="submit"
        className={`calculate-btn ${loading ? 'loading' : ''}`}
        disabled={loading}
      >
        {loading ? (
          <>
            <span className="spinner"></span>
            Calculating...
          </>
        ) : (
          <>
            Calculate Distance
             <svg
                        className="calculator-icon"
                        width="16"
                        height="16"
                        viewBox="0 0 16 16"
                        aria-hidden="true"
                      >
                        <rect x="2.5" y="1.5" width="11" height="13" rx="1.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
                        <rect x="4.5" y="3.5" width="7" height="2" fill="currentColor" />
                        <circle cx="5.5" cy="8.5" r="0.8" fill="currentColor" />
                        <circle cx="8" cy="8.5" r="0.8" fill="currentColor" />
                        <circle cx="10.5" cy="8.5" r="0.8" fill="currentColor" />
                        <circle cx="5.5" cy="11" r="0.8" fill="currentColor" />
                        <circle cx="8" cy="11" r="0.8" fill="currentColor" />
                        <rect x="9.8" y="10.2" width="1.4" height="2.4" fill="currentColor" />
                      </svg>
                    </>
          
        )}
      </button>
    </form>
  );
};

export default CalculatorForm;
