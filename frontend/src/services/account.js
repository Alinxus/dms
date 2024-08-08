// src/services/accounts.js
import api from './api';

export const getAccounts = () => api.get('/accounts');
export const createAccount = (accountData) => api.post('/accounts', accountData);
export const updateAccount = (id, accountData) => api.put(`/accounts/${id}`, accountData);
export const deleteAccount = (id) => api.delete(`/accounts/${id}`);