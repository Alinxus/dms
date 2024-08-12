// app/actions/accountActions.ts
'use server'

import prisma from '@/lib/prisma'

export async function createAccount(data: {
  userId: string
  platform: string
  username: string
  password: string
}) {
  return prisma.account.create({
    data: {
      userId: data.userId,
      platform: data.platform,
      username: data.username,
      password: data.password, // Note: In a real application, you should hash this password
    },
  })
}

export async function getAccounts(userId: string) {
  return prisma.account.findMany({
    where: { userId },
    select: { id: true, platform: true, username: true },
  })
}