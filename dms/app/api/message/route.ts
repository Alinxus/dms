import { NextApiRequest, NextApiResponse } from 'next'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  const { userId } = req.query

  if (!userId) {
    return res.status(400).json({ message: 'userId is required' })
  }

  try {
    const messages = await prisma.queuedMessage.findMany({
      where: { userId: userId as string },
      orderBy: { createdAt: 'desc' },
    })
    res.status(200).json({ messages })
  } catch (error) {
    console.error('Failed to fetch messages:', error)
    res.status(500).json({ message: 'Failed to fetch messages' })
  }
}