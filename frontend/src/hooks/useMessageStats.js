// src/hooks/useMessageStats.js
import { useState, useEffect } from 'react';
import api from '../services/api';

export const useMessageStats = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await api.get('/message-stats');
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch message stats');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return { stats, loading, error, refetchStats: fetchStats };
};