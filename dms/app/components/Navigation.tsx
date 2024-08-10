import Link from 'next/link'
import { UserButton } from '@clerk/nextjs'

export default function Navigation() {
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <ul className="flex space-x-4">
          <li><Link href="/" className="hover:text-blue-200">Home</Link></li>
          <li><Link href="/campaigns" className="hover:text-blue-200">Campaigns</Link></li>
          <li><Link href="/queue" className="hover:text-blue-200">Queue</Link></li>
          <li><Link href="/accounts" className="hover:text-blue-200">Accounts</Link></li>
          <li><Link href="/analytics" className="hover:text-blue-200">Analytics</Link></li>
        </ul>
        <UserButton afterSignOutUrl="/" />
      </div>
    </nav>
  )
}