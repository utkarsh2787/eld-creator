import React from 'react';

const ELDLogs = ({ logs }) => {
  if (!logs || logs.length === 0) {
    return <div>No ELD logs available</div>;
  }

  return (
    <div className="eld-logs-section">
      {logs.map((log, index) => (
        <div key={index} style={{ marginBottom: '30px' }}>
          <h3 style={{ color: '#667eea', marginBottom: '15px' }}>
            Day {index + 1} Log Sheet
          </h3>
          <img
            src={log}
            alt={`ELD Log Day ${index + 1}`}
            className="eld-log-image"
          />
        </div>
      ))}
    </div>
  );
};

export default ELDLogs;
