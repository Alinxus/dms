import { NextRequest, NextResponse } from 'next/server';
import { firefox, type BrowserContext, type Browser } from 'playwright';
import { randomUUID } from 'crypto';

interface SendDMRequest {
  messages: string[];
  cookies: string;
  usernames: string[];
  proxy?: string;
}

const randomSleep = (min: number, max: number) =>
  new Promise((resolve) => setTimeout(resolve, Math.random() * (max - min) + min));

export async function POST(req: NextRequest) {
  const { messages, cookies, usernames, proxy } = (await req.json()) as SendDMRequest;
  let browser: Browser | null = null;
  let context: BrowserContext | null = null;
  const success: string[] = [];
  const failed: string[] = [];

  try {
    console.log("Launching browser...");
    browser = await firefox.launch({
      headless: true,
      args: proxy ? [`--proxy-server=${proxy}`] : [],
      firefoxUserPrefs: {
        "dom.webdriver.enabled": false,
        "useAutomationExtension": false,
      },
    });

    context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    });

    console.log("Adding cookies to browser context...");
    await context.addCookies(JSON.parse(cookies));

    const page = await context.newPage();
    await page.goto("https://www.instagram.com/");
    await randomSleep(2000, 3000);

    await page.keyboard.press("Tab");
    await randomSleep(2000, 2000);
    await page.keyboard.press("Enter");
    await randomSleep(2000, 2000);

    await page.goto("https://www.instagram.com/direct/");

    for (const username of usernames) {
      try {
        await randomSleep(3000, 4000);
        const message = messages[Math.floor(Math.random() * messages.length)];
        const personalizedMessage = message.replace("{username}", username);

        const divSelector = ".x6s0dn4.x78zum5.xdt5ytf.xl56j7k";
        const divElement = await page.$(divSelector);
        if (divElement) {
          await divElement.click();
        } else {
          console.log(`Couldn't find the div element for ${username}`);
          failed.push(username);
          continue;
        }

        await randomSleep(4000, 5000);
        await page.keyboard.type(username);

        const selector = `span.x1lliihq.x1plvlek.xryxfnj:has-text('${username}')`;
        await page.waitForSelector(selector, { state: "visible", timeout: 10000 });
        await randomSleep(1000, 2000);
        await page.click(selector);
        await randomSleep(1000, 2000);

        for (let i = 0; i < 4; i++) {
          await page.keyboard.press("Tab");
          await randomSleep(100, 500);
        }

        await page.keyboard.press("Enter");
        await randomSleep(1000, 2000);
        await page.keyboard.type(personalizedMessage);
        await randomSleep(2000, 4000);
        await page.keyboard.press("Enter");
        await randomSleep(2000, 4000);

        console.log(`Message Sent to ${username}`);
        success.push(username);
        await page.goBack();
      } catch (error) {
        console.error(`Unable to message ${username}, moving on...`, error);
        failed.push(username);
        await page.goto("https://www.instagram.com/direct/");
      }
    }
  } catch (error) {
    console.error("Error during DM sending process:", error);
    return NextResponse.json({ success: false, error: error }, { status: 500 });
  } finally {
    if (browser) {
      await browser.close();
    }
  }

  return NextResponse.json({ success: true, sentTo: success, failed });
}