# backend/src/automation/base_automation.py

import asyncio
from playwright.async_api import async_playwright
import random

class BaseAutomation:
    async def setup(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def teardown(self):
        await self.browser.close()
        await self.playwright.stop()

    async def random_sleep(self, min_seconds, max_seconds):
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))

    def personalize_message(self, message, username):
        return message.replace("{username}", username)

    async def login(self, username, password):
        raise NotImplementedError("Login method must be implemented in subclass")

    async def send_dm(self, username, message):
        raise NotImplementedError("Send DM method must be implemented in subclass")

    async def logout(self):
        raise NotImplementedError("Logout method must be implemented in subclass")