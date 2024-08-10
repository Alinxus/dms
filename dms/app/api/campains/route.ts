import { NextResponse } from 'next/server'
import prisma from '@/lib/prisma'
import { addToQueue } from '@/lib/messageQueue'

export async function POST(request: Request) {
  try {
    const { userId, platform, username, recipient, message } = await request.json()

    // Create campaign in database
    const campaign = await prisma.campaign.create({
      data: {
        userId,
        platform,
        name: `${platform} campaign to ${recipient}`,
      },
    })

    // Add message to queue
    await addToQueue(userId, campaign.id, platform, username, recipient, message)

    return NextResponse.json({ message: 'Campaign created successfully', campaignId: campaign.id })
  } catch (error) {
    console.error('Error creating campaign:', error)
    return NextResponse.json({ error: 'Failed to create campaign' }, { status: 500 })
  }
}