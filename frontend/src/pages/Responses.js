// src/pages/Responses.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Responses() {
  const [responses, setResponses] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchResponses();
  }, [currentPage]);

  const fetchResponses = async () => {
    try {
      const response = await axios.get(`/api/responses?page=${currentPage}`);
      setResponses(response.data.responses);
      setTotalPages(response.data.totalPages);
    } catch (error) {
      console.error('Error fetching responses:', error);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Responses</h2>
      {responses.length > 0 ? (
        <>
          <ul className="bg-white shadow rounded-lg divide-y">
            {responses.map((response) => (
              <li key={response.id} className="px-4 py-3">
                <p><strong>From:</strong> {response.from}</p>
                <p><strong>Campaign:</strong> {response.campaignName}</p>
                <p><strong>Message:</strong> {response.message}</p>
                <p><strong>Received:</strong> {new Date(response.receivedAt).toLocaleString()}</p>
              </li>
            ))}
          </ul>
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
        <p>No responses yet.</p>
      )}
    </div>
  );
}

export default Responses;