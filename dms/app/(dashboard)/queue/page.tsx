'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@clerk/nextjs'

type QueuedMessage = {
  id: string
  platform: string
  recipient: string
  message: string
  status: string
  createdAt: string
}

export default function Queue() {
  const { isSignedIn, user } = useUser()
  const [messages, setMessages] = useState<QueuedMessage[]>([])

  useEffect(() => {
    if (isSignedIn && user) {
      fetchQueuedMessages()
    }
  }, [isSignedIn, user])

  const fetchQueuedMessages = async () => {
    try {
      const response = await fetch(`/api/queue?userId=${user?.id}`)
      if (response.ok) {
        const data = await response.json()
        setMessages(data.messages)
      } else {
        throw new Error('Failed to fetch queued messages')
      }
    } catch (error) {
      console.error('Error fetching queued messages:', error)
    }
  }

  const handleRetry = async (messageId: string) => {
    try {
      const response = await fetch(`/api/queue/${messageId}/retry`, { method: 'POST' })
      if (response.ok) {
        fetchQueuedMessages()
      } else {
        throw new Error('Failed to retry message')
      }
    } catch (error) {
      console.error('Error retrying message:', error)
    }
  }

  if (!isSignedIn) {
    return <h1 className="text-3xl font-bold mb-4">Please sign in to view the queue</h1>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Message Queue</h1>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">Platform</th>
            <th className="border p-2">Recipient</th>
            <th className="border p-2">Message</th>
            <th className="border p-2">Status</th>
            <th className="border p-2">Created At</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((message) => (
            <tr key={message.id} className="border">
              <td className="border p-2">{message.platform}</td>
              <td className="border p-2">{message.recipient}</td>
              <td className="border p-2">{message.message.substring(0, 50)}...</td>
              <td className="border p-2">{message.status}</td>
              <td className="border p-2">{new Date(message.createdAt).toLocaleString()}</td>
              <td className="border p-2">
                {message.status === 'failed' && (
                  <button
                    onClick={() => handleRetry(message.id)}
                    className="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
                  >
                    Retry
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}