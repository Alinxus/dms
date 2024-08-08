import React from 'react';
import {useMessageStats} from '../../hooks/useMessageStats';

const MessageStats = () => {
  const { stats, isLoading, error } = useMessageStats();

    if (isLoading) return <div>Loading message stats...</div>;
      if (error) return <div>Error: {error.message}</div>;

        return (
            <div className="bg-white shadow rounded-lg p-6">
                  <h2 className="text-xl font-semibold mb-4">Message Statistics</h2>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div>
                                          <p className="text-gray-600">Total Sent</p>
                                                    <p className="text-2xl font-bold">{stats.totalSent}</p>
                                                            </div>
                                                                    <div>
                                                                              <p className="text-gray-600">Delivered</p>
                                                                                        <p className="text-2xl font-bold">{stats.delivered}</p>
                                                                                                </div>
                                                                                                        <div>
                                                                                                                  <p className="text-gray-600">Read</p>
                                                                                                                            <p className="text-2xl font-bold">{stats.read}</p>
                                                                                                                                    </div>
                                                                                                                                            <div>
                                                                                                                                                      <p className="text-gray-600">Responses</p>
                                                                                                                                                                <p className="text-2xl font-bold">{stats.responses}</p>
                                                                                                                                                                        </div>
                                                                                                                                                                              </div>
                                                                                                                                                                                  </div>
                                                                                                                                                                                    );
                                                                                                                                                                                    };

                                                                                                                                                                                    export default MessageStats;