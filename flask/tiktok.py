from playwright.sync_api import sync_playwright
import random
import json
import time
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_login(page):
    logger.debug("Checking login status...")
    
    # Method 1: Check for profile icon
    if page.query_selector('div[data-e2e="profile-icon"]'):
        logger.debug("Login successful: Profile icon found")
        return True
    
    # Method 2: Check for login button
    if page.query_selector('a[href="/login"]'):
        logger.debug("Login failed: Login button found")
        return False
    
    # Method 3: Check URL for redirects
    if "login" in page.url:
        logger.debug(f"Login failed: Redirected to login page - {page.url}")
        return False
    
    # Method 4: Check for user-specific element
    if page.query_selector('div[data-e2e="user-post"]'):
        logger.debug("Login successful: User-specific element found")
        return True
    
    logger.warning("Login status unclear")
    return False

def send_tiktok_dms(messages_list, cookies, usernames, proxy=None):
    success = []
    failed = []

    with sync_playwright() as p:
        browser_type = p.chromium

        context_options = {
            "viewport": {'width': 1920, 'height': 1080},
            "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        if proxy:
            context_options["proxy"] = {
                "server": proxy
            }

        browser = browser_type.launch(
            channel='chrome',
            headless=True,  # Set to False for debugging
        )

        context = browser.new_context(**context_options)

        logger.debug("Adding cookies to browser context")
        context.add_cookies(json.loads(cookies))

        page = context.new_page()
        page.bring_to_front()
        logger.debug("Navigating to TikTok homepage")
        page.goto("https://www.tiktok.com/")
        time.sleep(random.uniform(2, 3))

        # Check if login was successful
        if not check_login(page):
            logger.error("Login failed. Please check your cookies.")
            page.screenshot(path="login_failed.png")
            return [], usernames

        logger.info("Login successful")

        for username in usernames:
            try:
                logger.debug(f"Processing user: {username}")
                time.sleep(random.uniform(3, 4))
                message = random.choice(messages_list)
                personalized_message = message.replace("{username}", username)
                
                # Navigate to user's profile
                logger.debug(f"Navigating to user's profile: {username}")
                page.goto(f'https://www.tiktok.com/@{username}')
                page.wait_for_selector('article', state="visible", timeout=90000)
                time.sleep(random.uniform(1, 2))

                # Extract user ID from page content
                logger.debug("Extracting user ID from page content")
                page_content = page.content()
                user_id_match = re.search(r'(?<="userInfo":\{"user":\{"id":")\d{1,30}', page_content)
                user_id = user_id_match.group(0) if user_id_match else None

                if not user_id:
                    logger.warning(f"Unable to find user ID for {username}")
                    failed.append(username)
                    continue

                # Navigate to DM page
                logger.debug(f"Navigating to DM page for user: {username}")
                page.goto(f'https://www.tiktok.com/messages?lang=en&u={user_id}')
                time.sleep(random.uniform(2, 3))

                # Type and send message
                logger.debug("Typing and sending message")
                input_selector = 'div[data-e2e="chat-input"]'
                page.wait_for_selector(input_selector, state="visible", timeout=90000)
                page.fill(input_selector, personalized_message)
                time.sleep(random.uniform(1, 2))

                send_button_selector = 'button[data-e2e="chat-send"]'
                page.click(send_button_selector)
                time.sleep(random.uniform(2, 4))

                # Check if message was sent successfully
                if page.query_selector('div[data-e2e="chat-item"]'):
                    logger.info(f"Message Sent to {username}")
                    success.append(username)
                else:
                    logger.warning(f"Failed to send message to {username}")
                    failed.append(username)

            except Exception as e:
                logger.exception(f"Unable to message {username}, moving on... Error: {str(e)}")
                failed.append(username)
                page.screenshot(path=f"error_{username}.png")

            time.sleep(random.uniform(30, 60))  # Longer delay between messages

        browser.close()

    return success, failed

# Example usage
if __name__ == "__main__":
    with open('tiktok_cookies.json', 'r') as f:
        cookies = f.read()
    
    messages = ["Hey {username}! Check out this cool TikTok effect!",
                "Hi {username}! Loved your recent video. Want to collab?"]
    usernames = ["user1", "user2", "user3"]
    
    # Example proxy (replace with your actual proxy if needed)
    test_proxy = "http://user:pass@proxy_host:proxy_port"
    
    success, failed = send_tiktok_dms(messages, cookies, usernames, proxy=test_proxy)
    logger.info(f"Successfully messaged: {success}")
    logger.info(f"Failed to message: {failed}")