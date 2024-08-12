'use client';

import { useState, useRef } from 'react';
import Papa from 'papaparse';

const Home: React.FC = () => {
  const [platform, setPlatform] = useState<string>('twitter');
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [recipient, setRecipient] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [status, setStatus] = useState<string>('');
  const [proxyUrl, setProxy] = useState<string>('');
  const [recipients, setRecipients] = useState<string[]>([]);
  const [inputMethod, setInputMethod] = useState<'direct' | 'csv'>('direct');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const targetsToMessage = inputMethod === 'direct' ? [recipient] : recipients;
    
    for (const currentRecipient of targetsToMessage) {
      try {
        const response = await fetch('/api/sendDm', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            platform, 
            username, 
            password, 
            recipient: currentRecipient, 
            message,
            proxyUrl 
          }),
        });
    
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || 'Failed to send message.');
        }
    
        const result = await response.json();
        setStatus(prevStatus => prevStatus + `\n${result.status || result.error}`);
      } catch (error) {
        setStatus(prevStatus => prevStatus + `\nFailed to send message to ${currentRecipient}. Error: ${error}`);
      }
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      Papa.parse(file, {
        complete: (results : any) => {
          const uploadedRecipients = results.data.flat().filter(Boolean);
          setRecipients(uploadedRecipients as string[]);
        },
        error: (error : any) => {
          console.error('Error parsing CSV:', error);
          setStatus('Error parsing CSV file');
        }
      });
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Send Social Media DM</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">Platform</label>
          <select 
            value={platform} 
            onChange={(e) => setPlatform(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="twitter">Twitter</option>
            <option value="instagram">Instagram</option>
          </select>
        </div>

        <div>
          <label className="block mb-1">Username</label>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block mb-1">Password</label>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block mb-1">Input Method</label>
          <select 
            value={inputMethod} 
            onChange={(e) => setInputMethod(e.target.value as 'direct' | 'csv')}
            className="w-full p-2 border rounded"
          >
            <option value="direct">Direct Input</option>
            <option value="csv">CSV Upload</option>
          </select>
        </div>

        {inputMethod === 'direct' ? (
          <div>
            <label className="block mb-1">Recipient Username</label>
            <input
              type="text"
              placeholder="Recipient Username"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              required
              className="w-full p-2 border rounded"
            />
          </div>
        ) : (
          <div>
            <label className="block mb-1">Upload CSV</label>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              ref={fileInputRef}
              className="w-full p-2 border rounded"
            />
            {recipients.length > 0 && (
              <p className="mt-2">{recipients.length} recipients loaded</p>
            )}
          </div>
        )}

        <div>
          <label className="block mb-1">Proxy URL (optional)</label>
          <input
            type="text"
            value={proxyUrl}
            onChange={(e) => setProxy(e.target.value)}
            placeholder="http://username:password@proxy-server:port"
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block mb-1">Message</label>
          <textarea
            placeholder="Message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
            className="w-full p-2 border rounded"
            rows={4}
          ></textarea>
        </div>

        <button 
          type="submit" 
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Send Message{inputMethod === 'csv' ? 's' : ''}
        </button>
      </form>
      {status && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="font-bold mb-2">Status:</h2>
          <pre className="whitespace-pre-wrap">{status}</pre>
        </div>
      )}
    </div>
  );
};

export default Home;
