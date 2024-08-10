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

    const messages = await prisma.queuedMessage.findMany({
      where: { userId: userId },
      orderBy: { createdAt: 'desc' },
    })
    return NextResponse.json({ messages })
  } catch (error) {
    return handleApiError(error)
  }
}