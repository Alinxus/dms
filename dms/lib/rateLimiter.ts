import { RateLimiterMemory } from 'rate-limiter-flexible'

const rateLimiter = new RateLimiterMemory({
  points: 10, // Number of points
  duration: 60 * 60, // Per hour
})

export async function checkRateLimit(userId: string): Promise<boolean> {
  try {
    await rateLimiter.consume(userId)
    return true
  } catch (error) {
    return false
  }
}