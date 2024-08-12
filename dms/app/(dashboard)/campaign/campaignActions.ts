// app/actions/campaignActions.ts
'use server'

import prisma from '@/lib/prisma'

export async function createCampaign(data: {
  userId: string
  platform: string
  name: string
  status: string
}) {
  return prisma.campaign.create({
    data: {
      id: data.userId,
      platform: data.platform,
      name: data.name,
      status: data.status,
    },
  })
}