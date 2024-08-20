from playwright.sync_api import sync_playwright
import random
import json
import time

def send_instagram_dms(messages_list, cookies, usernames, proxy):
    success = []
    failed = []

    with sync_playwright() as p:
        browser_type = p.firefox
        browser_args = []

        if proxy:
            browser_args.append(f'--proxy-server={proxy}')

        print("Launching browser...")
        browser = browser_type.launch(
            headless=True,  # Set to False for debugging
            firefox_user_prefs={
                "dom.webdriver.enabled": False,
                "useAutomationExtension": False,
            },
            args=browser_args
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
        )

        print("Adding cookies to browser context...")
        context.add_cookies(json.loads(cookies))

        page = context.new_page()
        page.bring_to_front()
        page.goto("https://www.instagram.com/")
        time.sleep(random.uniform(2, 3))

        page.keyboard.press("Tab")
        time.sleep(2)
        page.keyboard.press("Enter")
        time.sleep(2)

        page.goto('https://www.instagram.com/direct/')

        for username in usernames:
            try:
                time.sleep(random.uniform(3, 4))
                message = random.choice(messages_list)
                personalized_message = message.replace("{username}", username)
                
                div_selector = '.x6s0dn4.x78zum5.xdt5ytf.xl56j7k'
                div_element = page.query_selector(div_selector)
                div_element.click()
                time.sleep(random.uniform(4, 5))
                page.keyboard.type(username)
                
                selector = f"span.x1lliihq.x1plvlek.xryxfnj:has-text('{username}')"
                page.wait_for_selector(selector, state="visible", timeout=10000)
                time.sleep(random.uniform(1, 2))
                page.click(selector)
                time.sleep(random.uniform(1, 2))
                page.keyboard.press("Tab")
                time.sleep(random.uniform(0.1, 0.5))
                page.keyboard.press("Tab")
                time.sleep(random.uniform(0.1, 0.5))
                page.keyboard.press("Tab")
                time.sleep(random.uniform(0.1, 0.5))
                page.keyboard.press("Tab")
                time.sleep(random.uniform(0.1, 0.5))
                page.keyboard.press("Enter")
                time.sleep(random.uniform(1, 2))
                page.keyboard.type(personalized_message)
                time.sleep(random.uniform(2, 4))
                page.keyboard.press("Enter")
                time.sleep(random.uniform(2, 4))

                print(f"Message Sent to {username}")
                success.append(username)
                page.go_back()
            except Exception as e:
                print(f"Unable to message {username}, moving on...")
                failed.append(username)
                page.goto('https://www.instagram.com/direct/')

        browser.close()

    return success, failed
