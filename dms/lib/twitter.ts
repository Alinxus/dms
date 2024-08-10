// lib/twitterAutomation.ts
import { chromium, Browser, Page } from 'playwright';

export async function sendTwitterDM(username: string, password: string, recipient: string, message: string) {
  const browser: Browser = await chromium.launch({ headless: false });
  const page: Page = await browser.newPage();

  try {
    // Login to Twitter
    await page.goto('https://twitter.com/login');
    await page.fill('input[name="text"]', username);
    await page.click('div[role="button"]:has-text("Next")');
    await page.fill('input[name="password"]', password);
    await page.click('div[data-testid="LoginForm_Login_Button"]');

    // Wait for login to complete
    await page.waitForNavigation();

    // Navigate to DM page
    await page.goto(`https://twitter.com/messages/compose`);
    
    // Search for recipient
    await page.fill('input[data-testid="searchPeople"]', recipient);
    await page.click(`div[role="option"]:has-text("${recipient}")`);

    // Send message
    await page.fill('div[data-testid="dmComposerTextInput"]', message);
    await page.click('div[data-testid="dmComposerSendButton"]');

    console.log(`Message sent to ${recipient} on Twitter successfully.`);
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
  }
}