import React from 'react';

const ScheduleTable = ({ schedule }) => {
  if (!schedule || schedule.length === 0) {
    return <div>No schedule data available</div>;
  }

  const getActivityBadgeClass = (activity) => {
    switch (activity) {
      case 'driving_to_pickup':
      case 'driving_to_dropoff':
        return 'activity-driving';
      case 'pickup':
      case 'dropoff':
        return 'activity-pickup';
      case 'required_rest':
        return 'activity-rest';
      case 'fuel_stop':
      case 'required_break':
        return 'activity-fuel';
      default:
        return '';
    }
  };

  const formatActivity = (activity) => {
    return activity
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const formatTime = (hours) => {
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    return `${h}h ${m}m`;
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="schedule-table">
        <thead>
          <tr>
            <th>Day</th>
            <th>Activity</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Duration</th>
            <th>Distance</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {schedule.map((segment, index) => (
            <tr key={index}>
              <td>{segment.day + 1}</td>
              <td>
                <span className={`activity-badge ${getActivityBadgeClass(segment.activity)}`}>
                  {formatActivity(segment.activity)}
                </span>
              </td>
              <td>{formatTime(segment.start_time)}</td>
              <td>{formatTime(segment.end_time)}</td>
              <td>{formatTime(segment.duration)}</td>
              <td>{segment.distance_covered.toFixed(1)} mi</td>
              <td>{formatActivity(segment.status)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScheduleTable;
