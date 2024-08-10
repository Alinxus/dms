import { NextResponse } from 'next/server'
import prisma from '@/lib/prisma'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const userId = searchParams.get('userId')

  if (!userId) {
    return NextResponse.json({ error: 'userId is required' }, { status: 400 })
  }

  try {
    const accounts = await prisma.account.findMany({
      where: { userId: userId },
    })
    return NextResponse.json({ accounts })
  } catch (error) {
    console.error('Failed to fetch accounts:', error)
    return NextResponse.json({ error: 'Failed to fetch accounts' }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const { userId, platform, username, password } = await request.json()

    // In a real-world application, you should encrypt the password before storing it
    const account = await prisma.account.create({
      data: {
        userId,
        platform,
        username,
        password, // Remember to encrypt this in a real application!
      },
    })

    return NextResponse.json({ message: 'Account added successfully', accountId: account.id })
  } catch (error) {
    console.error('Error adding account:', error)
    return NextResponse.json({ error: 'Failed to add account' }, { status: 500 })
  }
}