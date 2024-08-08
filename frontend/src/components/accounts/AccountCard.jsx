import React from 'react';

const AccountCard = ({ account }) => {
  return (
      <div className="bg-white shadow-md rounded-lg p-4">
            <h3 className="text-lg font-semibold">{account.username}</h3>
                  <p className="text-gray-600">Platform: {account.platform}</p>
                        <p className="text-gray-600">Proxy: {account.proxy}</p>
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

                                                                                              export default AccountCard;