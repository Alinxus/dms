// src/hooks/useReports.js
import { useState, useEffect } from 'react';

const mockReportData = {
  campaignPerformance: [
    { id: 1, name: 'Campaign 1', messagesSent: 100, responses: 20 },
    { id: 2, name: 'Campaign 2', messagesSent: 150, responses: 30 },
  ],
  accountPerformance: [
    { id: 1, name: 'Account 1', messagesSent: 75, responses: 15 },
    { id: 2, name: 'Account 2', messagesSent: 125, responses: 25 },
  ],
  overallStats: {
    totalMessagesSent: 250,
    totalResponses: 50,
    conversionRate: '20%',
  },
};

export const useReports = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulating API call
    setTimeout(() => {
      setReportData(mockReportData);
      setLoading(false);
    }, 1000);
  }, []);

  return { reportData, loading, error };
};