// src/components/campaigns/CampaignForm.jsx
import React, { useState } from 'react';
import { useCampaigns } from '../hooks/useCampaigns';

const CreateCampaign = ({ initialData, onSuccess }) => {
  const [formData, setFormData] = useState(initialData || {
    name: '',
    message: '',
  });
  const [csvFile, setCsvFile] = useState(null);

  const { addCampaign, editCampaign } = useCampaigns();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('message', formData.message);
      if (csvFile) {
        formDataToSend.append('leads', csvFile);
      }

      if (initialData) {
        await editCampaign(initialData.id, formDataToSend);
      } else {
        await addCampaign(formDataToSend);
      }
      onSuccess();
    } catch (error) {
      console.error('Failed to save campaign:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setCsvFile(e.target.files[0]);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">Campaign Name</label>
        <input
          type="text"
          name="name"
          id="name"
          value={formData.name}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-medium text-gray-700">Message</label>
        <textarea
          name="message"
          id="message"
          value={formData.message}
          onChange={handleChange}
          rows="3"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        ></textarea>
      </div>
      <div>
        <label htmlFor="leads" className="block text-sm font-medium text-gray-700">Upload Leads (CSV)</label>
        <input
          type="file"
          name="leads"
          id="leads"
          accept=".csv"
          onChange={handleFileChange}
          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <button
        type="submit"
        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        {initialData ? 'Update Campaign' : 'Create Campaign'}
      </button>
    </form>
  );
};

export default CreateCampaign;