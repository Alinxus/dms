from .base_automation import BaseAutomation

class InstagramAutomation(BaseAutomation):
    async def setup(self):
        await super().setup()
        await self.page.goto("https://www.instagram.com/")
        await self.random_sleep(2, 3)
        await self.page.keyboard.press("Tab")
        await self.random_sleep(2, 3)
        await self.page.keyboard.press("Enter")
        await self.random_sleep(2, 3)
        await self.page.goto('https://www.instagram.com/direct/')

    async def send_dm(self, username, message):
        try:
            await self.random_sleep(3, 4)
            personalized_message = self.personalize_message(message, username)
            
            div_selector = '.x6s0dn4.x78zum5.xdt5ytf.xl56j7k'
            div_element = await self.page.query_selector(div_selector)
            await div_element.click()
            await self.random_sleep(4, 5)
            await self.page.keyboard.type(username)
            selector = f"span.x1lliihq.x1plvlek.xryxfnj:has-text('{username}')"
            await self.page.wait_for_selector(selector, state="visible", timeout=10000)
            await self.random_sleep(1, 2)
            await self.page.click(selector)
            await self.random_sleep(1, 2)
            for _ in range(4):
                await self.page.keyboard.press("Tab")
                await self.random_sleep(0.1, 0.5)
            await self.page.keyboard.press("Enter")
            await self.random_sleep(1, 2)
            await self.page.keyboard.type(personalized_message)
            await self.random_sleep(2, 4)
            await self.page.keyboard.press("Enter")
            await self.random_sleep(2, 4)
            await self.page.go_back()
            return True
        except Exception as e:
            print(f"Error sending message to {username} on Instagram: {str(e)}")
            await self.page.goto('https://www.instagram.com/direct/')
            return False