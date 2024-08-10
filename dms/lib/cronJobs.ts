import cron from 'node-cron'
import { processQueue } from './messageQueue'

export function startCronJobs() {
  // Run the queue processing job every 5 minutes
  cron.schedule('*/5 * * * *', async () => {
    console.log('Running queue processing job')
    try {
      await processQueue()
    } catch (error) {
      console.error('Error processing queue:', error)
    }
  })
}