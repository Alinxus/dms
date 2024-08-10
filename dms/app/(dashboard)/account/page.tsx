'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@clerk/nextjs'

type Account = {
  id: string
  platform: string
  username: string
}

export default function Accounts() {
  const { isSignedIn, user } = useUser()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [platform, setPlatform] = useState('instagram')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  useEffect(() => {
    if (isSignedIn && user) {
      fetchAccounts()
    }
  }, [isSignedIn, user])

  const fetchAccounts = async () => {
    try {
      const response = await fetch(`/api/account?userId=${user?.id}`)
      if (response.ok) {
        const data = await response.json()
        setAccounts(data.accounts)
      } else {
        throw new Error('Failed to fetch accounts')
      }
    } catch (error) {
      console.error('Error fetching accounts:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!isSignedIn || !user) {
      alert('Please sign in to add accounts')
      return
    }

    try {
      const response = await fetch('/api/account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId: user.id,
          platform,
          username,
          password,
        }),
      })

      if (response.ok) {
        alert('Account added successfully')
        setPlatform('instagram')
        setUsername('')
        setPassword('')
        fetchAccounts()
      } else {
        throw new Error('Failed to add account')
      }
    } catch (error) {
      console.error('Error adding account:', error)
      alert('Failed to add account')
    }
  }

  if (!isSignedIn) {
    return <h1 className="text-3xl font-bold mb-4">Please sign in to manage accounts</h1>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Manage Accounts</h1>
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div>
          <label htmlFor="platform" className="block mb-2">Platform</label>
          <select
            id="platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="instagram">Instagram</option>
            <option value="twitter">Twitter</option>
            <option value="linkedin">LinkedIn</option>
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
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Add Account
        </button>
      </form>

      <h2 className="text-2xl font-bold mb-4">Your Accounts</h2>
      <ul className="space-y-2">
        {accounts.map((account) => (
          <li key={account.id} className="flex justify-between items-center bg-gray-100 p-4 rounded">
            <span>{account.username} ({account.platform})</span>
            <button 
              onClick={() => {/* Implement delete functionality */}}
              className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}