// src/services/campaigns.js
import api from './api';

export const getCampaigns = () => api.get('/campaigns');

export const createCampaign = (campaignData) => {
  return api.post('/campaigns', campaignData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const updateCampaign = (id, campaignData) => {
  return api.put(`/campaigns/${id}`, campaignData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const deleteCampaign = (id) => api.delete(`/campaigns/${id}`);
export const startCampaign = (id) => api.post(`/campaigns/${id}/start`);
export const stopCampaign = (id) => api.post(`/campaigns/${id}/stop`);