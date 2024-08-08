// src/pages/CampaignDetail.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function CampaignDetails() {
  const { id } = useParams();
  const [campaign, setCampaign] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchCampaignDetails();
    fetchCampaignStats();
  }, [id]);

  const fetchCampaignDetails = async () => {
    try {
      const response = await axios.get(`/api/campaigns/${id}`);
      setCampaign(response.data.campaign);
    } catch (error) {
      console.error('Error fetching campaign details:', error);
    }
  };

  const fetchCampaignStats = async () => {
    try {
      const response = await axios.get(`/api/campaigns/${id}/stats`);
      setStats(response.data.stats);
    } catch (error) {
      console.error('Error fetching campaign stats:', error);
    }
  };

  if (!campaign) return <div>Loading...</div>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">{campaign.name}</h2>
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <p><strong>Status:</strong> {campaign.status}</p>
        <p><strong>Platform:</strong> {campaign.platform}</p>
        <p><strong>Message Template:</strong> {campaign.messageTemplate}</p>
      </div>
      {stats && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-2">Campaign Stats</h3>
          <p><strong>Total Messages Sent:</strong> {stats.totalSent}</p>
          <p><strong>Responses Received:</strong> {stats.responsesReceived}</p>
          <p><strong>Open Rate:</strong> {stats.openRate}%</p>
          <p><strong>Response Rate:</strong> {stats.responseRate}%</p>
        </div>
      )}
    </div>
  );
}

export default CampaignDetails;