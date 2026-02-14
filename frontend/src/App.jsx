/**
 * Main App Component
 * Coordinates all components and manages application state
 */

import React from 'react';
import './App.css';

// Components
import Header from './components/Header/Header';
import CalculatorForm from './components/CalculatorForm/CalculatorForm';
import ErrorToast from './components/ErrorToast/ErrorToast';
import HistoryTable from './components/HistoryTable/HistoryTable';

// Custom Hook
import useDistanceCalculator from './hooks/useDistanceCalculator';

function App() {
  const {
    source,
    destination,
    loading,
    result,
    error,
    history,
    showHistory,
    unit,
    setSource,
    setDestination,
    setUnit,
    calculateDistance,
    toggleView,
    clearError,
  } = useDistanceCalculator();

  return (
    <div className="app">
      <div className="container">
        <Header showHistory={showHistory} onToggleView={toggleView} />

        {!showHistory ? (
          <div className="main-form">
            <CalculatorForm
              source={source}
              destination={destination}
              unit={unit}
              loading={loading}
              distance={result}
              onSourceChange={setSource}
              onDestinationChange={setDestination}
              onUnitChange={setUnit}
              onSubmit={calculateDistance}
            />

            <ErrorToast error={error} onClose={clearError} />
          </div>
        ) : (
          <HistoryTable queries={history} />
        )}
      </div>
    </div>
  );
}

export default App;
