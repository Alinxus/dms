// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AddAccount from './pages/AddAccount';
import CreateCampaign from './pages/CreateCampaign';

import CampaignsList from './pages/Campaigns'
import Analytics from './pages/Analytics'
import LeadsList from './pages/Leads'
import Accounts from './pages/Accounts';
import Campaigns from './pages/Campaigns';
import Reports from './pages/Reports';
import Sessions from './pages/Sessions';
import Responses from './pages/Responses'
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/add-account" element={<AddAccount />} />
              <Route path="/create-campaign" element={<CreateCampaign />} />
              <Route path="/campaigns" element={<CampaignsList />} />
              <Route path="/leads" element={<LeadsList />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/accounts" component={Accounts} />
                            <Route path="/campaigns" component={Campaigns} />
                                          <Route path="/reports" component={Reports} />
                                                        <Route path="/sessions" component={Sessions} />

            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
