# backend/src/automation/twitter.py

from .base_automation import BaseAutomation

class TwitterAutomation(BaseAutomation):
    async def setup(self):
        await super().setup()
        await self.page.goto("https://twitter.com/")

    async def login(self, username, password):
        await self.page.goto("https://twitter.com/login")
        await self.random_sleep(2, 3)
        await self.page.fill('input[autocomplete="username"]', username)
        await self.page.click('div[role="button"]:has-text("Next")')
        await self.random_sleep(1, 2)
        await self.page.fill('input[name="password"]', password)
        await self.page.click('div[role="button"]:has-text("Log in")')
        await self.page.wait_for_navigation()

    async def send_dm(self, username, message):
        try:
            await self.page.goto("https://twitter.com/messages/compose")
            await self.random_sleep(2, 3)
            
            await self.page.fill('input[data-testid="searchPeople"]', username)
            await self.random_sleep(1, 2)
            
            await self.page.click(f'div[role="option"]:has-text("{username}")')
            await self.random_sleep(1, 2)
            
            personalized_message = self.personalize_message(message, username)
            await self.page.fill('div[data-testid="dmComposerTextInput"]', personalized_message)
            await self.random_sleep(1, 2)
            
            await self.page.click('div[data-testid="dmComposerSendButton"]')
            await self.random_sleep(2, 3)
            
            return True
        except Exception as e:
            print(f"Error sending message to {username} on Twitter: {str(e)}")
            return False

    async def logout(self):
        await self.page.click('div[data-testid="AppTabBar_More_Menu"]')
        await self.random_sleep(1, 2)
        await self.page.click('a[data-testid="logout"]')
        await self.random_sleep(1, 2)
        await self.page.click('div[data-testid="confirmationSheetConfirm"]')