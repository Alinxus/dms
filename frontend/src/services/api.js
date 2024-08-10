// src/services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api'  || 'https://cautious-orbit-9799vqqpxrcgpj-8000.app.github.dev/';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (email, password) => api.post('/login', { email, password });
export const register = (userData) => api.post('/register', userData);
export const getAccounts = () => api.get('/accounts');
export const addAccount = (accountData) => api.post('/accounts', accountData);
export const getCampaigns = () => api.get('/campaigns');
export const createCampaign = (campaignData) => api.post('/campaigns', campaignData);

export default api;