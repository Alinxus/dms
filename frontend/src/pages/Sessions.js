// src/pages/Sessions.jsx
import React from 'react';
import SessionList from '../components/sessions/SessionList';
import SessionForm from '../components/sessions/SessionForm';

const Sessions = () => {
  return (
      <div className="container mx-auto px-4">
            <h1 className="text-2xl font-bold mb-4">Manage Sessions</h1>
                  <SessionForm />
                        <SessionList />
                            </div>
                              );
                              };

                              export default Sessions;