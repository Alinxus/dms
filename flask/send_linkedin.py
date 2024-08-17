import asyncio
from playwright.async_api import async_playwright, TimeoutError
import random
import warnings
import os
from datetime import datetime

warnings.filterwarnings("ignore")

async def take_screenshot(page, filename):
    os.makedirs('screenshots', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/{filename}_{timestamp}.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"Screenshot saved: {screenshot_path}")

async def login_linkedin(page, email, password):
    await page.goto("https://www.linkedin.com/login")
    await page.fill('input[id="username"]', email)
    await page.fill('input[id="password"]', password)
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")
    
    if "feed" in page.url:
        print("Login successful")
        return True
    else:
        print("Login failed")
        await take_screenshot(page, "login_failed")
        return False

async def send_message(page, profile_url, message):
    try:
        await page.goto(profile_url, wait_until="networkidle")
        
        # Look for the "Message" button
        message_button = await page.query_selector('button[aria-label="Message"]')
        if not message_button:
            raise Exception("Message button not found")
        
        await message_button.click()
        await page.wait_for_selector('div[aria-label="Write a message…"]', timeout=10000)
        
        # Type and send the message
        await page.fill('div[aria-label="Write a message…"]', message)
        send_button = await page.query_selector('button[aria-label="Send"]')
        if not send_button:
            raise Exception("Send button not found")
        
        await send_button.click()
        await asyncio.sleep(random.uniform(2, 4))
        
        print(f"Message sent successfully to {profile_url}")
        return True
    except Exception as e:
        print(f"Error sending message to {profile_url}: {str(e)}")
        await take_screenshot(page, f"error_{profile_url.split('/')[-1]}")
        return False

async def main(email, password, messages_list, contacts):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            if not await login_linkedin(page, email, password):
                return None

            success = []
            failed = []

            for contact in contacts:
                message = random.choice(messages_list)
                if await send_message(page, contact, message):
                    success.append(contact)
                else:
                    failed.append(contact)
                
                await asyncio.sleep(random.uniform(30, 60))  # Longer delay between messages

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            await take_screenshot(page, "unexpected_error")
        finally:
            await browser.close()
        
        return success, failed

if __name__ == "__main__":
    print("This script should be imported and not run directly.")