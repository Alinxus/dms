// src/components/campaigns/CampaignItem.jsx
import React from 'react';
import {useCampaigns} from '../../hooks/useCampaigns';

const CampaignItem = ({ campaign }) => {
  const { startCampaign, stopCampaign, removeCampaign } = useCampaigns();

  const handleStart = async () => {
    try {
      await startCampaign(campaign.id);
    } catch (error) {
      console.error('Failed to start campaign:', error);
    }
  };

  const handleStop = async () => {
    try {
      await stopCampaign(campaign.id);
    } catch (error) {
      console.error('Failed to stop campaign:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this campaign?')) {
      try {
        await removeCampaign(campaign.id);
      } catch (error) {
        console.error('Failed to delete campaign:', error);
      }
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold">{campaign.name}</h3>
        <span className={`px-2 py-1 rounded-full text-sm ${
          campaign.status === 'active' ? 'bg-green-200 text-green-800' : 'bg-gray-200 text-gray-800'
        }`}>
          {campaign.status}
        </span>
      </div>
      <p className="text-gray-600 mb-4">{campaign.message}</p>
      <div className="mb-4">
        <p className="text-sm text-gray-500">Leads: {campaign.leadsCount}</p>
        <p className="text-sm text-gray-500">Messages Sent: {campaign.messagesSent}</p>
        <p className="text-sm text-gray-500">Responses: {campaign.responses}</p>
      </div>
      <div className="flex space-x-2">
        {campaign.status !== 'active' && (
          <button
            onClick={handleStart}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
          >
            Start
          </button>
        )}
        {campaign.status === 'active' && (
          <button
            onClick={handleStop}
            className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded"
          >
            Stop
          </button>
        )}
        <button
          onClick={() => {/* Implement edit functionality */}}
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default CampaignItem;