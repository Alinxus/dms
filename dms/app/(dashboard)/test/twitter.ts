import { chromium } from 'playwright';

export const sendTwitterDM = async (
  username: string,
  password: string,
  recipient: string,
  message: string
): Promise<string> => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('https://twitter.com/login');
  await page.fill('input[name="session[username_or_email]"]', username);
  await page.fill('input[name="session[password]"]', password);
  await page.click('div[data-testid="LoginForm_Login_Button"]');

  await page.waitForTimeout(5000);

  await page.goto(`https://twitter.com/messages/compose?recipient_id=${recipient}`);
  await page.fill('div[aria-label="Message Text"]', message);
  await page.click('div[data-testid="dmComposerSendButton"]');

  await browser.close();

  return 'Twitter DM sent successfully!';
};
