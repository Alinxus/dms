import { NextResponse } from 'next/server'
import prisma from '@/lib/prisma'

export async function POST(
  request: Request,
  { params }: { params: { messageId: string } }
) {
  const messageId = params.messageId

  try {
    const updatedMessage = await prisma.queuedMessage.update({
      where: { id: messageId },
      data: { status: 'pending' },
    })
    return NextResponse.json({ message: 'Message queued for retry', updatedMessage })
  } catch (error) {
    console.error('Failed to retry message:', error)
    return NextResponse.json({ error: 'Failed to retry message' }, { status: 500 })
  }
}