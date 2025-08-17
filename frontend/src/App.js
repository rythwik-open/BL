import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Components
import Dashboard from './components/Dashboard';
import ReviewQueue from './components/ReviewQueue';
import Analytics from './components/Analytics';
import ContentCalendar from './components/ContentCalendar';
import Navigation from './components/Navigation';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/review" element={<ReviewQueue />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/calendar" element={<ContentCalendar />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;