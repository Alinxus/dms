from playwright.sync_api import sync_playwright
import time
import random
import json
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def take_screenshot(page, filename):
    os.makedirs('screenshots', exist_ok=True)
    page.screenshot(path=f'screenshots/{filename}.png', full_page=True)
    logging.info(f"Screenshot saved: screenshots/{filename}.png")

def check_login(page):
    if "https://www.facebook.com/" in page.url and page.query_selector('div[role="banner"]'):
        logging.info("Successfully logged in to Facebook")
        return True
    else:
        logging.error(f"Facebook login failed. Current URL: {page.url}")
        take_screenshot(page, "facebook_login_failed")
        return False

def send_message(page, username, message):
    try:
        logging.info(f"Navigating to Facebook profile: {username}")
        page.goto(f"https://www.facebook.com/{username}", wait_until="networkidle", timeout=30000)
        take_screenshot(page, f"facebook_profile_{username}")

        # Click on "Message" button
        message_button = page.query_selector('div[aria-label="Message"] a')
        if not message_button:
            logging.error("Message button not found")
            take_screenshot(page, f"facebook_no_message_button_{username}")
            return False

        message_button.click()
        page.wait_for_selector('div[aria-label="Message"]', state="visible", timeout=10000)

        # Type and send message
        input_field = page.query_selector('div[aria-label="Message"] p')
        input_field.fill(message)

        # Press Enter to send the message
        input_field.press('Enter')

        logging.info(f"Message sent successfully to {username} on Facebook")
        return True
    except Exception as e:
        logging.error(f"Error sending message to {username} on Facebook: {str(e)}")
        take_screenshot(page, f"facebook_error_{username}")
        return False

def send_facebook_dms(cookies, messages_list, usernames, proxy=None):
    success = []
    failed = []

    with sync_playwright() as p:
        try:
            browser_type = p.firefox

            context_options = {
                "viewport": {'width': 1920, 'height': 1080},
                "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
            }

            if proxy:
                context_options["proxy"] = {
                    "server": proxy
                }

            browser = browser_type.launch(
                headless=True,  # Set to False for debugging
                firefox_user_prefs={
                    "dom.webdriver.enabled": False,
                    "useAutomationExtension": False,
                }
            )

            context = browser.new_context(**context_options)

            # Load cookies
            context.add_cookies(json.loads(cookies))
            
            page = context.new_page()
            page.goto("https://www.facebook.com/")
            
            if not check_login(page):
                return [], usernames

            for username in usernames:
                message = random.choice(messages_list)
                if send_message(page, username, message):
                    success.append(username)
                else:
                    failed.append(username)
                
                time.sleep(random.uniform(30, 60))  # Delay between messages

        except Exception as e:
            logging.error(f"An unexpected error occurred in Facebook script: {str(e)}")
            failed.extend([u for u in usernames if u not in success and u not in failed])
        finally:
            if 'browser' in locals():
                browser.close()
    
    return success, failed

if __name__ == "__main__":
    # This section is for testing purposes
    with open('facebook_cookies.json', 'r') as f:
        test_cookies = f.read()
    
    test_messages = ["Hello! This is a test message on Facebook."]
    test_usernames = ["example.user"]
    
    # Example proxy (replace with your actual proxy if needed)
    test_proxy = "http://user:pass@proxy_host:proxy_port"
    
    success, failed = send_facebook_dms(test_cookies, test_messages, test_usernames, proxy=test_proxy)
    print(f"Facebook - Success: {success}")
    print(f"Facebook - Failed: {failed}")