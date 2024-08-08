import { useState, useEffect } from 'react';
import { getAccounts } from '../services/api';

const useAccounts = () => {
  const [accounts, setAccounts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
      const [error, setError] = useState(null);

        useEffect(() => {
            const fetchAccounts = async () => {
                  try {
                          const data = await getAccounts();
                                  setAccounts(data);
                                          setIsLoading(false);
                                                } catch (err) {
                                                        setError(err);
                                                                setIsLoading(false);
                                                                      }
                                                                          };

                                                                              fetchAccounts();
                                                                                }, []);

                                                                                  return { accounts, isLoading, error };
                                                                                  };

                                                                                  export default useAccounts;