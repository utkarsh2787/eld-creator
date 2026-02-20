import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import RouteMap from './components/RouteMap';
import ScheduleTable from './components/ScheduleTable';
import ELDLogs from './components/ELDLogs';
import CityAutocomplete from './components/CityAutocomplete';

function App() {
  const [formData, setFormData] = useState({
    current_location: '',
    pickup_location: '',
    dropoff_location: '',
    current_cycle_used: '',
    driver_name: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('https://eld-creator.onrender.com/api/plan-trip/', formData, {
        timeout: 1000000, // 10 second timeout
      });
      setResults(response.data);
    } catch (err) {
      if (err.code === 'ECONNABORTED' || err.message?.toLowerCase().includes('timeout')) {
        setError('⏱ Request timed out — the server took too long to respond. Route may not be available.');
      } else {
        setError(err.response?.data?.error || 'Route not found or an error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🚚 ELD Trip Planner</h1>
          <p>Plan HOS-compliant trips with automated route planning and ELD logs</p>
        </header>

        <div className="input-section">
          <form onSubmit={handleSubmit}>
            <div className="input-grid">
              <div className="input-group">
                <label htmlFor="current_location">Current Location</label>
                <CityAutocomplete
                  id="current_location"
                  name="current_location"
                  value={formData.current_location}
                  onChange={handleInputChange}
                  placeholder="e.g., Los Angeles, CA"
                />
              </div>

              <div className="input-group">
                <label htmlFor="pickup_location">Pickup Location</label>
                <CityAutocomplete
                  id="pickup_location"
                  name="pickup_location"
                  value={formData.pickup_location}
                  onChange={handleInputChange}
                  placeholder="e.g., Phoenix, AZ"
                />
              </div>

              <div className="input-group">
                <label htmlFor="dropoff_location">Dropoff Location</label>
                <CityAutocomplete
                  id="dropoff_location"
                  name="dropoff_location"
                  value={formData.dropoff_location}
                  onChange={handleInputChange}
                  placeholder="e.g., Dallas, TX"
                />
              </div>

              <div className="input-group">
                <label htmlFor="current_cycle_used">Current Cycle Used (Hours)</label>
                <input
                  type="number"
                  id="current_cycle_used"
                  name="current_cycle_used"
                  value={formData.current_cycle_used}
                  onChange={handleInputChange}
                  placeholder="0-70"
                  min="0"
                  max="70"
                  step="0.1"
                  required
                />
              </div>

              <div className="input-group">
                <label htmlFor="driver_name">Driver Name</label>
                <input
                  type="text"
                  id="driver_name"
                  name="driver_name"
                  value={formData.driver_name}
                  onChange={handleInputChange}
                  placeholder="e.g., John Doe"
                />
              </div>
            </div>

            <button type="submit" className="plan-button" disabled={loading}>
              {loading ? 'Planning Trip...' : 'Plan Trip'}
            </button>
          </form>
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Calculating route and generating ELD logs...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && (
          <>
            <div className="results-section">
              <h2 className="section-title">
                <span className="icon">📊</span>
                Trip Summary
              </h2>
              <div className="summary-grid">
                <div className="summary-card">
                  <h3>{results.summary.total_distance_miles}</h3>
                  <p>Total Miles</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.total_driving_hours}</h3>
                  <p>Driving Hours</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.total_trip_hours}</h3>
                  <p>Total Trip Hours</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.total_trip_days}</h3>
                  <p>Trip Days</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.number_of_rest_stops}</h3>
                  <p>Rest Stops</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.number_of_fuel_stops}</h3>
                  <p>Fuel Stops</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.cycle_hours_remaining}</h3>
                  <p>Cycle Hours Remaining</p>
                </div>
                <div className="summary-card">
                  <h3>{results.summary.hos_compliant ? '✓' : '✗'}</h3>
                  <p>HOS Compliant</p>
                </div>
              </div>
            </div>

            <div className="results-section">
              <h2 className="section-title">
                <span className="icon">🗺️</span>
                Route Map
              </h2>
              <RouteMap route={results.route} />
            </div>

            <div className="results-section">
              <h2 className="section-title">
                <span className="icon">📅</span>
                Trip Schedule
              </h2>
              <ScheduleTable schedule={results.schedule} />
            </div>

            <div className="results-section">
              <h2 className="section-title">
                <span className="icon">📋</span>
                ELD Daily Logs
              </h2>
              <ELDLogs logs={results.eld_logs} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
