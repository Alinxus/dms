// src/components/campaigns/CampaignList.jsx
import React from 'react';
import { useCampaigns } from '../hooks/useCampaigns';
import CampaignItem from '../components/dashboard/CampaignItem';

const CampaignList = () => {
  const { 
    campaigns, 
    loading, 
    error, 
    removeCampaign, 
    startCampaign, 
    stopCampaign 
  } = useCampaigns();

  if (loading) return <div>Loading campaigns...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="space-y-4">
      {campaigns.map(campaign => (
        <CampaignItem 
          key={campaign.id} 
          campaign={campaign}
          onDelete={() => removeCampaign(campaign.id)}
          onStart={() => startCampaign(campaign.id)}
          onStop={() => stopCampaign(campaign.id)}
        />
      ))}
    </div>
  );
};

export default CampaignList;