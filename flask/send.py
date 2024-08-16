import asyncio
from playwright.async_api import async_playwright
import random
import json
import warnings
import os

warnings.filterwarnings("ignore")

async def main(messages_list, contacts):
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(channel='chrome', headless=True)
        context = await browser.new_context()

        cookies_file = 'session.json'
        print(f"Loading cookies from {cookies_file}.")
        with open(cookies_file, 'r') as json_file:
            saved_cookies = json.load(json_file)
        await context.add_cookies(saved_cookies)
        print("Cookies loaded successfully.")

        page = await context.new_page()
        await page.bring_to_front()
        await page.goto("https://www.instagram.com/")
        print("Navigated to Instagram.")
        await asyncio.sleep(random.uniform(2, 3))

        await page.keyboard.press("Tab")
        await asyncio.sleep(2)
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)

        count = 0
        await page.goto('https://www.instagram.com/direct/')
        print("Navigated to Instagram Direct Messages.")

        success = []
        failed = []

        for username in contacts:
            try:
                await asyncio.sleep(random.uniform(3, 4))
                message = random.choice(messages_list)
                personalized_message = message.replace("{username}", username)
                count += 1
                print(f"Sending message {count} to {username}.")
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
                await page.keyboard.press("Tab")
                await asyncio.sleep(random.uniform(0.1, 0.5))
                await page.keyboard.press("Tab")
                await asyncio.sleep(random.uniform(0.1, 0.5))
                await page.keyboard.press("Tab")
                await asyncio.sleep(random.uniform(0.1, 0.5))
                await page.keyboard.press("Tab")
                await asyncio.sleep(random.uniform(0.1, 0.5))
                await page.keyboard.press("Enter")
                await asyncio.sleep(random.uniform(1, 2))
                await page.keyboard.type(personalized_message)
                await asyncio.sleep(random.uniform(2, 4))
                await page.keyboard.press("Enter")
                await asyncio.sleep(random.uniform(2, 4))
                print(f"Message sent successfully to {username}.")
                success.append(username)
                await page.go_back()
            except Exception as e:
                print(f"Unable to send message to {username}. Error: {str(e)}")
                failed.append(username)
                await page.goto('https://www.instagram.com/direct/')
        await browser.close()
        print("Browser closed successfully.")
        
        return success, failed

if __name__ == "__main__":
    print("This script should be imported and not run directly.")