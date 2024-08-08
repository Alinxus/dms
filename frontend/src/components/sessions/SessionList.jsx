// src/components/sessions/SessionList.jsx
import React from 'react';
import {useSessions} from '../../hooks/useSessions';
import SessionCard from './SessionCard';

const SessionList = () => {
  const { sessions, isLoading, error } = useSessions();

    if (isLoading) return <div>Loading sessions...</div>;
      if (error) return <div>Error: {error.message}</div>;

        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {sessions.map(session => (
                          <SessionCard key={session.id} session={session} />
                                ))}
                                    </div>
                                      );
                                      };

                                      export default SessionList;