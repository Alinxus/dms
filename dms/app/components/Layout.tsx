import React, { ReactNode } from 'react';
import Head from 'next/head';
import { UserButton } from '@clerk/nextjs';

type Props = {
  children?: ReactNode;
  title?: string;
};

const Layout = ({ children, title = 'Mass DM Sender' }: Props) => (
  <div>
    <Head>
      <title>{title}</title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>
    <header>
      <nav className="bg-gray-800 text-white p-4 flex justify-between items-center">
        <ul className="flex space-x-4">
          <li><a href="/">Home</a></li>
          <li><a href="/campaigns">Campaigns</a></li>
          <li><a href="/accounts">Accounts</a></li>
          <li><a href='/queue'>Queues</a></li>
        </ul>
        <UserButton />
      </nav>
    </header>
    <main className="container mx-auto p-4">
      {children}
    </main>
    <footer className="bg-gray-800 text-white p-4 text-center">
      <span>Mass DM Sender © {new Date().getFullYear()}</span>
    </footer>
  </div>
);

export default Layout;