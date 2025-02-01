import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import FactCheckPage from './components/FactCheckPage';
import InnovationNewsPage from './components/InnovationNewsPage';
import RegisterPage from './components/RegisterPage';
import LoginPage from './components/LoginPage';
import ProgressTracking from './components/ProgressTracking';
import Navbar from './components/Navbar';
import './App.css';
import ComingSoon from './components/ComingSoon';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/fact-check" element={<FactCheckPage />} />
        <Route path="/innovation-news" element={<InnovationNewsPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/coming-soon" element={<ComingSoon />} />
        <Route path="/progress-tracking" element={<ProgressTracking />} />
      </Routes>
    </Router>
  );
}

export default App;