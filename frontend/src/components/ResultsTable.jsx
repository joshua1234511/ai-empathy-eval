import React from 'react';

export default function ResultsTable({ results }) {
  if (!results || results.length === 0) return null;
  return (
    <table border="1" cellPadding={6} style={{marginTop:20}}>
      <thead>
        <tr>
          <th>Model</th>
          <th>Decision</th>
          <th>Rationale</th>
          <th>Accuracy</th>
        </tr>
      </thead>
      <tbody>
        {results.map(r => (
          <tr key={r.model}>
            <td>{r.model}</td>
            <td>{r.decision}</td>
            <td>{r.rationale}</td>
            <td>{r.accuracy !== undefined ? r.accuracy : ''}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
