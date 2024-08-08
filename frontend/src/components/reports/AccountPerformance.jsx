import React from 'react';
import useAccounts from '../../hooks/useAccounts';
import { Pie } from 'react-chartjs-2';

const AccountPerformance = () => {
  const { accounts, isLoading, error } = useAccounts();

    if (isLoading) return <div>Loading account performance...</div>;
      if (error) return <div>Error: {error.message}</div>;

        const data = {
            labels: accounts.map(a => a.username),
                datasets: [
                      {
                              data: accounts.map(a => a.messagesSent),
                                      backgroundColor: [
                                                '#FF6384',
                                                          '#36A2EB',
                                                                    '#FFCE56',
                                                                              '#4BC0C0',
                                                                                        '#9966FF',
                                                                                                  '#FF9F40',
                                                                                                          ],
                                                                                                                },
                                                                                                                    ],
                                                                                                                      };

                                                                                                                        return (
                                                                                                                            <div className="bg-white shadow rounded-lg p-6">
                                                                                                                                  <h2 className="text-xl font-semibold mb-4">Account Performance</h2>
                                                                                                                                        <Pie data={data} />
                                                                                                                                            </div>
                                                                                                                                              );
                                                                                                                                              };

                                                                                                                                              export default AccountPerformance;