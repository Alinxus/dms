import asyncio
from playwright.async_api import async_playwright
import json
import random

class BaseAutomation:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.browser = None
        self.context = None
        self.page = None

    async def setup(self):
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(channel='chrome', headless=False)
        self.context = await self.browser.new_context()

        with open(self.cookies_file, 'r') as json_file:
            saved_cookies = json.load(json_file)
        await self.context.add_cookies(saved_cookies)

        self.page = await self.context.new_page()
        await self.page.bring_to_front()

    async def close(self):
        await self.browser.close()

    async def random_sleep(self, min_time, max_time):
        await asyncio.sleep(random.uniform(min_time, max_time))

    @staticmethod
    def personalize_message(message, username):
        return message.replace("{username}", username)

    async def send_dm(self, username, message):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def login(self, username: str, password: str):
        pass