import { PrismaClient } from '@prisma/client'
import { sendInstagramDM } from './instagram'
import { sendTwitterDM } from './twitter'
import { sendLinkedInDM } from './linkedin'

const prisma = new PrismaClient()

const RATE_LIMIT = 60 * 1000 // 1 minute in milliseconds

export async function addToQueue(userId: string, platform: string, username: string, recipient: string, message: string) {
  return prisma.message.create({
    data: {
      userId,
      platform,
      username,
      recipient,
      message,
    },
  })
}

export async function processQueue() {
  const pendingMessages = await prisma.message.findMany({
    where: { status: 'pending' },
    orderBy: { createdAt: 'asc' },
  })

  for (const message of pendingMessages) {
    try {
      switch (message.platform) {
        case 'instagram':
          await sendInstagramDM(message.username, 'password', message.recipient, message.message)
          break
        case 'twitter':
          await sendTwitterDM(message.username, 'password', message.recipient, message.message)
          break
        case 'linkedin':
          await sendLinkedInDM(message.username, 'password', message.recipient, message.message)
          break
        default:
          throw new Error(`Unsupported platform: ${message.platform}`)
      }

      await prisma.message.update({
        where: { id: message.id },
        data: { status: 'sent' },
      })

      console.log(`Message ${message.id} sent successfully`)
    } catch (error) {
      console.error(`Failed to send message ${message.id}:`, error)
      await prisma.message.update({
        where: { id: message.id },
        data: { status: 'failed' },
      })
    }

    // Apply rate limiting
    await new Promise(resolve => setTimeout(resolve, RATE_LIMIT))
  }
}