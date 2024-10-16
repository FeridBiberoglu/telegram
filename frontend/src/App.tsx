// import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './pages/LandingsPage';
import FilterPage from './pages/filterpage';
import TokensPage from './pages/TokensPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/filters" element={<FilterPage />} />
          <Route path="/tokens" element={<TokensPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;