from playwright.sync_api import sync_playwright
import random

class AntiDetectBrowser:
    def __init__(self, proxy_list):
            self.proxy_list = proxy_list
                    self.playwright = sync_playwright().start()
                            self.browser = self.playwright.chromium.launch()

                                def create_context(self):
                                        proxy = random.choice(self.proxy_list)
                                                context = self.browser.new_context(
                                                            proxy={
                                                                            "server": proxy,
                                                                                            # Add credentials if needed:
                                                                                                            # "username": "user",
                                                                                                                            # "password": "pass"
                                                                                                                                        },
                                                                                                                                                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                                                                                                                                            )
                                                                                                                                                                    return context

                                                                                                                                                                        def perform_action(self, url):
                                                                                                                                                                                context = self.create_context()
                                                                                                                                                                                        page = context.new_page()
                                                                                                                                                                                                page.goto(url)
                                                                                                                                                                                                        # Perform your actions here
                                                                                                                                                                                                                context.close()

                                                                                                                                                                                                                    def close(self):
                                                                                                                                                                                                                            self.browser.close()
                                                                                                                                                                                                                                    self.playwright.stop()

                                                                                                                                                                                                                                    # Usage
                                                                                                                                                                                                                                    proxy_list = [
                                                                                                                                                                                                                                        "http://proxy1.example.com:8080",
                                                                                                                                                                                                                                            "http://proxy2.example.com:8080",
                                                                                                                                                                                                                                                # Add more proxies...
                                                                                                                                                                                                                                                ]

                                                                                                                                                                                                                                                anti_detect = AntiDetectBrowser(proxy_list)

                                                                                                                                                                                                                                                for _ in range(10):  # Perform 10 actions
                                                                                                                                                                                                                                                    anti_detect.perform_action("https://example.com")

                                                                                                                                                                                                                                                    anti_detect.close()
                                                                                                                                                                                                                                                    