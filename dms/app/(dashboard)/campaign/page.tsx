import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import Layout from '../components/Layout';
import { sendInstagramDM } from '../lib/instagramAutomation';
import { sendTwitterDM } from '../lib/twitterAutomation';
import { sendLinkedInDM } from '../lib/linkedinAutomation';

const CampaignsPage = () => {
  const { isSignedIn, user } = useUser();
  const [platform, setPlatform] = useState('instagram');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [recipient, setRecipient] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isSignedIn) {
      alert('Please sign in to send messages');
      return;
    }
    
    switch (platform) {
      case 'instagram':
        await sendInstagramDM(username, password, recipient, message);
        break;
      case 'twitter':
        await sendTwitterDM(username, password, recipient, message);
        break;
      case 'linkedin':
        await sendLinkedInDM(username, password, recipient, message);
        break;
      default:
        alert('Invalid platform selected');
    }
  };

  if (!isSignedIn) {
    return (
      <Layout title="Campaigns | Mass DM Sender">
        <h1 className="text-3xl font-bold mb-4">Please sign in to create campaigns</h1>
      </Layout>
    );
  }

  return (
    <Layout title="Campaigns | Mass DM Sender">
      <h1 className="text-3xl font-bold mb-4">Create Campaign</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="platform" className="block">Platform</label>
          <select
            id="platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="w-full border p-2"
            required
          >
            <option value="instagram">Instagram</option>
            <option value="twitter">Twitter</option>
            <option value="linkedin">LinkedIn</option>
          </select>
        </div>
        <div>
          <label htmlFor="username" className="block">Username/Email</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full border p-2"
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="block">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2"
            required
          />
        </div>
        <div>
          <label htmlFor="recipient" className="block">Recipient</label>
          <input
            type="text"
            id="recipient"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            className="w-full border p-2"
            required
          />
        </div>
        <div>
          <label htmlFor="message" className="block">Message</label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full border p-2"
            required
          ></textarea>
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Send Message
        </button>
      </form>
    </Layout>
  );
};

export default CampaignsPage;