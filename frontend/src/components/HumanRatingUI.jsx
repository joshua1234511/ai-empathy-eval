import React, { useState } from 'react';
import axios from 'axios';

export default function HumanRatingUI({ scenarioId, results, onRated }) {
  const [ratings, setRatings] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [done, setDone] = useState(false);

  const handleChange = (model, field, value) => {
    setRatings(r => ({ ...r, [model]: { ...r[model], [field]: value } }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      await Promise.all(results.map(r => {
        const { empathy, explanation } = ratings[r.model] || {};
        if (!empathy || !explanation) return null;
        return axios.post('/api/rate', {
          scenario_id: scenarioId,
          model: r.model,
          empathy: Number(empathy),
          explanation: Number(explanation)
        }, { headers: { Authorization: `Bearer ${token}` } });
      }));
      setDone(true);
      if (onRated) onRated();
    } catch (err) {
      setError('Error submitting ratings');
    }
    setLoading(false);
  };

  if (done) return <div>Thank you for rating!</div>;

  return (
    <form onSubmit={handleSubmit}>
      <h3>Human Ratings</h3>
      {results.map(r => (
        <div key={r.model} style={{marginBottom:10}}>
          <b>{r.model}</b>
          <div>Empathy (1-5): <input type="number" min="1" max="5" value={ratings[r.model]?.empathy||''} onChange={e => handleChange(r.model, 'empathy', e.target.value)} required /></div>
          <div>Explanation (1-5): <input type="number" min="1" max="5" value={ratings[r.model]?.explanation||''} onChange={e => handleChange(r.model, 'explanation', e.target.value)} required /></div>
        </div>
      ))}
      <button type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Submit Ratings'}</button>
      {error && <div style={{color:'red'}}>{error}</div>}
    </form>
  );
}
