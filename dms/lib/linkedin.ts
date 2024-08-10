// lib/linkedinAutomation.ts
import { chromium, Browser, Page } from 'playwright';

export async function sendLinkedInDM(email: string, password: string, recipient: string, message: string) {
  const browser: Browser = await chromium.launch({ headless: false });
  const page: Page = await browser.newPage();

  try {
    // Login to LinkedIn
    await page.goto('https://www.linkedin.com/login');
    await page.fill('input#username', email);
    await page.fill('input#password', password);
    await page.click('button[type="submit"]');

    // Wait for login to complete
    await page.waitForNavigation();

    // Navigate to messaging
    await page.goto('https://www.linkedin.com/messaging/');

    // Click on "New message" button
    await page.click('button[aria-label="Compose message"]');

    // Search for recipient
    await page.fill('input[aria-label="Type a name or multiple names"]', recipient);
    await page.click(`div[aria-label="${recipient}"]`);

    // Send message
    await page.fill('div[role="textbox"]', message);
    await page.click('button[aria-label="Send"]');

    console.log(`Message sent to ${recipient} on LinkedIn successfully.`);
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
  }
}