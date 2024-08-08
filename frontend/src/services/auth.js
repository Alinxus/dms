// src/services/auth.js
import api from './api';

export const login = (credentials) => api.post('/login', credentials);
export const register = (userData) => api.post('/register', userData);
export const logout = () => {
  localStorage.removeItem('token');
  // Additional logout logic
};