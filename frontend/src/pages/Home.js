// src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold mb-4">Welcome to Mass DM Sender</h1>
      <p className="text-xl mb-8">Send personalized messages across multiple platforms</p>
      <Link to="/register" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
        Get Started
      </Link>
    </div>
  );
}

export default Home;