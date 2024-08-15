import asyncio
from playwright.async_api import async_playwright
import random
import json
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
import traceback

async def login(page, username, password, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Login attempt {attempt + 1}")
            await page.goto('https://www.instagram.com/')
            await page.wait_for_load_state('networkidle')

            print("Loaded Instagram login page")

            await handle_cookie_consent(page)

            print("Filling username")
            await page.fill('input[name="username"]', username)
            print("Filling password")
            await page.fill('input[name="password"]', password)

            print("Attempting to click submit button")
            submit_button_selectors = [
                'button[type="submit"]',
                'button:has-text("Log In")',
                'button:has-text("Sign In")',
                '[data-testid="login-button"]'
            ]

            for selector in submit_button_selectors:
                try:
                    await page.click(selector, timeout=10000)
                    print(f"Clicked submit button with selector: {selector}")
                    break
                except PlaywrightTimeoutError:
                    print(f"Failed to click submit button with selector: {selector}")
                    continue

            print("Waiting for navigation after login")
            await page.wait_for_load_state('networkidle', timeout=60000)

            print("Checking if login was successful")
            is_logged_in = await page.is_visible('a[href="/direct/inbox/"]', timeout=10000)
            if is_logged_in:
                print("Login successful")
                return True
            else:
                print("Login unsuccessful, checking for error messages")
                error_message = await page.inner_text('div[role="alert"]', timeout=5000)
                print(f"Login error: {error_message}")

        except Exception as e:
            print(f"An error occurred during login: {str(e)}")

        if attempt < max_retries - 1:
            print(f"Retrying login in 5 seconds...")
            await asyncio.sleep(5)
        else:
            print("Max login attempts reached")

    return False

async def handle_cookie_consent(page):
    try:
        print("Checking for cookie consent dialog")
        await page.wait_for_selector('div[role="dialog"]', timeout=5000)
        
        consent_button_selectors = [
            'button[tabindex="0"]:has-text("Allow")',
            'button:has-text("Accept All")',
            'button:has-text("Allow essential and optional cookies")'
        ]
        
        for selector in consent_button_selectors:
            try:
                await page.click(selector, timeout=5000)
                print(f"Clicked cookie consent button with selector: {selector}")
                return
            except PlaywrightTimeoutError:
                print(f"Failed to click {selector}")

        print("Attempting to click cookie consent button using JavaScript")
        await page.evaluate('''
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const allowButton = buttons.find(button => 
                    button.textContent.toLowerCase().includes('allow') || 
                    button.textContent.toLowerCase().includes('accept')
                );
                if (allowButton) allowButton.click();
            }
        ''')
    except PlaywrightTimeoutError:
        print("No cookie consent dialog found")
    except Exception as e:
        print(f"Error handling cookie consent: {str(e)}")

async def send_dms(messages_list, usernames, cookies_file, instagram_username, instagram_password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel='chrome',
            headless=True,  # Set to True for production
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context()
        
        # Load cookies
        try:
            with open(cookies_file, 'r') as json_file:
                cookies = json.load(json_file)
            await context.add_cookies(cookies)
            print("Cookies loaded successfully")
        except Exception as e:
            print(f"Error loading cookies: {e}")

        page = await context.new_page()
        
        try:
            print("Navigating to Instagram...")
            await page.goto("https://www.instagram.com/")
            await page.wait_for_load_state('networkidle')

            # Check if we're logged in
            is_logged_in = await page.is_visible('a[href="/direct/inbox/"]')
            if not is_logged_in:
                print("Not logged in. Attempting manual login...")
                await login(page, instagram_username, instagram_password)
                print("Login successful")

                # Save new cookies
                new_cookies = await context.cookies()
                with open(cookies_file, 'w') as json_file:
                    json.dump(new_cookies, json_file)
                print("New cookies saved")

            results = []
            for username in usernames:
                success = False
                for attempt in range(3):  # Try sending the DM up to 3 times
                    try:
                        print(f"Sending message to {username}, Attempt {attempt + 1}")
                        await page.goto('https://www.instagram.com/direct/new/', timeout=90000)
                        await page.wait_for_load_state('networkidle', timeout=90000)

                        # Verify visibility of the input box and proceed
                        await page.wait_for_selector('input[name="queryBox"]', timeout=90000)
                        await page.fill('input[name="queryBox"]', username)
                        
                        await page.wait_for_selector(f'div[role="button"]:has-text("{username}")', timeout=50000)
                        await page.click(f'div[role="button"]:has-text("{username}")')
                        await page.wait_for_selector('div[role="button"]:has-text("Next")', timeout=50000)
                        await page.click('div[role="button"]:has-text("Next")')

                        # Type and send message
                        await page.wait_for_selector('textarea[placeholder="Message..."]', timeout=50000)
                        message = random.choice(messages_list)
                        await page.fill('textarea[placeholder="Message..."]', message)
                        await page.click('button:has-text("Send")')

                        print(f"Message sent to {username}")
                        results.append({"username": username, "status": "sent"})
                        success = True
                        break  # Exit retry loop on success

                    except Exception as e:
                        print(f"Error sending message to {username} on attempt {attempt + 1}: {traceback.format_exc()}")

                    if attempt < 2:  # Wait before retrying
                        print(f"Retrying in 5 seconds...")
                        await asyncio.sleep(5)

                if not success:
                    results.append({"username": username, "status": "failed", "error": "Failed after 3 attempts"})

            return results

        except Exception as e:
            print(f"Unexpected error: {e}")
            return [{"username": username, "status": "failed", "error": str(e)} for username in usernames]

        finally:
            await browser.close()

def send_messages(messages_list, usernames, cookies_file='session.json', instagram_username=None, instagram_password=None):
    return asyncio.run(send_dms(messages_list, usernames, cookies_file, instagram_username, instagram_password))
