'use client'

import { useState, useEffect, useCallback } from 'react'
import { useUser } from '@clerk/nextjs'
import Link from 'next/link'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// ... (previous type definitions)

type CampaignPerformance = {
  campaignId: string
  campaignName: string
  data: { date: string; messagesSent: number }[]
}

export default function Dashboard() {
  const { isSignedIn, user } = useUser()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [sessions, setSessions] = useState<Session[]>([])
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [recentMessages, setRecentMessages] = useState<RecentMessage[]>([])
  const [campaignPerformance, setCampaignPerformance] = useState<CampaignPerformance[]>([])

  const fetchDashboardData = useCallback(async () => {
    if (!isSignedIn || !user) return

    try {
      const response = await fetch(`/api/dashboard?userId=${user.id}`)
      if (response.ok) {
        const data = await response.json()
        setAccounts(data.accounts)
        setSessions(data.sessions)
        setCampaigns(data.campaigns)
        setRecentMessages(data.recentMessages)
        setCampaignPerformance(data.campaignPerformance)
      } else {
        throw new Error('Failed to fetch dashboard data')
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }, [isSignedIn, user])

  useEffect(() => {
    fetchDashboardData()

    // Set up SSE for real-time updates
    if (isSignedIn && user) {
      const eventSource = new EventSource(`/api/dashboard/sse?userId=${user.id}`)
      
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'update') {
          fetchDashboardData()
        }
      }

      return () => {
        eventSource.close()
      }
    }
  }, [isSignedIn, user, fetchDashboardData])

  const handleCampaignAction = async (campaignId: string, action: 'start' | 'stop') => {
    try {
      const response = await fetch(`/api/campaigns/${campaignId}/${action}`, { method: 'POST' })
      if (response.ok) {
        fetchDashboardData()
      } else {
        throw new Error(`Failed to ${action} campaign`)
      }
    } catch (error) {
      console.error(`Error ${action}ing campaign:`, error)
    }
  }

  if (!isSignedIn) {
    return <h1 className="text-3xl font-bold mb-4">Please sign in to view your dashboard</h1>
  }

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      
      <section>
        <h2 className="text-2xl font-bold mb-2">Accounts and Sessions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {accounts.map(account => (
            <div key={account.id} className="bg-white p-4 rounded shadow">
              <h3 className="font-bold">{account.username}</h3>
              <p className="text-gray-600">{account.platform}</p>
              {sessions.filter(session => session.accountId === account.id).map(session => (
                <div key={session.id} className="mt-2 text-sm">
                  <p>Session ID: {session.id}</p>
                  <p>Last Active: {new Date(session.lastActive).toLocaleString()}</p>
                </div>
              ))}
              <Link href={`/accounts/${account.id}/edit`} className="text-blue-500 hover:underline mt-2 inline-block">
                Edit Account
              </Link>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-2">Active Campaigns</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead>
              <tr className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                <th className="py-3 px-6 text-left">Name</th>
                <th className="py-3 px-6 text-left">Status</th>
                <th className="py-3 px-6 text-center">Messages Sent</th>
                <th className="py-3 px-6 text-center">Messages Queued</th>
                <th className="py-3 px-6 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="text-gray-600 text-sm font-light">
              {campaigns.map(campaign => (
                <tr key={campaign.id} className="border-b border-gray-200 hover:bg-gray-100">
                  <td className="py-3 px-6 text-left whitespace-nowrap">
                    <Link href={`/campaigns/${campaign.id}/edit`} className="text-blue-500 hover:underline">
                      {campaign.name}
                    </Link>
                  </td>
                  <td className="py-3 px-6 text-left">{campaign.status}</td>
                  <td className="py-3 px-6 text-center">{campaign.messagesSent}</td>
                  <td className="py-3 px-6 text-center">{campaign.messagesQueued}</td>
                  <td className="py-3 px-6 text-center">
                    {campaign.status === 'active' ? (
                      <button 
                        onClick={() => handleCampaignAction(campaign.id, 'stop')}
                        className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                      >
                        Stop
                      </button>
                    ) : (
                      <button 
                        onClick={() => handleCampaignAction(campaign.id, 'start')}
                        className="bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600"
                      >
                        Start
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-2">Campaign Performance</h2>
        {campaignPerformance.map((campaign) => (
          <div key={campaign.campaignId} className="mt-4">
            <h3 className="text-xl font-bold">{campaign.campaignName}</h3>
            <div className="h-64">
              <Line
                data={{
                  labels: campaign.data.map(d => d.date),
                  datasets: [
                    {
                      label: 'Messages Sent',
                      data: campaign.data.map(d => d.messagesSent),
                      borderColor: 'rgb(75, 192, 192)',
                      tension: 0.1
                    }
                  ]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                }}
              />
            </div>
          </div>
        ))}
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-2">Recent Messages</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead>
              <tr className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                <th className="py-3 px-6 text-left">Campaign</th>
                <th className="py-3 px-6 text-left">Recipient</th>
                <th className="py-3 px-6 text-left">Status</th>
                <th className="py-3 px-6 text-left">Sent At</th>
              </tr>
            </thead>
            <tbody className="text-gray-600 text-sm font-light">
              {recentMessages.map(message => (
                <tr key={message.id} className="border-b border-gray-200 hover:bg-gray-100">
                  <td className="py-3 px-6 text-left whitespace-nowrap">{message.campaignName}</td>
                  <td className="py-3 px-6 text-left">{message.recipient}</td>
                  <td className="py-3 px-6 text-left">{message.status}</td>
                  <td className="py-3 px-6 text-left">{new Date(message.sentAt).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}