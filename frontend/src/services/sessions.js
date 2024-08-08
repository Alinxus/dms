// src/services/sessions.js
import api from './api';

export const getSessions = () => api.get('/sessions');
export const createSession = (sessionData) => api.post('/sessions', sessionData);
export const updateSession = (id, sessionData) => api.put(`/sessions/${id}`, sessionData);
export const deleteSession = (id) => api.delete(`/sessions/${id}`);