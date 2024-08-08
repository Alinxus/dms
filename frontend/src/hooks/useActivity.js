// src/hooks/useActivity.js
import { useState, useEffect } from 'react';
import api from '../services/api';

export const useActivity = (limit = 10) => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchActivities = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/activities?limit=${limit}`);
      setActivities(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch activities');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActivities();
  }, [limit]);

  const addActivity = async (activityData) => {
    try {
      const response = await api.post('/activities', activityData);
      setActivities(prevActivities => [response.data, ...prevActivities].slice(0, limit));
      return response.data;
    } catch (err) {
      setError('Failed to add activity');
      throw err;
    }
  };

  return { 
    activities, 
    loading, 
    error, 
    refetchActivities: fetchActivities,
    addActivity
  };
};