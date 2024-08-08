// src/components/sessions/SessionCard.jsx
import React from 'react';

const SessionCard = ({ session }) => {
  return (
      <div className="bg-white shadow-md rounded-lg p-4">
            <h3 className="text-lg font-semibold">Session {session.id}</h3>
                  <p className="text-gray-600">Proxy: {session.proxy}</p>
                        <p className="text-gray-600">User Agent: {session.userAgent}</p>
                              <h4 className="mt-2 font-medium">Connected Accounts:</h4>
                                    <ul className="list-disc list-inside">
                                            {session.accounts.map(account => (
                                                      <li key={account.id}>{account.username} ({account.platform})</li>
                                                              ))}
                                                                    </ul>
                                                                          <div className="mt-4">
                                                                                  <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                                                                                            Edit
                                                                                                    </button>
                                                                                                            <button className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 ml-2">
                                                                                                                      Delete
                                                                                                                              </button>
                                                                                                                                    </div>
                                                                                                                                        </div>
                                                                                                                                          );
                                                                                                                                          };

                                                                                                                                          export default SessionCard;