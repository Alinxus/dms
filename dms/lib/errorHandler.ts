import { NextResponse } from 'next/server'

export class AppError extends Error {
  statusCode: number

  constructor(message: string, statusCode: number) {
    super(message)
    this.statusCode = statusCode
  }
}

export function logError(error: Error, context?: string) {
  console.error(`[${new Date().toISOString()}] ${context ? context + ': ' : ''}`, error)
  // In a production app, you might want to use a more sophisticated logging service here
}

export function handleApiError(error: unknown) {
  if (error instanceof AppError) {
    return NextResponse.json({ error: error.message }, { status: error.statusCode })
  } else {
    logError(error as Error)
    return NextResponse.json({ error: 'An unexpected error occurred' }, { status: 500 })
  }
}