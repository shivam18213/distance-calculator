
import React from 'react';
import './HistoryTable.css';

const HistoryTable = ({ queries }) => {
  return (
    <div className="history-view">
      <h2>Historical Queries</h2>
      <p className="history-subtitle">History of the user's queries.</p>

      <div className="history-table">
        <div className="table-header">
          <div>Source Address</div>
          <div>Destination Address</div>
          <div>Distance in Miles</div>
          <div>Distance in Kilometers</div>
        </div>
        <div className="table-body">
          {queries.length === 0 ? (
            <div className="empty-state">No queries yet</div>
          ) : (
            queries.map((query) => (
              <div key={query.id} className="table-row">
                <div>{query.source}</div>
                <div>{query.destination}</div>
                <div>{query.distance_miles} mi</div>
                <div>{query.distance_km} km</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default HistoryTable;
