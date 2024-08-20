from playwright.sync_api import sync_playwright, TimeoutError
import random
import json
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def take_screenshot(page, filename):
    os.makedirs('screenshots', exist_ok=True)
    page.screenshot(path=f'screenshots/{filename}.png', full_page=True)
    logging.info(f"Screenshot saved: screenshots/{filename}.png")

def send_twitter_dms(messages_list, cookies, usernames, proxy=None):
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

        # Add the cookies to the browser context
        context.add_cookies(json.loads(cookies))

        page = context.new_page()
        page.bring_to_front()
        page.goto("https://x.com/home")
        time.sleep(random.uniform(2, 3))

        for username in usernames:
            try:
                logging.info(f"Attempting to message {username}")
                time.sleep(random.uniform(3, 4))
                message = random.choice(messages_list)
                personalized_message = message.replace("{username}", username)
                
                # Navigate to the user's profile
                page.goto(f'https://x.com/{username}')
                page.wait_for_selector('article', state="visible", timeout=10000)
                time.sleep(random.uniform(1, 2))

                # Find and click the "Message" button
                message_button_selector = "button[aria-label='Message']"
                message_button = page.wait_for_selector(message_button_selector, state="visible", timeout=10000)

                if message_button:
                    message_button.click()
                    logging.info(f"Clicked message button for {username}")
                    time.sleep(random.uniform(3, 4))

                    # Wait for the message input field
                    input_selector = 'div[data-testid="dmComposerTextInput"]'
                    input_field = page.wait_for_selector(input_selector, state="visible", timeout=10000)
                    
                    if input_field:
                        # Type the message
                        input_field.fill(personalized_message)
                        logging.info(f"Typed message for {username}")
                        time.sleep(random.uniform(2, 4))

                        # Try to find and click the send button
                        send_button = page.query_selector('div[data-testid="dmComposerSendButton"]')
                        if send_button:
                            send_button.click()
                            logging.info(f"Clicked send button for {username}")
                        else:
                            # If send button not found, press Enter
                            page.keyboard.press("Enter")
                            logging.info(f"Pressed Enter key for {username}")

                        time.sleep(random.uniform(2, 4))

                        # Verify the message was sent
                        try:
                            sent_message = page.wait_for_selector(f'div[data-testid="messageEntry"] >> text="{personalized_message}"', timeout=10000)
                            if sent_message:
                                logging.info(f"Message successfully sent to {username}")
                                success.append(username)
                            else:
                                logging.warning(f"Message may not have been sent to {username}")
                                take_screenshot(page, f"message_not_verified_{username}")
                                failed.append(username)
                        except TimeoutError:
                            logging.warning(f"Couldn't verify if message was sent to {username}")
                            take_screenshot(page, f"message_verification_timeout_{username}")
                            failed.append(username)
                    else:
                        logging.error(f"Message input field not found for {username}")
                        take_screenshot(page, f"no_input_field_{username}")
                        failed.append(username)
                else:
                    logging.error(f"Message button not found for {username}")
                    take_screenshot(page, f"no_message_button_{username}")
                    failed.append(username)

                # Go back to home
                page.goto("https://x.com/home")
                time.sleep(random.uniform(2, 3))

            except TimeoutError as te:
                logging.error(f"Timeout error for {username}: {str(te)}")
                take_screenshot(page, f"timeout_error_{username}")
                failed.append(username)
            except Exception as e:
                logging.error(f"Unable to message {username}, moving on... Error: {str(e)}")
                take_screenshot(page, f"unexpected_error_{username}")
                failed.append(username)
            finally:
                page.goto("https://x.com/home")
                time.sleep(random.uniform(2, 3))

        browser.close()

    return success, failed

if __name__ == "__main__":
    # This section is for testing purposes
    with open('twitter_cookies.json', 'r') as f:
        test_cookies = f.read()
    
    test_messages = ["Hello {username}! This is a test message on X."]
    test_usernames = ["example_user"]
    
    # Example proxy (replace with your actual proxy if needed)
    test_proxy = "http://user:pass@proxy_host:proxy_port"
    
    success, failed = send_twitter_dms(test_messages, test_cookies, test_usernames, proxy=test_proxy)
    print(f"Success: {success}")
    print(f"Failed: {failed}")