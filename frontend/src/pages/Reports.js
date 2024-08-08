import React from 'react';
import CampaignPerformance from '../components/reports/CampaignPerfomance';
import AccountPerformance from '../components/reports/AccountPerformance';
import MessageStats from '../components/reports/MessageStats';

const Reports = () => {
  return (
      <div className="container mx-auto px-4">
            <h1 className="text-3xl font-bold mb-6">Reports</h1>
                  <div className="space-y-8">
                          <CampaignPerformance />
                                  <AccountPerformance />
                                          <MessageStats />
                                                </div>
                                                    </div>
                                                      );
                                                      };

                                                      export default Reports;