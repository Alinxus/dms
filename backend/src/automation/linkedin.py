# backend/src/automation/linkedin.py

from .base_automation import BaseAutomation

class LinkedInAutomation(BaseAutomation):
    async def setup(self):
        await super().setup()
        await self.page.goto("https://www.linkedin.com/")

    async def login(self, username, password):
        await self.page.goto("https://www.linkedin.com/login")
        await self.random_sleep(2, 3)
        await self.page.fill('#username', username)
        await self.page.fill('#password', password)
        await self.page.click('button[type="submit"]')
        await self.page.wait_for_navigation()

    async def send_dm(self, username, message):
        try:
            await self.page.goto("https://www.linkedin.com/messaging/")
            await self.random_sleep(2, 3)
            
            await self.page.click('button[aria-label="Compose message"]')
            await self.random_sleep(1, 2)
            
            await self.page.fill('input[aria-label="Type to search for connections"]', username)
            await self.random_sleep(1, 2)
            
            await self.page.click(f'div[aria-label="Search results"] li:has-text("{username}")')
            await self.random_sleep(1, 2)
            
            personalized_message = self.personalize_message(message, username)
            await self.page.fill('div[role="textbox"]', personalized_message)
            await self.random_sleep(1, 2)
            
            await self.page.click('button[aria-label="Send"]')
            await self.random_sleep(2, 3)
            
            return True
        except Exception as e:
            print(f"Error sending message to {username} on LinkedIn: {str(e)}")
            return False

    async def logout(self):
        await self.page.click('button[data-control-name="nav.settings"]')
        await self.random_sleep(1, 2)
        await self.page.click('a[data-control-name="nav.settings_signout"]')