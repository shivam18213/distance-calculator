import { useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const useDistanceCalculator = () => {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [unit, setUnit] = useState('miles');

  // Fetch history on mount
  useEffect(() => {
    fetchHistory();
  }, []);

  /**
   * Fetch historical queries from the API
   */
  const fetchHistory = async () => {
    try {
      const queries = await ApiService.fetchHistory();
      setHistory(queries);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  /**
   * Calculate distance between source and destination
   */
  const calculateDistance = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      const data = await ApiService.calculateDistance(source, destination);
      setResult(data);
      await fetchHistory(); // Refresh history after new query
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Toggle between calculator and history view
   */
  const toggleView = () => {
    setShowHistory(!showHistory);
  };

  /**
   * Clear error message
   */
  const clearError = () => {
    setError(null);
  };

  return {
    // State
    source,
    destination,
    loading,
    result,
    error,
    history,
    showHistory,
    unit,

    // Actions
    setSource,
    setDestination,
    setUnit,
    calculateDistance,
    toggleView,
    clearError,
  };
};

export default useDistanceCalculator;
