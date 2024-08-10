'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@clerk/nextjs'

type UserSettings = {
  sendFrequency: number
  maxDailyMessages: number
}

export default function Settings() {
  const { isSignedIn, user } = useUser()
  const [settings, setSettings] = useState<UserSettings>({
    sendFrequency: 60,
    maxDailyMessages: 50,
  })

  useEffect(() => {
    if (isSignedIn && user) {
      fetchSettings()
    }
  }, [isSignedIn, user])

  const fetchSettings = async () => {
    try {
      const response = await fetch(`/api/settings?userId=${user?.id}`)
      if (response.ok) {
        const data = await response.json()
        setSettings(data.settings)
      } else {
        throw new Error('Failed to fetch settings')
      }
    } catch (error) {
      console.error('Error fetching settings:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId: user?.id,
          ...settings,
        }),
      })
      if (response.ok) {
        alert('Settings updated successfully')
      } else {
        throw new Error('Failed to update settings')
      }
    } catch (error) {
      console.error('Error updating settings:', error)
      alert('Failed to update settings')
    }
  }

  if (!isSignedIn) {
    return <h1 className="text-3xl font-bold mb-4">Please sign in to view settings</h1>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">User Settings</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="sendFrequency" className="block mb-2">Send Frequency (minutes)</label>
          <input
            type="number"
            id="sendFrequency"
            value={settings.sendFrequency}
            onChange={(e) => setSettings({ ...settings, sendFrequency: parseInt(e.target.value) })}
            className="w-full p-2 border rounded"
            min="1"
            required
          />
        </div>
        <div>
          <label htmlFor="maxDailyMessages" className="block mb-2">Max Daily Messages</label>
          <input
            type="number"
            id="maxDailyMessages"
            value={settings.maxDailyMessages}
            onChange={(e) => setSettings({ ...settings, maxDailyMessages: parseInt(e.target.value) })}
            className="w-full p-2 border rounded"
            min="1"
            required
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Save Settings
        </button>
      </form>
    </div>
  )
}