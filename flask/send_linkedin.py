from playwright.sync_api import sync_playwright, TimeoutError
import time
import random
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def take_screenshot(page, filename):
    os.makedirs('screenshots', exist_ok=True)
    page.screenshot(path=f'screenshots/{filename}.png', full_page=True)
    logging.info(f"Screenshot saved: screenshots/{filename}.png")

def check_login(page):
    if "feed" in page.url:
        logging.info("Successfully logged in")
        return True
    else:
        logging.error(f"Login failed. Current URL: {page.url}")
        take_screenshot(page, "login_failed")
        return False

def send_message(page, profile_url, message):
    try:
        logging.info(f"Navigating to profile: {profile_url}")
        page.goto(profile_url, wait_until="networkidle", timeout=90000)
        take_screenshot(page, f"profile_{profile_url.split('/')[-1]}")
        
        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")
        
        # Try to find the message button with various selectors
        message_button_selectors = [
            'button.artdeco-button.artdeco-button--2.artdeco-button--primary:has-text("Message")',
            'button[aria-label^="Message"]',
            'button:has-text("Message")',
            'a[data-control-name="message"]'
        ]
        
        message_button = None
        for selector in message_button_selectors:
            message_button = page.query_selector(selector)
            if message_button:
                logging.info(f"Found message button with selector: {selector}")
                break
        
        if not message_button:
            logging.error("Message button not found")
            take_screenshot(page, f"no_message_button_{profile_url.split('/')[-1]}")
            return False
        
        logging.info("Clicking 'Message' button")
        message_button.click()
        
        # Wait for the messaging overlay to appear
        overlay_selector = 'div[aria-label="Messaging overlay"]'
        page.wait_for_selector(overlay_selector, state="visible", timeout=10000)
        take_screenshot(page, f"message_overlay_{profile_url.split('/')[-1]}")
        
        # Try to find the message input field
        input_selector = 'div[role="textbox"][aria-label="Write a message…"]'
        message_input = page.query_selector(input_selector)
        
        if not message_input:
            logging.error("Message input field not found")
            take_screenshot(page, f"no_input_field_{profile_url.split('/')[-1]}")
            return False
        
        logging.info("Typing message")
        message_input.fill(message)
        
        # Try to find the send button
        send_button_selector = 'button[aria-label="Send now"]'
        send_button = page.query_selector(send_button_selector)
        
        if not send_button:
            logging.error("Send button not found")
            take_screenshot(page, f"no_send_button_{profile_url.split('/')[-1]}")
            return False
        
        logging.info("Clicking 'Send' button")
        send_button.click()
        
        time.sleep(random.uniform(2, 4))
        
        logging.info(f"Message sent successfully to {profile_url}")
        return True
    except Exception as e:
        logging.error(f"Error sending message to {profile_url}: {str(e)}")
        take_screenshot(page, f"error_{profile_url.split('/')[-1]}")
        return False

def send_linkedin_dms(cookies, messages_list, contacts):
    success = []
    failed = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel='chrome', headless=True)  # Set to True for production
            context = browser.new_context()
            
            # Load cookies
            context.add_cookies(json.loads(cookies))
            
            page = context.new_page()
            page.goto("https://www.linkedin.com/feed/")
            
            if not check_login(page):
                return [], contacts

            for contact in contacts:
                message = random.choice(messages_list)
                if send_message(page, contact, message):
                    success.append(contact)
                else:
                    failed.append(contact)
                
                time.sleep(random.uniform(30, 60))  # Longer delay between messages

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            failed.extend([c for c in contacts if c not in success and c not in failed])
        finally:
            if 'browser' in locals():
                browser.close()
    
    return success, failed

if __name__ == "__main__":
    # This section is for testing purposes
    with open('linkedin_cookies.json', 'r') as f:
        test_cookies = f.read()
    
    test_messages = ["Hello! This is a test message."]
    test_contacts = ["https://www.linkedin.com/in/example-profile"]
    
    success, failed = send_linkedin_dms(test_cookies, test_messages, test_contacts)
    print(f"Success: {success}")
    print(f"Failed: {failed}")