import { chromium, Browser, Page } from 'playwright';

export async function sendInstagramDM(username: string, password: string, recipient: string, message: string) {
  const browser: Browser = await chromium.launch({ headless: false });
  const page: Page = await browser.newPage();

  try {
    // Login to Instagram
    await page.goto('https://www.instagram.com/accounts/login/');
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');
    
    // Wait for login to complete
    await page.waitForNavigation();

    // Navigate to DM page
    await page.goto('https://www.instagram.com/direct/inbox/');
    await page.click('button[aria-label="New message"]');
    
    // Search for recipient
    await page.fill('input[placeholder="Search..."]', recipient);
    await page.click(`div[aria-label="${recipient}"]`);
    await page.click('button[aria-label="Next"]');

    // Send message
    await page.fill('textarea[placeholder="Message..."]', message);
    await page.press('textarea[placeholder="Message..."]', 'Enter');

    console.log(`Message sent to ${recipient} successfully.`);
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
  }
}