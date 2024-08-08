// src/hooks/useCampaigns.js
import { useState, useEffect, useCallback } from 'react';
import { 
  getCampaigns, 
  createCampaign, 
  updateCampaign, 
  deleteCampaign,
  startCampaign,
  stopCampaign
} from '../services/campaigns';

export const useCampaigns = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCampaigns = useCallback(async () => {
    try {
      setLoading(true);
      const response = await getCampaigns();
      setCampaigns(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch campaigns');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCampaigns();
  }, [fetchCampaigns]);

  const addCampaign = async (campaignData) => {
    try {
      const response = await createCampaign(campaignData);
      setCampaigns(prevCampaigns => [...prevCampaigns, response.data]);
      return response.data;
    } catch (err) {
      setError('Failed to create campaign');
      throw err;
    }
  };
  
  const editCampaign = async (id, campaignData) => {
    try {
      const response = await updateCampaign(id, campaignData);
      setCampaigns(prevCampaigns => 
        prevCampaigns.map(campaign => 
          campaign.id === id ? response.data : campaign
        )
      );
      return response.data;
    } catch (err) {
      setError('Failed to update campaign');
      throw err;
    }
  };
  const removeCampaign = async (id) => {
    try {
      await deleteCampaign(id);
      setCampaigns(prevCampaigns => 
        prevCampaigns.filter(campaign => campaign.id !== id)
      );
    } catch (err) {
      setError('Failed to delete campaign');
      throw err;
    }
  };

  const start = async (id) => {
    try {
      const response = await startCampaign(id);
      setCampaigns(prevCampaigns => 
        prevCampaigns.map(campaign => 
          campaign.id === id ? { ...campaign, status: 'running' } : campaign
        )
      );
      return response.data;
    } catch (err) {
      setError('Failed to start campaign');
      throw err;
    }
  };

  const stop = async (id) => {
    try {
      const response = await stopCampaign(id);
      setCampaigns(prevCampaigns => 
        prevCampaigns.map(campaign => 
          campaign.id === id ? { ...campaign, status: 'stopped' } : campaign
        )
      );
      return response.data;
    } catch (err) {
      setError('Failed to stop campaign');
      throw err;
    }
  };

  return {
    campaigns,
    loading,
    error,
    fetchCampaigns,
    addCampaign,
    editCampaign,
    removeCampaign,
    startCampaign: start,
    stopCampaign: stop
  };
};