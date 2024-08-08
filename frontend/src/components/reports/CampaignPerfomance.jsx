import React from 'react';
import {useCampaigns} from '../../hooks/useCampaigns';
import { Bar } from 'react-chartjs-2';

const CampaignPerformance = () => {
  const { campaigns, isLoading, error } = useCampaigns();

    if (isLoading) return <div>Loading campaign performance...</div>;
      if (error) return <div>Error: {error.message}</div>;

        const data = {
            labels: campaigns.map(c => c.name),
                datasets: [
                      {
                              label: 'Messages Sent',
                                      data: campaigns.map(c => c.messagesSent),
                                              backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                                    },
                                                          {
                                                                  label: 'Responses Received',
                                                                          data: campaigns.map(c => c.responsesReceived),
                                                                                  backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                                                                        },
                                                                                            ],
                                                                                              };

                                                                                                return (
                                                                                                    <div className="bg-white shadow rounded-lg p-6">
                                                                                                          <h2 className="text-xl font-semibold mb-4">Campaign Performance</h2>
                                                                                                                <Bar data={data} />
                                                                                                                    </div>
                                                                                                                      );
                                                                                                                      };

                                                                                                                      export default CampaignPerformance;