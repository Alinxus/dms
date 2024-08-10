'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@clerk/nextjs'

type MessageStat = {
  status: string
  platform: string
  _count: { _all: number }
}

export default function Analytics() {
  const { isSignedIn, user } = useUser()
  const [stats, setStats] = useState<MessageStat[]>([])
  const [successRate, setSuccessRate] = useState<number>(0)

  useEffect(() => {
    if (isSignedIn && user) {
      fetchAnalytics()
    }
  }, [isSignedIn, user])

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`/api/analytics?userId=${user?.id}`)
      if (response.ok) {
        const data = await response.json()
        setStats(data.stats)
        setSuccessRate(data.successRate)
      } else {
        throw new Error('Failed to fetch analytics')
      }
    } catch (error) {
      console.error('Error fetching analytics:', error)
    }
  }

  if (!isSignedIn) {
    return <h1 className="text-3xl font-bold mb-4">Please sign in to view analytics</h1>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Analytics</h1>
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-2">Success Rate</h2>
        <p className="text-4xl font-bold text-green-500">{successRate.toFixed(2)}%</p>
      </div>
      <h2 className="text-2xl font-bold mb-2">Message Stats</h2>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">Status</th>
            <th className="border p-2">Platform</th>
            <th className="border p-2">Count</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((stat, index) => (
            <tr key={index} className="border">
              <td className="border p-2">{stat.status}</td>
              <td className="border p-2">{stat.platform}</td>
              <td className="border p-2">{stat._count._all}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}