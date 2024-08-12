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
    return NextResponse.json({ error: 'Failed to send message. ' + error }, { status: 500 });
  }
}


// Your existing sendTwitterDM and sendInstagramDM functions here...
const sendInstagramDM = async (
  username: string,
  password: string,
  recipient: string,
  message: string
) => {
  const browser = await chromium.launch({ headless: false }); // Set to false for debugging
  const page = await browser.newPage();

  try {
    console.log('Navigating to Instagram...');
    await page.goto('https://www.instagram.com/', { waitUntil: 'networkidle' });
    
    console.log('Filling login form...');
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="password"]', password);
    
    console.log('Submitting login form...');
    await page.click('button[type="submit"]');
    
    console.log('Waiting for login to complete...');
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 60000 });
    
    console.log('Checking if login was successful...');
    await page.screenshot({ path: 'login_check.png' });
    const isLoginSuccessful = await page.isVisible('nav[role="navigation"]');
    if (!isLoginSuccessful) {
      throw new Error('Login failed. Please check your credentials.');
    }

    console.log('Navigating to Direct Messages...');
    await page.goto('https://www.instagram.com/direct/inbox/', { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'dm_page_check.png' });

    console.log('Starting a new message...');
    await page.click('svg[aria-label="New message"]');
    await page.waitForSelector('input[placeholder="Search..."]', { timeout: 60000 });

    console.log('Searching for recipient...');
    await page.fill('input[placeholder="Search..."]', recipient);
    await page.waitForTimeout(3000);
    
    console.log('Selecting recipient...');
    const recipientOption = await page.$(`.x1i10hfl[href="/${recipient}/"]`);
    if (!recipientOption) {
      throw new Error(`Recipient ${recipient} not found.`);
    }
    await recipientOption.click();
    
    console.log('Clicking Next...');
    await page.click('div[role="button"]:has-text("Next")');

    console.log('Typing message...');
    await page.waitForSelector('textarea[placeholder="Message..."]', { timeout: 60000 });
    await page.fill('textarea[placeholder="Message..."]', message);

    console.log('Sending message...');
    await page.click('button[type="submit"]');
    
    console.log('Waiting for message to be sent...');
    await page.waitForTimeout(5000);
    
    console.log('Verifying message was sent...');
    const sentMessage = await page.$(`text="${message}"`);
    if (!sentMessage) {
      throw new Error('Message not found in the chat. It may not have been sent.');
    }
    
    console.log('Message sent successfully!');
    await page.screenshot({ path: 'message_sent_check.png' });

  } catch (error) {
    console.error('Error sending Instagram DM:', error);
    await page.screenshot({ path: 'instagram_error_screenshot.png' });
    throw error;
  } finally {
    await browser.close();
  }
};
  
  const sendTwitterDM = async (
    username: string,
    password: string,
    recipient: string,
    message: string
  ) => {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
  
    try {
      await page.goto('https://twitter.com/login', { waitUntil: 'networkidle' });
  
      // Wait for and fill the username field
      await page.waitForSelector('input[name="session[username_or_email]"]', { timeout: 60000 });
      await page.fill('input[name="session[username_or_email]"]', username);
  
      // Wait for and fill the password field
      await page.waitForSelector('input[name="session[password]"]', { timeout: 60000 });
      await page.fill('input[name="session[password]"]', password);
      
      // Click the login button
      await page.waitForSelector('div[data-testid="LoginForm_Login_Button"]', { timeout: 60000 });
      await page.click('div[data-testid="LoginForm_Login_Button"]');
      
      // Wait for the messages page and send the DM
      await page.waitForTimeout(10000); // Wait for page load
      await page.goto(`https://twitter.com/messages/compose?recipient_id=${recipient}`);
      await page.waitForSelector('div[aria-label="Message Text"]', { timeout: 60000 });
      await page.fill('div[aria-label="Message Text"]', message);
      await page.click('div[data-testid="dmComposerSendButton"]');
  
    } catch (error) {
      console.error('Error sending Twitter DM:', error);
      await page.screenshot({ path: 'twitter_error_screenshot.png' }); // Take a screenshot for debugging
    } finally {
      await browser.close();
    }
  };
  
  