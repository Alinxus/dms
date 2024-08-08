// src/components/sessions/SessionForm.jsx
import React, { useState } from 'react';
import useAccounts from '../../hooks/useAccounts';

const SessionForm = () => {
  const [proxy, setProxy] = useState('');
    const [selectedAccounts, setSelectedAccounts] = useState([]);
      const { accounts } = useAccounts();

        const handleSubmit = (e) => {
            e.preventDefault();
                // Submit session data to backend
                    console.log('Creating session with:', { proxy, selectedAccounts });
                      };

                        return (
                            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                                  <div className="mb-4">
                                          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="proxy">
                                                    Proxy
                                                            </label>
                                                                    <input
                                                                              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                                                                        id="proxy"
                                                                                                  type="text"
                                                                                                            value={proxy}
                                                                                                                      onChange={(e) => setProxy(e.target.value)}
                                                                                                                                placeholder="http://proxy.example.com:8080"
                                                                                                                                        />
                                                                                                                                              </div>
                                                                                                                                                    <div className="mb-4">
                                                                                                                                                            <label className="block text-gray-700 text-sm font-bold mb-2">
                                                                                                                                                                      Select Accounts
                                                                                                                                                                              </label>
                                                                                                                                                                                      {accounts.map(account => (
                                                                                                                                                                                                <label key={account.id} className="inline-flex items-center mt-3">
                                                                                                                                                                                                            <input
                                                                                                                                                                                                                          type="checkbox"
                                                                                                                                                                                                                                        className="form-checkbox h-5 w-5 text-gray-600"
                                                                                                                                                                                                                                                      checked={selectedAccounts.includes(account.id)}
                                                                                                                                                                                                                                                                    onChange={() => {
                                                                                                                                                                                                                                                                                    setSelectedAccounts(prev =>
                                                                                                                                                                                                                                                                                                      prev.includes(account.id)
                                                                                                                                                                                                                                                                                                                          ? prev.filter(id => id !== account.id)
                                                                                                                                                                                                                                                                                                                                              : [...prev, account.id]
                                                                                                                                                                                                                                                                                                                                                              );
                                                                                                                                                                                                                                                                                                                                                                            }}
                                                                                                                                                                                                                                                                                                                                                                                        />
                                                                                                                                                                                                                                                                                                                                                                                                    <span className="ml-2 text-gray-700">{account.username} ({account.platform})</span>
                                                                                                                                                                                                                                                                                                                                                                                                              </label>
                                                                                                                                                                                                                                                                                                                                                                                                                      ))}
                                                                                                                                                                                                                                                                                                                                                                                                                            </div>
                                                                                                                                                                                                                                                                                                                                                                                                                                  <div className="flex items-center justify-between">
                                                                                                                                                                                                                                                                                                                                                                                                                                          <button
                                                                                                                                                                                                                                                                                                                                                                                                                                                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                                                                                                                                                                                                                                                                                                                                                                                                                                                              type="submit"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                      >
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Create Session
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        </button>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              </div>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  </form>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    );
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    };

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    export default SessionForm;