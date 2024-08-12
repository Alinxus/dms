import './globals.css'
import { ClerkProvider } from '@clerk/nextjs'
import Navigation from './components/Navigation'
import { startCronJobs } from '@/lib/cronJobs'

startCronJobs()

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="bg-gray-100 min-h-screen">
          {/* <Navigation /> */}
          <main className="container mx-auto p-4 mt-8">
            <div className="bg-white shadow-md rounded-lg p-6">
              {children}
            </div>
          </main>
        </body>
      </html>
    </ClerkProvider>
  )
}