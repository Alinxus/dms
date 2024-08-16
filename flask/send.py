import asyncio
from playwright.async_api import async_playwright
import random
import json
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

async def main(messages_list, contacts, cookies_path):
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(channel='chrome', headless=True)
        context = await browser.new_context()

        print(f"Loading cookies from {cookies_path}")
        try:
            with open(cookies_path, 'r') as json_file:
                saved_cookies = json.load(json_file)
            await context.add_cookies(saved_cookies)
            print("Cookies loaded successfully.")
        except Exception as e:
            print(f"Error loading cookies: {str(e)}")
            return None

        page = await context.new_page()
        await page.bring_to_front()
        
        try:
            await page.goto("https://www.instagram.com/", wait_until="networkidle")
            print("Navigated to Instagram.")
            await take_screenshot(page, "instagram_home")

            await page.keyboard.press("Tab")
            await asyncio.sleep(2)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)

            await page.goto('https://www.instagram.com/direct/')
            print("Navigated to Instagram Direct Messages.")
            await take_screenshot(page, "dm_page")

            success = []
            failed = []

            for username in contacts:
                try:
                    await asyncio.sleep(random.uniform(3, 4))
                    message = random.choice(messages_list)
                    personalized_message = message.replace("{username}", username)
                    print(f"Sending message to {username}")
                    
                    div_selector = '.x6s0dn4.x78zum5.xdt5ytf.xl56j7k'
                    div_element = await page.query_selector(div_selector)
                    await div_element.click()
                    await asyncio.sleep(random.uniform(4, 5))
                    
                    await page.keyboard.type(username)
                    selector = f"span.x1lliihq.x1plvlek.xryxfnj:has-text('{username}')"
                    await page.wait_for_selector(selector, state="visible", timeout=10000)
                    await asyncio.sleep(random.uniform(1, 2))
                    await page.click(selector)
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    for _ in range(4):
                        await page.keyboard.press("Tab")
                        await asyncio.sleep(random.uniform(0.1, 0.5))
                    
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(random.uniform(1, 2))
                    await page.keyboard.type(personalized_message)
                    await asyncio.sleep(random.uniform(2, 4))
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    print(f"Message sent successfully to {username}")
                    success.append(username)
                    await page.go_back()
                    
                except Exception as e:
                    print(f"Unable to send message to {username}. Error: {str(e)}")
                    await take_screenshot(page, f"error_{username}")
                    failed.append(username)
                    await page.goto('https://www.instagram.com/direct/')

                await asyncio.sleep(random.uniform(3, 5))

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            await take_screenshot(page, "unexpected_error")
        finally:
            await browser.close()
            print("Browser closed successfully.")
        
        return success, failed

if __name__ == "__main__":
    print("This script should be imported and not run directly.")