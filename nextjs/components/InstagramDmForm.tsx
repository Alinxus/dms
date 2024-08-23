'use client';
import { useState } from 'react';
import { FaInstagram, FaPaperPlane, FaSpinner } from 'react-icons/fa';

interface FormData {
  cookies: string;
  messages: string;
  usernames: string;
  proxy: string;
}

interface Result {
  success: boolean;
  sentTo: string[];
  failed: string[];
  error?: any;
}

export default function InstagramDMForm() {
  const [formData, setFormData] = useState<FormData>({
    cookies: '',
    messages: '',
    usernames: '',
    proxy: '',
  });
  const [result, setResult] = useState<Result | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);

    try {
      const response = await fetch('/api/instagram', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          messages: formData.messages.split('\n'),
          usernames: formData.usernames.split('\n'),
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ success: false, sentTo: [], failed: [], error: 'An error occurred while sending DMs.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-2xl rounded-lg p-8 max-w-2xl mx-auto">
      <div className="flex items-center justify-center mb-6">
        <FaInstagram className="text-5xl text-pink-500 mr-4" />
        <h2 className="text-3xl font-bold text-gray-800">DM Sender</h2>
      </div>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="cookies" className="block text-sm font-medium text-gray-700">
            Cookies (JSON format)
          </label>
          <textarea
            id="cookies"
            name="cookies"
            rows={4}
            value={formData.cookies}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Paste your cookies JSON here"
            required
          />
        </div>
        <div>
          <label htmlFor="messages" className="block text-sm font-medium text-gray-700">
            Messages (one per line. as many as you want)
          </label>
          <textarea
            id="messages"
            name="messages"
            rows={4}
            value={formData.messages}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Enter your messages here, one per line"
            required
          />
        </div>
        <div>
          <label htmlFor="usernames" className="block text-sm font-medium text-gray-700">
            Usernames (one per line)
          </label>
          <textarea
            id="usernames"
            name="usernames"
            rows={4}
            value={formData.usernames}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Enter usernames here, one per line"
            required
          />
        </div>
        <div>
          <label htmlFor="proxy" className="block text-sm font-medium text-gray-700">
            Proxy (optional)
          </label>
          <input
            type="text"
            id="proxy"
            name="proxy"
            value={formData.proxy}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="http://user:pass@host:port"
          />
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? (
            <>
              <FaSpinner className="animate-spin mr-2" /> Sending...
            </>
          ) : (
            <>
              <FaPaperPlane className="mr-2" /> Send DMs
            </>
          )}
        </button>
      </form>
      {result && (
        <div className={`mt-6 p-4 rounded-md ${result.success ? 'bg-green-100' : 'bg-red-100'}`}>
          <h3 className={`text-lg font-medium ${result.success ? 'text-green-800' : 'text-red-800'}`}>
            {result.success ? 'DMs Sent Successfully' : 'Error Sending DMs'}
          </h3>
          {result.sentTo && result.sentTo.length > 0 && (
            <p className="mt-2 text-sm text-green-700">
              Sent to: {result.sentTo.join(', ')}
            </p>
          )}
          {result.failed && result.failed.length > 0 && (
            <p className="mt-2 text-sm text-red-700">
              Failed: {result.failed.join(', ')}
            </p>
          )}
          {result.error && (
            <p className="mt-2 text-sm text-red-700">
              Error: {result.error}
            </p>
          )}
        </div>
      )}
    </div>
  );
}