// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-xl font-bold text-gray-800">Mass DM Sender</Link>
          <div className="flex items-center">
            {user ? (
              <>
                <Link to="/dashboard" className="mx-2 text-gray-600 hover:text-gray-800">Dashboard</Link>
                <button onClick={logout} className="mx-2 text-gray-600 hover:text-gray-800">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="mx-2 text-gray-600 hover:text-gray-800">Login</Link>
                <Link to="/register" className="mx-2 text-gray-600 hover:text-gray-800">Register</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;