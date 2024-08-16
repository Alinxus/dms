import asyncio
from playwright.async_api import async_playwright, TimeoutError
import random
import json
import csv
import warnings
import os
import sys
import logging
from datetime import datetime

warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(filename='instagram_dm_sender.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def take_screenshot(page, filename):
    os.makedirs('screenshots', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/{filename}_{timestamp}.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    logging.info(f"Screenshot saved: {screenshot_path}")

async def validate_login(page):
    try:
        # Navigate to Instagram homepage
        await page.goto("https://www.instagram.com/", timeout=30000)
        await page.wait_for_load_state('networkidle')
        
        # Check for user-specific elements that indicate a successful login
        user_element = await page.query_selector('svg[aria-label="Home"]')
        if user_element:
            logging.info("Login validated successfully.")
            return True
        else:
            logging.error("Login validation failed. User-specific elements not found.")
            await take_screenshot(page, "login_validation_failed")
            return False
    except Exception as e:
        logging.error(f"Error during login validation: {str(e)}")
        await take_screenshot(page, "login_validation_error")
        return False

async def login_with_cookies(context, page):
    cookies_file = 'session.json'
    try:
        # Load cookies if available
        if os.path.exists(cookies_file):
            with open(cookies_file, 'r') as json_file:
                saved_cookies = json.load(json_file)
            await context.add_cookies(saved_cookies)
            logging.info("Cookies loaded successfully")

        # Validate the login
        if await validate_login(page):
            return True
        else:
            logging.error("Login unsuccessful. Cookies may be expired.")
            return False
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        await take_screenshot(page, "login_error")
        return False

async def manual_login(context, page):
    try:
        # Direct the user to log in manually
        logging.info("Manual login required.")
        print("Please log in manually.")
        await page.goto("https://www.instagram.com/accounts/login/")
        
        # Wait for the user to complete login
        await page.wait_for_selector('svg[aria-label="Home"]', timeout=60000)
        
        # Validate login and save new session cookies
        if await validate_login(page):
            logging.info("Manual login successful. Saving new cookies.")
            new_cookies = await context.cookies()
            with open('session.json', 'w') as json_file:
                json.dump(new_cookies, json_file)
            logging.info("New cookies saved successfully.")
            return True
        else:
            logging.error("Manual login failed.")
            return False
    except Exception as e:
        logging.error(f"Error during manual login: {str(e)}")
        await take_screenshot(page, "manual_login_error")
        return False

def read_csv_usernames(filename):
    usernames = []
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0]:
                    usernames.append(row[0])
        return usernames
    except FileNotFoundError:
        logging.error(f"CSV file '{filename}' not found.")
        return []

def get_user_input_usernames():
    usernames = []
    print("Enter usernames (one per line). Press Enter twice to finish:")
    while True:
        username = input().strip()
        if not username:
            break
        usernames.append(username)
    return usernames

async def send_message(page, username, message):
    try:
        logging.info(f"Attempting to send message to {username}")
        
        # Navigate directly to the user's profile
        await page.goto(f'https://www.instagram.com/{username}/', timeout=30000)
        await page.wait_for_load_state('networkidle', timeout=30000)

        # Look for the "Message" button
        message_button_selector = 'div[role="button"]:has-text("Message")'
        await page.wait_for_selector(message_button_selector, timeout=10000)
        await page.click(message_button_selector)

        # Wait for the message input to appear
        message_input_selector = 'textarea[placeholder="Message..."]'
        await page.wait_for_selector(message_input_selector, timeout=10000)

        # Type and send the message
        await page.fill(message_input_selector, message)
        await page.keyboard.press('Enter')

        logging.info(f"Message sent to {username}")
        await take_screenshot(page, f"message_sent_{username}")
        return True
    except Exception as e:
        logging.error(f"Error sending message to {username}: {str(e)}")
        await take_screenshot(page, f"message_error_{username}")
        return False
async def main(messages_list, usernames):
    proxy = os.getenv('PROXY')
    async with async_playwright() as p:
        launch_options = {
            'headless': False,
            'channel': 'chrome'
        }
        if proxy:
            launch_options['proxy'] = {
                'server': proxy
            }
        browser = await p.chromium.launch(**launch_options)
        context = await browser.new_context()
        page = await context.new_page()

        if not await login_with_cookies(context, page):
            logging.error("Login failed. Exiting.")
            await browser.close()
            return

        successful_sends = []
        failed_sends = []

        for username in usernames:
            message = random.choice(messages_list)
            success = await send_message(page, username, message)
            if success:
                successful_sends.append(username)
            else:
                failed_sends.append(username)
            await asyncio.sleep(random.uniform(10, 20))  # Add a longer delay between messages

        await browser.close()

        logging.info("\nSummary:")
        logging.info(f"Successfully sent messages to: {successful_sends}")
        logging.info(f"Failed to send messages to: {failed_sends}")
        print("\nSummary:")
        print(f"Successfully sent messages to: {successful_sends}")
        print(f"Failed to send messages to: {failed_sends}")

if __name__ == "__main__":    # Read environment variables for messages
    message_var_count = int(os.getenv("NUM_VARIATIONS", 1))
    messages = [os.getenv(f"DM_MESSAGE_{i+1}", f"Default message {i+1}") for i in range(message_var_count)]

    # Ask user for input method
    input_method = input("Choose input method (1 for CSV, 2 for manual input): ")

    if input_method == '1':
        csv_filename = input("Enter the CSV filename: ")
        usernames = read_csv_usernames(csv_filename)
    elif input_method == '2':
        usernames = get_user_input_usernames()
    else:
        logging.error("Invalid input method selected. Exiting.")
        print("Invalid input method selected. Exiting.")
        sys.exit(1)

    if not usernames:
        logging.error("No usernames provided. Exiting.")
        print("No usernames provided. Exiting.")
        sys.exit(1)

    asyncio.run(main(messages, usernames))
