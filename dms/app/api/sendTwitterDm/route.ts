// /app/api/sendTwitterDms/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { chromium } from 'playwright';
import random from 'random';
import { parseCsv } from '../../utils/csvParser';

export async function POST(req: NextRequest) {
  const { messagesList, csvFilePath } = await req.json();

  let usernames: string[] = [];
  if (csvFilePath) {
    usernames = await parseCsv(csvFilePath);
  } else {
    usernames = await readAllDataFromSheet('TwitterDMs');
  }

  try {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();

    const cookiesFile = 'twitterSession.json';
    const savedCookies = require(`../../../${cookiesFile}`);
    await context.addCookies(savedCookies);

    const page = await context.newPage();
    await page.goto('https://twitter.com/messages');

    for (const username of usernames) {
      try {
        await page.waitForTimeout(random.float(2000, 3000));
        await page.fill('input[name="session[username_or_email]"]', username);
        await page.press('input[name="session[username_or_email]"]', 'Enter');

        await page.waitForTimeout(random.float(1000, 2000));

        const message = messagesList[random.int(0, messagesList.length - 1)];
        const personalizedMessage = message.replace('{username}', username);

        await page.fill('textarea', personalizedMessage);
        await page.press('textarea', 'Enter');

        console.log(`Message Sent to ${username}`);
        await enterDataInSheetSuccess(username);
        await removeFirstLineFromSheet();

      } catch (error) {
        console.log(`Unable to message ${username}, moving on...`);
        await enterDataInSheetFail(username);
        await removeFirstLineFromSheet();
      }
    }

    await browser.close();
    return NextResponse.json({ success: true, message: 'Twitter DMs sent successfully' });

  } catch (error) {
    console.error('Error sending Twitter DMs:', error);
    return NextResponse.json({ success: false, error: error.message });
  }
}

// Helper functions for Google Sheets, etc., remain the same as the previous code
