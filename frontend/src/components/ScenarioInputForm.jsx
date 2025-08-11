import React, { useState } from 'react';
import axios from 'axios';

export default function ScenarioInputForm({ onResult }) {
  const [scenario, setScenario] = useState('');
  const [reference, setReference] = useState('');
  const [additional, setAdditional] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      const res = await axios.post('/api/evaluate', {
        scenario_text: scenario,
        reference_decision: reference,
        additional_data: additional ? JSON.parse(additional) : null
      }, { headers: { Authorization: `Bearer ${token}` } });
      onResult(res.data);
    } catch (err) {
      setError('Error submitting scenario');
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Submit Scenario</h2>
      <textarea placeholder="Scenario text" value={scenario} onChange={e => setScenario(e.target.value)} required />
      <input placeholder="Reference decision (A/B, optional)" value={reference} onChange={e => setReference(e.target.value)} />
      <textarea placeholder="Additional data (JSON, optional)" value={additional} onChange={e => setAdditional(e.target.value)} />
      <button type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Submit'}</button>
      {error && <div style={{color:'red'}}>{error}</div>}
    </form>
  );
}
