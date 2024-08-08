import React from 'react';
import {useActivity} from '../../hooks/useActivity';

const RecentActivity = () => {
  const { activities, isLoading, error } = useActivity();

    if (isLoading) return <div>Loading recent activity...</div>;
      if (error) return <div>Error: {error.message}</div>;

        return (
            <div className="bg-white shadow rounded-lg p-6">
                  <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
                        <ul className="divide-y divide-gray-200">
                                {activities.slice(0, 5).map((activity, index) => (
                                          <li key={index} className="py-3">
                                                      <p className="text-sm">{activity.description}</p>
                                                                  <p className="text-xs text-gray-500">{new Date(activity.timestamp).toLocaleString()}</p>
                                                                            </li>
                                                                                    ))}
                                                                                          </ul>
                                                                                              </div>
                                                                                                );
                                                                                                };

                                                                                                export default RecentActivity;