// src/services/reports.js
import api from './api';

export const getOverviewStats = () => api.get('/reports/overview');
export const getCampaignPerformance = (id) => api.get(`/reports/campaigns/${id}`);
export const getAccountPerformance = (id) => api.get(`/reports/accounts/${id}`);