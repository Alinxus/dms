import { NextResponse } from 'next/server'
import { getMessageStats, getSuccessRate } from '@/lib/analytics'
import { AppError, handleApiError } from '@/lib/errorHandler'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')

    if (!userId) {
      throw new AppError('userId is required', 400)
    }

    const endDate = new Date()
    const startDate = new Date(endDate.getTime() - 30 * 24 * 60 * 60 * 1000) // Last 30 days

    const stats = await getMessageStats(userId, startDate, endDate)
    const successRate = await getSuccessRate(userId, startDate, endDate)

    return NextResponse.json({ stats, successRate })
  } catch (error) {
    return handleApiError(error)
  }
}