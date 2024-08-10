import prisma from './prisma'

export async function getMessageStats(userId: string, startDate: Date, endDate: Date) {
  const stats = await prisma.queuedMessage.groupBy({
    by: ['status', 'platform'],
    where: {
      userId: userId,
      createdAt: {
        gte: startDate,
        lte: endDate,
      },
    },
    _count: {
      _all: true,
    },
  })

  return stats
}

export async function getSuccessRate(userId: string, startDate: Date, endDate: Date) {
  const totalMessages = await prisma.queuedMessage.count({
    where: {
      userId: userId,
      createdAt: {
        gte: startDate,
        lte: endDate,
      },
    },
  })

  const sentMessages = await prisma.queuedMessage.count({
    where: {
      userId: userId,
      status: 'sent',
      createdAt: {
        gte: startDate,
        lte: endDate,
      },
    },
  })

  return totalMessages > 0 ? (sentMessages / totalMessages) * 100 : 0
}