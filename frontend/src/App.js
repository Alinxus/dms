// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AddAccount from './pages/AddAccount';
import CreateCampaign from './pages/CreateCampaign';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Switch>
              <Route exact path="/" component={Home} />
              <Route path="/login" component={Login} />
              <Route path="/register" component={Register} />
              <Route path="/dashboard" component={Dashboard} />
              <Route path="/add-account" component={AddAccount} />
              <Route path="/create-campaign" component={CreateCampaign} />
            </Switch>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;