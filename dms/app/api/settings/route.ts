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

    let settings = await prisma.userSettings.findUnique({
      where: { userId: userId },
    })

    if (!settings) {
      settings = await prisma.userSettings.create({
        data: { userId: userId },
      })
    }

    return NextResponse.json({ settings })
  } catch (error) {
    return handleApiError(error)
  }
}

export async function POST(request: Request) {
  try {
    const { userId, sendFrequency, maxDailyMessages } = await request.json()

    if (!userId) {
      throw new AppError('userId is required', 400)
    }

    const settings = await prisma.userSettings.upsert({
      where: { userId: userId },
      update: { sendFrequency, maxDailyMessages },
      create: { userId, sendFrequency, maxDailyMessages },
    })

    return NextResponse.json({ settings })
  } catch (error) {
    return handleApiError(error)
  }
}