import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import ScenarioInputForm from './components/ScenarioInputForm';
import ResultsTable from './components/ResultsTable';
import HumanRatingUI from './components/HumanRatingUI';

function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'));
  const [result, setResult] = useState(null);
  const [rated, setRated] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    setLoggedIn(false);
    setResult(null);
    setRated(false);
  };

  if (!loggedIn) {
    return <LoginForm onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div style={{maxWidth:700, margin:'auto', padding:20}}>
      <button onClick={handleLogout} style={{float:'right'}}>Logout</button>
      <h1>AI Empathy Eval</h1>
      <ScenarioInputForm onResult={setResult} />
      {result && <ResultsTable results={result.results} />}
      {result && !rated && <HumanRatingUI scenarioId={result.scenario_id} results={result.results} onRated={() => setRated(true)} />}
      {rated && <div>Ratings submitted. Thank you!</div>}
    </div>
  );
}

export default App;
