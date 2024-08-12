// app/campaigns/page.tsx
'use client'

import { useState } from 'react'
import { useUser } from '@clerk/nextjs'
import { createCampaign } from './campaignActions'

export default function Campaigns() {
  const { isSignedIn, user } = useUser()
  const [platform, setPlatform] = useState('twitter')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [recipient, setRecipient] = useState('')
  const [message, setMessage] = useState('')
  const [proxyUrl, setProxyUrl] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // if (!isSignedIn || !user) {
    //   alert('Please sign in to create campaigns')
    //   return
    // }

    try {
      // First, create the campaign in the database
      const campaign = await createCampaign({
        userId: user.id,
        platform,
        name: `${platform} campaign to ${recipient}`,
        status: 'pending'
      })

      // Then, send the DM using the API route
      const response = await fetch('/api/sendDm', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platform,
          username,
          password,
          recipient,
          message,
          proxyUrl,
        }),
      })

      if (response.ok) {
        alert('Campaign created and message sent successfully!')
        // Reset form or redirect user
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error)
      }
    } catch (error) {
      console.error('Error creating campaign:', error)
      alert('Failed to create campaign and send message')
    }
  }

  if (!isSignedIn) {
    return <h1 className="text-3xl font-bold mb-4">Please sign in to create campaigns</h1>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Create Campaign</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="platform" className="block mb-2">Platform</label>
          <select
            id="platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="twitter">Twitter</option>
            <option value="instagram">Instagram</option>
          </select>
        </div>
        <div>
          <label htmlFor="username" className="block mb-2">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="block mb-2">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <label htmlFor="recipient" className="block mb-2">Recipient</label>
          <input
            type="text"
            id="recipient"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <label htmlFor="message" className="block mb-2">Message</label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full p-2 border rounded"
            rows={4}
            required
          ></textarea>
        </div>
        {platform === 'instagram' && (
          <div>
            <label htmlFor="proxyUrl" className="block mb-2">Proxy URL</label>
            <input
              type="text"
              id="proxyUrl"
              value={proxyUrl}
              onChange={(e) => setProxyUrl(e.target.value)}
              className="w-full p-2 border rounded"
            />
          </div>
        )}
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Create Campaign and Send Message
        </button>
      </form>
    </div>
  )
}