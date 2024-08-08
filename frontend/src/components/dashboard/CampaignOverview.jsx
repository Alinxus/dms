import React from 'react';
import {useCampaigns} from '../../hooks/useCampaigns';

const CampaignOverview = () => {
  const { campaigns, isLoading, error } = useCampaigns();

    if (isLoading) return <div>Loading campaigns...</div>;
      if (error) return <div>Error: {error.message}</div>;

        const activeCampaigns = campaigns.filter(c => c.status === 'active');
          const totalMessages = campaigns.reduce((sum, c) => sum + c.messagesSent, 0);

            return (
                <div className="bg-white shadow rounded-lg p-6">
                      <h2 className="text-xl font-semibold mb-4">Campaign Overview</h2>
                            <div className="grid grid-cols-2 gap-4">
                                    <div>
                                              <p className="text-gray-600">Active Campaigns</p>
                                                        <p className="text-2xl font-bold">{activeCampaigns.length}</p>
                                                                </div>
                                                                        <div>
                                                                                  <p className="text-gray-600">Total Messages Sent</p>
                                                                                            <p className="text-2xl font-bold">{totalMessages}</p>
                                                                                                    </div>
                                                                                                          </div>
                                                                                                              </div>
                                                                                                                );
                                                                                                                };

                                                                                                                export default CampaignOverview;