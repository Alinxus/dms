import asyncio
from playwright.async_api import async_playwright
import random
import streamlit as st
import praw

async def main(proxy_server, proxy_port, proxy_username, proxy_password, reddit_username, reddit_password, combined_list):

    async with async_playwright() as p:

        browser = await p.firefox.launch(proxy={
                'server': f"{proxy_server}:{proxy_port}",
                'username': proxy_username,
                'password': proxy_password
            }, channel='firefox', headless=True)
        
        page = await browser.new_page()

        await page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.5"})
        await page.goto("https://www.reddit.com/login")

        await page.fill('input[name="username"]', reddit_username)
        await page.fill('input[name="password"]', reddit_password)

        await page.click('button[type="submit"]')
        
        st.success(f"Logged in with Username {reddit_username}")
        
        await asyncio.sleep(random.uniform(4, 5))

        unique_usernames = []

        with open('assets/usernames.txt', 'r') as file:
            for line in file:
                username = line.strip()
                if username not in unique_usernames:
                    unique_usernames.append(username)
        
        count = 0

        for username in unique_usernames:

            try:

                count = int(count + 1)

                reddit = praw.Reddit(
                client_id='3weoQJkbAfj5Y0JychVBpQ',
                client_secret='98xVkdvTu4FdomIbzbN4VVs9piZsNw',
                user_agent='Complete_Variation19',
                check_for_async=False
                )
                
                user = reddit.redditor(username)
                user_id = user.id

                await page.goto(f'https://chat.reddit.com/user/id/t2_{user_id}')

                await asyncio.sleep(random.uniform(4, 5))

                await page.click('textarea[name="message"]')

                await asyncio.sleep(4)

                await page.click('textarea[name="message"]')
            
                random_choice = random.choice(combined_list)

                selected_item_from_list1 = random_choice[0]
                selected_item_from_list2 = random_choice[1]

                await page.fill('textarea[name="message"]', selected_item_from_list1)

                #await page.screenshot(path='screenshot1.png')

                await asyncio.sleep(4)

                if selected_item_from_list2 is not None:

                    file_input = page.locator('input[type="file"]')
                    
                    await file_input.set_input_files(selected_item_from_list2)

                await asyncio.sleep(5)

                #await page.screenshot(path='screenshot2.png')

                await page.click('svg[rpl][icon-name="send-fill"]')

                await asyncio.sleep(4)

                element_exists = await page.query_selector('.theme-rpl.hasIcon.hasAction') is not None

                if element_exists:
                    st.warning(f"Account {reddit_username} Direct Message Limit Reached for the Day, Moving on to Next Account")
                    break
                else:
                    pass

                st.info(f"Message Sent to {username}")

                with open('assets/usernames.txt', 'r') as file:
                    lines = file.readlines()

                lines = [line for line in lines if line.strip() != username]

                with open('assets/usernames.txt', 'w') as file:
                    file.writelines(lines)

            except Exception as e:
                print(e)
                st.error(f"Failed To Message {username} 🚨, Skipping")

        await browser.close()
