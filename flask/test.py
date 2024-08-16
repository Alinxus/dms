from playwright.sync_api import sync_playwright

def send_instagram_dm(username, password, recipient, message):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto('https://www.instagram.com/accounts/login/')
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_navigation()

        page.goto(f'https://www.instagram.com/{recipient}/')
        page.click('button:has-text("Message")')
        page.fill('textarea[placeholder="Message..."]', message)
        page.click('button[type="submit"]')

        context.close()
        browser.close()

# Example usage
send_instagram_dm('olajide.alameen', 'Ahmadolajide04', 'alexlikesbiz', 'Hello! This is a test message.')
