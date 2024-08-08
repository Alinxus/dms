import React from 'react';
import AccountList from '../components/accounts/AccountList';
import AccountForm from '../components/accounts/AccountForm';

const Accounts = () => {
  return (
      <div className="container mx-auto px-4">
            <h1 className="text-2xl font-bold mb-4">Manage Accounts</h1>
                  <AccountForm />
                        <AccountList />
                            </div>
                              );
                              };

                              export default Accounts;