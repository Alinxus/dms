// src/contexts/AuthContext.js
import React, { createContext, useState, useContext } from 'react';
import { login, logout } from '../services/auth';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const loginUser = async (credentials) => {
    const response = await login(credentials);
    setUser(response.data.user);
    localStorage.setItem('token', response.data.token);
  };

  const logoutUser = () => {
    logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);