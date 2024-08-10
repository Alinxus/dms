import { NextResponse } from 'next/server'
import prisma from '@/lib/prisma'
import { AppError, handleApiError } from '@/lib/errorHandler'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')

    if (!userId) {
      throw new AppError('userId is required', 400)
    }

    const accounts = await prisma.account.findMany({
      where: { userId: userId },
      select: { id: true, platform: true, username: true },
    })

    const sessions = await prisma.session.findMany({
      where: { account: { userId: userId } },
      select: { id: true, accountId: true, userAgent: true, updatedAt: true },
    })

    const campaigns = await prisma.campaign.findMany({
      where: { session: { account: { userId: userId } } },
      select: {
        id: true,
        name: true,
        status: true,
        messages: {
          select: {
            status: true,
          },
        },
      },
    })

    const recentMessages = await prisma.message.findMany({
      where: { campaign: { session: { account: { userId: userId } } } },
      orderBy: { updatedAt: 'desc' },
      take: 10,
      select: {
        id: true,
        campaign: { select: { name: true } },
        recipient: true,
        status: true,
        updatedAt: true,
      },
    })

    const formattedCampaigns = campaigns.map(campaign => ({
      id: campaign.id,
      name: campaign.name,
      status: campaign.status,
      messagesSent: campaign.messages.filter(m => m.status === 'sent').length,
      messagesQueued: campaign.messages.filter(m => m.status === 'pending').length,
    }))

    const formattedRecentMessages = recentMessages.map(message => ({
      id: message.id,
      campaignName: message.campaign.name,
      recipient: message.recipient,
      status: message.status,
      sentAt: message.updatedAt.toISOString(),
    }))

    return NextResponse.json({
      accounts,
      sessions: sessions.map(session => ({
        ...session,
        lastActive: session.updatedAt.toISOString(),
      })),
      campaigns: formattedCampaigns,
      recentMessages: formattedRecentMessages,
    })
  } catch (error) {
    return handleApiError(error)
  }
}