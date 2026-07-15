import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [edaResults, setEdaResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = 'http://localhost:5000/api';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [pricesRes, eventsRes, changePointRes, edaRes] = await Promise.all([
        axios.get(`${API_BASE}/prices`),
        axios.get(`${API_BASE}/events`),
        axios.get(`${API_BASE}/change-point`),
        axios.get(`${API_BASE}/analysis/eda`)
      ]);

      setPriceData(pricesRes.data.data);
      setEvents(eventsRes.data.events);
      setChangePoint(changePointRes.data.results);
      setEdaResults(edaRes.data.eda_results);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data from API. Make sure the Flask backend is running.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">Loading dashboard data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={fetchData} className="retry-button">Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Brent Oil Price Analysis Dashboard</h1>
        <p>Change Point Detection and Event Correlation Analysis</p>
      </header>

      <main className="dashboard">
        {/* Summary Cards */}
        <section className="summary-section">
          <div className="summary-card">
            <h3>Price Summary</h3>
            {edaResults && (
              <div className="summary-content">
                <p><strong>Mean:</strong> ${edaResults.price_statistics.mean.toFixed(2)}</p>
                <p><strong>Median:</strong> ${edaResults.price_statistics.median.toFixed(2)}</p>
                <p><strong>Std Dev:</strong> ${edaResults.price_statistics.std.toFixed(2)}</p>
                <p><strong>Range:</strong> ${edaResults.price_statistics.min.toFixed(2)} - ${edaResults.price_statistics.max.toFixed(2)}</p>
              </div>
            )}
          </div>

          <div className="summary-card">
            <h3>Change Point Analysis</h3>
            {changePoint && (
              <div className="summary-content">
                <p><strong>Date:</strong> {changePoint.change_point_date}</p>
                <p><strong>Mean Before:</strong> ${changePoint.mean_before.toFixed(2)}</p>
                <p><strong>Mean After:</strong> ${changePoint.mean_after.toFixed(2)}</p>
                <p><strong>Change:</strong> ${changePoint.price_change.toFixed(2)} ({changePoint.percentage_change.toFixed(1)}%)</p>
              </div>
            )}
          </div>

          <div className="summary-card">
            <h3>Data Coverage</h3>
            {edaResults && (
              <div className="summary-content">
                <p><strong>Period:</strong> {edaResults.data_period.start} to {edaResults.data_period.end}</p>
                <p><strong>Observations:</strong> {edaResults.data_period.observations.toLocaleString()}</p>
                <p><strong>Events:</strong> {events.length}</p>
              </div>
            )}
          </div>
        </section>

        {/* Events Table */}
        <section className="events-section">
          <h2>Key Events Database</h2>
          <div className="table-container">
            <table className="events-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Event Description</th>
                  <th>Type</th>
                  <th>Expected Impact</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event, index) => (
                  <tr key={index}>
                    <td>{event.date}</td>
                    <td>{event.event_description}</td>
                    <td>{event.event_type}</td>
                    <td className={event.expected_impact === 'Positive' ? 'positive' : 'negative'}>
                      {event.expected_impact}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Analysis Notes */}
        <section className="notes-section">
          <h2>Analysis Notes</h2>
          <div className="notes-content">
            <h3>Change Point Detection</h3>
            <p>The Bayesian change point model identified a significant structural break on {changePoint?.change_point_date}. 
            This represents a {changePoint?.percentage_change.toFixed(1)}% increase in the mean price level, suggesting 
            a fundamental shift in oil market dynamics during this period.</p>
            
            <h3>Event Correlation</h3>
            <p>The analysis examined {events.length} major geopolitical and economic events. The detected change point 
            does not directly correspond to any single event in our database, suggesting that the structural change was 
            driven by broader market factors such as increased global demand (particularly from China), market speculation, 
            and long-term supply dynamics.</p>
            
            <h3>Methodology</h3>
            <p>This analysis used Bayesian change point detection with PyMC, providing full posterior distributions 
            for all parameters and quantifying uncertainty in the estimates. The model achieved excellent convergence 
            (R-hat = 1.00), indicating reliable results.</p>
          </div>
        </section>
      </main>

      <footer className="App-footer">
        <p>Brent Oil Price Change Point Analysis | 10 Academy - KAIM 9 - Week 10</p>
      </footer>
    </div>
  );
}

export default App;