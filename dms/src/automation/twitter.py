from .base import BaseDMSender
from playwright.sync_api import expect

class TwitterDMSender(BaseDMSender):
    def _login(self, page):
        page.goto("https://twitter.com/login")
        page.fill("input[autocomplete='username']", self.credentials['username'])
        page.click("div[role='button']:has-text('Next')")
        page.fill("input[name='password']", self.credentials['password'])
        page.click("div[data-testid='LoginForm_Login_Button']")
        page.wait_for_load_state("networkidle")

    def _navigate_to_dm(self, page, recipient):
        page.goto(f"https://twitter.com/messages/compose")
        page.fill("input[data-testid='searchPeople']", recipient)
        page.click(f"div[role='option']:has-text('{recipient}')")
        page.click("div[data-testid='nextButton']")
        expect(page.locator("div[data-testid='dmComposerTextInput']")).to_be_visible()

    def _send_message(self, page, message):
        page.fill("div[data-testid='dmComposerTextInput']", message)
        page.click("div[data-testid='dmComposerSendButton']")
        page.wait_for_load_state("networkidle")