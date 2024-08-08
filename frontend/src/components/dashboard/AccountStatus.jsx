import React from 'react';
import useAccounts from '../../hooks/useAccounts';

const AccountStatus = () => {
  const { accounts, isLoading, error } = useAccounts();

    if (isLoading) return <div>Loading accounts...</div>;
      if (error) return <div>Error: {error.message}</div>;

        const activeAccounts = accounts.filter(a => a.status === 'active');

          return (
              <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-xl font-semibold mb-4">Account Status</h2>
                          <div>
                                  <p className="text-gray-600">Active Accounts</p>
                                          <p className="text-2xl font-bold">{activeAccounts.length} / {accounts.length}</p>
                                                </div>
                                                      <div className="mt-4">
                                                              <p className="text-gray-600">Accounts by Platform</p>
                                                                      {Object.entries(
                                                                                accounts.reduce((acc, account) => {
                                                                                            acc[account.platform] = (acc[account.platform] || 0) + 1;
                                                                                                        return acc;
                                                                                                                  }, {})
                                                                                                                          ).map(([platform, count]) => (
                                                                                                                                    <div key={platform} className="flex justify-between items-center mt-2">
                                                                                                                                                <span>{platform}</span>
                                                                                                                                                            <span className="font-semibold">{count}</span>
                                                                                                                                                                      </div>
                                                                                                                                                                              ))}
                                                                                                                                                                                    </div>
                                                                                                                                                                                        </div>
                                                                                                                                                                                          );
                                                                                                                                                                                          };

                                                                                                                                                                                          export default AccountStatus;