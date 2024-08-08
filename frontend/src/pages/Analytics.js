// src/pages/Analytics.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

function Analytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const response = await axios.get('/api/analytics');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    }
  };

  if (!data) return <div>Loading...</div>;

  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: 'Messages Sent',
        data: data.messagesSent,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      },
      {
        label: 'Responses Received',
        data: data.responsesReceived,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1
      }
    ]
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Analytics</h2>
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h3 className="text-xl font-semibold mb-2">Overall Stats</h3>
        <p><strong>Total Campaigns:</strong> {data.totalCampaigns}</p>
        <p><strong>Total Messages Sent:</strong> {data.totalMessagesSent}</p>
        <p><strong>Total Responses:</strong> {data.totalResponses}</p>
        <p><strong>Average Response Rate:</strong> {data.averageResponseRate}%</p>
      </div>
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-2">Messages and Responses Over Time</h3>
        <Line data={chartData} />
      </div>
    </div>
  );
}

export default Analytics;