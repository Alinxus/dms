import { chromium } from 'playwright';

export default async function handler(req, res) {
  const { username, password, recipient, message } = req.body;

    const browser = await chromium.launch({ headless: false });
      const page = await browser.newPage();

        await page.goto('https://www.instagram.com/');
          await page.fill('input[name="username"]', username);
            await page.fill('input[name="password"]', password);
              await page.click('button[type="submit"]');

                await page.waitForTimeout(5000);

                  await page.goto('https://www.instagram.com/direct/inbox/');
                    await page.click('button[type="button"]');
                      await page.fill('input[placeholder="Search..."]', recipient);
                        await page.click('button[type="button"]:has-text("Next")');
                          await page.fill('textarea[placeholder="Message..."]', message);
                            await page.click('button[type="button"]:has-text("Send")');

                              await browser.close();

                                res.status(200).json({ status: 'Message sent successfully!' });
                                }