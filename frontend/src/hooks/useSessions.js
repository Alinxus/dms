// src/hooks/useSessions.js
import { useState, useEffect } from 'react';
import api from '../services/api';

export const useSessions = () => {
  const [sessions, setSessions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
      const [error, setError] = useState(null);

        useEffect(() => {
            const fetchSessions = async () => {
                  try {
                          const response = await api.get('/sessions');
                                  setSessions(response.data);
                                          setIsLoading(false);
                                                } catch (err) {
                                                        setError(err.message);
                                                                setIsLoading(false);
                                                                      }
                                                                          };

                                                                              fetchSessions();
                                                                                }, []);

                                                                                  return { sessions, isLoading, error };
                                                                                  };

                                                                                 