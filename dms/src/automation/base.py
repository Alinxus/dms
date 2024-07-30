from playwright.sync_api import sync_playwright

class BaseDMSender:
    def __init__(self, credentials):
        self.credentials = credentials

    def send_dm(self, recipient, message):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                self._login(page)
                self._navigate_to_dm(page, recipient)
                self._send_message(page, message)
            finally:
                browser.close()

    def _login(self, page):
        raise NotImplementedError

    def _navigate_to_dm(self, page, recipient):
        raise NotImplementedError

    def _send_message(self, page, message):
        raise NotImplementedError