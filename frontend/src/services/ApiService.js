
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class ApiService {

  static async calculateDistance(source, destination) {
    const response = await fetch(`${API_URL}/calculate-distance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        source: source.trim(),
        destination: destination.trim(),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to calculate distance');
    }

    return data;
  }

  static async fetchHistory(limit = 50) {
    const response = await fetch(`${API_URL}/history?limit=${limit}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch history');
    }

    return data.queries || [];
  }

  /**
   * Health check
   * @returns {Promise<Object>} Health status
   */
  static async healthCheck() {
    const response = await fetch(`${API_URL}/health`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error('Health check failed');
    }

    return data;
  }
}

export default ApiService;
