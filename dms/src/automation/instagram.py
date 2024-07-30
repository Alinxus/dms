from .base import BaseDMSender

class InstagramDMSender(BaseDMSender):
    def _login(self, page):
        page.goto("https://www.instagram.com/")
        page.fill("input[name='username']", self.credentials['username'])
        page.fill("input[name='password']", self.credentials['password'])
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

    def _navigate_to_dm(self, page, recipient):
        page.goto(f"https://www.instagram.com/{recipient}/")
        page.click("button[contains(text(), 'Message')]")
        page.wait_for_selector("div[aria-label='Message']")

    def _send_message(self, page, message):
        page.fill("div[aria-label='Message']", message)
        page.press("div[aria-label='Message']", "Enter")
        page.wait_for_load_state("networkidle")