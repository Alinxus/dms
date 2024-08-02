// src/pages/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [campaigns, setCampaigns] = useState([]);

  useEffect(() => {
    fetchAccounts();
    fetchCampaigns();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await axios.get('/api/accounts');
      setAccounts(response.data.accounts);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const fetchCampaigns = async () => {
    try {
      const response = await axios.get('/api/campaigns');
      setCampaigns(response.data.campaigns);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h3 className="text-xl font-semibold mb-2">Connected Accounts</h3>
          {accounts.length > 0 ? (
            <ul className="bg-white shadow rounded-lg divide-y">
              {accounts.map((account) => (
                <li key={account.id} className="px-4 py-3">
                  {account.platform}: {account.username}
                </li>
              ))}
            </ul>
          ) : (
            <p>No accounts connected yet.</p>
          )}
          <Link to="/add-account" className="mt-4 inline-block bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
            Add Account
          </Link>
        </div>
        <div>
          <h3 className="text-xl font-semibold mb-2">Campaigns</h3>
          {campaigns.length > 0 ? (
            <ul className="bg-white shadow rounded-lg divide-y">
              {campaigns.map((campaign) => (
                <li key={campaign.id} className="px-4 py-3">
                  {campaign.name} - {campaign.status}
                </li>
              ))}
            </ul>
          ) : (
            <p>No campaigns created yet.</p>
          )}
          <Link to="/create-campaign" className="mt-4 inline-block bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded">
            Create Campaign
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;