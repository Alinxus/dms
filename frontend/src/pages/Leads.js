// src/pages/LeadsList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function LeadsList() {
  const [leads, setLeads] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchLeads();
  }, [currentPage]);

  const fetchLeads = async () => {
    try {
      const response = await axios.get(`/api/leads?page=${currentPage}`);
      setLeads(response.data.leads);
      setTotalPages(response.data.totalPages);
    } catch (error) {
      console.error('Error fetching leads:', error);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Leads</h2>
      {leads.length > 0 ? (
        <>
          <table className="w-full bg-white shadow rounded-lg">
            <thead>
              <tr className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                <th className="py-3 px-6 text-left">Name</th>
                <th className="py-3 px-6 text-left">Platform</th>
                <th className="py-3 px-6 text-left">Status</th>
              </tr>
            </thead>
            <tbody className="text-gray-600 text-sm font-light">
              {leads.map((lead) => (
                <tr key={lead.id} className="border-b border-gray-200 hover:bg-gray-100">
                  <td className="py-3 px-6 text-left">{lead.name}</td>
                  <td className="py-3 px-6 text-left">{lead.platform}</td>
                  <td className="py-3 px-6 text-left">{lead.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-4 flex justify-between">
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
            >
              Previous
            </button>
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      ) : (
        <p>No leads found.</p>
      )}
    </div>
  );
}

export default LeadsList;