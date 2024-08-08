import React from 'react';
import AccountCard from './AccountCard';
import useAccounts from '../../hooks/useAccounts';

const AccountList = () => {
  const { accounts, isLoading, error } = useAccounts();

    if (isLoading) return <div>Loading accounts...</div>;
      if (error) return <div>Error: {error.message}</div>;

        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {accounts.map(account => (
                          <AccountCard key={account.id} account={account} />
                                ))}
                                    </div>
                                      );
                                      };

                                      export default AccountList;