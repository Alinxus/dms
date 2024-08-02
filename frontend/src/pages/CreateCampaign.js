// src/pages/CreateCampaign.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function CreateCampaign() {
  const [name, setName] = useState('');
  const [messageTemplate, setMessageTemplate] = useState('');
  const [selectedAccounts, setSelectedAccounts] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await axios.get('/api/accounts');
      setAccounts(response.data.accounts);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post('/api/campaigns', {
        name,
        message_template: messageTemplate,
        account_ids: selectedAccounts,
      });
      navigate('/dashboard');
    } catch (error) {
      setError('Failed to create campaign. Please try again.');
    }
  };

  const handleAccountSelection = (accountId) => {
    setSelectedAccounts((prevSelected) => {
      if (prevSelected.includes(accountId)) {
        return prevSelected.filter((id) => id !== accountId);
      } else {
        return [...prevSelected, accountId];
      }
    });
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Create Campaign</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block mb-2">Campaign Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="messageTemplate" className="block mb-2">Message Template</label>
          <textarea
            id="messageTemplate"
            value={messageTemplate}
            onChange={(e) => setMessageTemplate(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            rows="4"
            required
          ></textarea>
          <p className="text-sm text-gray-600 mt-1">Use {'{username}'} to personalize the message.</p>
        </div>
        <div className="mb-4">
          <label className="block mb-2">Select Accounts</label>
          <div className="space-y-2">
            {accounts.map((account) => (
              <label key={account.id} className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedAccounts.includes(account.id)}
                  onChange={() => handleAccountSelection(account.id)}
                  className="mr-2"
                />
                {account.platform}: {account.username}
              </label>
            ))}
          </div>
        </div>
        <button type="submit" className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded">
          Create Campaign
        </button>
      </form>
    </div>
  );
}

export default CreateCampaign;