import { NextRequest, NextResponse } from 'next/server';
import {chromium} from 'playwright'

export async function POST(req: NextRequest) {
  let data;

  try {
    data = await req.json(); // Parse JSON body
  } catch (error) {
    return NextResponse.json({ error: 'Invalid JSON input' }, { status: 400 });
  }

  const { platform, username, password, recipient, message } = data;

  if (!platform || !username || !password || !recipient || !message) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  try {
    if (platform === 'twitter') {
      await sendTwitterDM(username, password, recipient, message);
    } else if (platform === 'instagram') {
      await sendInstagramDM(username, password, recipient, message);
    }
    return NextResponse.json({ status: 'Message sent successfully!' }, { status: 200 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to send message. ' + error.message }, { status: 500 });
  }
}

// Your existing sendTwitterDM and sendInstagramDM functions here...
const sendInstagramDM = async (
    username: string,
    password: string,
    recipient: string,
    message: string
  ) => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
  
    try {
      // Go to Instagram and log in
      await page.goto('https://www.instagram.com/', { waitUntil: 'networkidle' });
      
      // Fill in username and password
      await page.fill('input[name="username"]', username);
      await page.fill('input[name="password"]', password);
      await page.click('button[type="submit"]');
      
      // Wait for login to complete and check if login was successful
      await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 60000 });
      
      // Take a screenshot after login to verify
      await page.screenshot({ path: 'login_check.png' });
  
      const isLoginSuccessful = await page.isVisible('nav[role="navigation"]');
      if (!isLoginSuccessful) {
        throw new Error('Login failed. Please check your credentials.');
      }
  
      // Navigate to Direct Messages
      await page.goto('https://www.instagram.com/direct/inbox/', { waitUntil: 'networkidle' });
      await page.screenshot({ path: 'dm_page_check.png' });
  
      // Click to start a new message
      await page.click('svg[aria-label="New Message"]'); // This selector might need to be updated
      await page.waitForSelector('input[placeholder="Search..."]', { timeout: 60000 });
  
      // Search for the recipient
      await page.fill('input[placeholder="Search..."]', recipient);
      await page.waitForTimeout(3000); // Wait for the search results to load
      await page.keyboard.press('Enter'); // Select the first result
      await page.waitForTimeout(3000);
      await page.keyboard.press('Enter'); // Confirm the selection
  
      // Type the message
      await page.waitForSelector('textarea[placeholder="Message..."]', { timeout: 60000 });
      await page.fill('textarea[placeholder="Message..."]', message);
  
      // Send the message
      await page.click('button[type="button"]:has-text("Send")');
      
      // Take a final screenshot to confirm the message was sent
      await page.screenshot({ path: 'message_sent_check.png' });
  
    } catch (error) {
      console.error('Error sending Instagram DM:', error);
      await page.screenshot({ path: 'instagram_error_screenshot.png' }); // Take a screenshot for debugging
    } finally {
      await browser.close();
    }
  };
  