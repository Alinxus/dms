import streamlit as st
import asyncio
import os
from reddit import scrape_usernames,scrape_usernames_from_comments,scrape_usernames_from_posts
from procsum import main
from streamlit_extras.let_it_rain import rain

login = False

if __name__ == '__main__':

    agreement = """Software License Agreement

This software 'RedditReach' is protected by copyright law and is the property of the author. You are granted the right to use the software for personal purposes only. You may not distribute, sublicense, or make any modifications to the software without the explicit permission of the author.

For inquiries regarding distribution or modification, please contact the author at basitcarry@proton.me

By using this software, you agree to abide by the terms of this license agreement.

August 28, 2023"""

    st.set_page_config(
    page_title="RedditReach",
    page_icon="🤠",
)

    rain(
        emoji="🤠",
        font_size=34,
        falling_speed=5,
        animation_length=1,
    )

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.markdown('<style> .stDeployButton { display: none; } </style>', unsafe_allow_html=True)

    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

    page = st.sidebar.selectbox("Select a page", ["🎉 Welcome", "✅ Add Account's and Proxies", "💬 Send Direct Message's", "👀 Frequently Asked Question's", "⚠️ License Agreement"])

    if page == "🎉 Welcome":
        
        image = st.image("assets/bg.png")

        st.title("Welcome to RedditReach 🤠")

        st.divider()

        st.info("RedditReach is a bot that automates the process of sending direct chat messages (DMs) on Reddit to multiple users.")
        st.info("To get started, navigate using the sidebar on the left.")
        hyperlink_url = "https://discord.gg/eW5bVTFgss"
        st.info(f'Require assistance or have suggestions? Reach out to me [here]({hyperlink_url}). Alternatively, you can reach me via email at basitcarry@proton.me.')

    elif page == "✅ Add Account's and Proxies":

        image = st.image("assets/bg.png")

        st.title("Add Account's and Proxies")

        st.divider()

        st.subheader("Paid Version💰")

        num_accounts = st.number_input("Add Accounts", min_value=1, step=1)
        
        account_data = []

        for i in range(num_accounts):

            st.subheader(f"Account {i + 1}")

            username = st.text_input("Enter Reddit Username", key=f"username_{i}",placeholder='Username')
            password = st.text_input("Enter Reddit Password", key=f"password_{i}", type="password",placeholder='Passowrd')

            st.subheader(f"Proxy For Account {i + 1}")

            webshare_url = 'https://www.webshare.io/'
            st.info(f"Need Proxies? No problem! Get 10 free proxies from [Webshare](https://www.webshare.io/) to get started.")
            proxy_col1, proxy_col2, proxy_col3, proxy_col4 = st.columns(4)

            proxy_server = proxy_col1.text_input("Proxy Server", key=f"proxy_server_{i}", placeholder='Proxy Server')
            proxy_port = proxy_col2.text_input("Proxy Port", key=f"proxy_port_{i}", placeholder='Proxy Port')
            proxy_username = proxy_col3.text_input("Proxy Username", key=f"proxy_username_{i}", placeholder='Proxy Username')
            proxy_password = proxy_col4.text_input("Proxy Password", key=f"proxy_password_{i}", type="password", placeholder='Proxy Password')

            account_entry = f"{username},{password},{proxy_server},{proxy_port},{proxy_username},{proxy_password}"
            account_data.append(account_entry)

        empty_space = st.write(" ")

        if st.button("Add Account(s) 👍",help='Adds the account to the accounts list'):
            with open("assets/Accounts.txt", "a") as file:
                for entry in account_data:
                    file.write(entry + "\n")

            st.success("Accounts Saved")

        empty_space = st.write(" ")
        
        st.warning("Before adding an account for sending DMs, confirm its eligibility by sending a manual DM on Reddit. Note that new accounts with very low karma (less than 100) may not be permitted to send chat messages by Reddit.")
        
        empty_space = st.write(" ")
        empty_space = st.write(" ")
        
        col1, col3, col2 = st.columns(3)

        col3.write('')

        if col1.button("Show Saved Account(s)",help='Shows all the accounts available in accounts list'):
            with open("assets/Accounts.txt", "r") as file:
                accounts = file.readlines()
                for account in accounts:
                    st.info(account.strip()) 

        if col2.button("Remove All Accounts 🚨", help='Removes all saved Accounts and Proxies',type="primary"):
            try:
                file_path = "assets/Accounts.txt"
                os.remove(file_path)
                st.success("All Accounts and Proxies Have Been Removed")
            except:
                st.error("No Saved Accounts Found")

    elif page == "💬 Send Direct Message's":
        
        image = st.image("assets/bg.png")

        try:

            accounts_num = 0
            reddit_usernames = []
            reddit_passwords = []
            proxy_servers = []
            proxy_ports = []
            proxy_usernames = []
            proxy_passwords = []

            with open("assets/Accounts.txt", "r") as file:

                for line in file:
                    parts = line.strip().split(",")

                    if len(parts) >= 6:
                        accounts_num = int(accounts_num + 1)
                        reddit_username, reddit_password, proxy_server, proxy_port, proxy_username, proxy_password = parts[:6]
                        reddit_usernames.append(reddit_username)
                        reddit_passwords.append(reddit_password)
                        proxy_servers.append(proxy_server)
                        proxy_ports.append(proxy_port)
                        proxy_usernames.append(proxy_username)
                        proxy_passwords.append(proxy_password)

            st.title("Send Direct Messages")

            st.divider()

            st.subheader("1. Scrape Usernames")

            choice = st.radio("Scrape Usernames from", ["Posts and Comments", "Posts Only", "Comments Only"])

            subreddit_names = []

            subreddit_names_num = st.number_input("How Many Subreddits Do You Want to Scrape Usernames From",min_value=1,step=1)

            for i in range(subreddit_names_num):

                subreddit_name = st.text_input(f"Enter Subreddit Name {i+1}", placeholder='dankmemes',key=f"subreddit_names_{i}")
                subreddit_names.append(subreddit_name)

            if st.button("Scrape Usernames"):
                try:
                    os.remove('assets/usernames.txt')
                    st.info("Removed Previously Scraped Usernames")
                except:
                    pass
                with st.spinner("Scraping in Progress"):

                    st.warning(f"Scraping from {choice}")

                    for subreddit_name in subreddit_names:
                        if choice == "Posts and Comments":
                            scrape_usernames(subreddit_name)
                        elif choice == "Posts Only":
                            scrape_usernames_from_posts(subreddit_name)
                        elif choice == "Comments Only":
                            scrape_usernames_from_comments(subreddit_name)

                        st.success(f'Scrapping from r/{subreddit_name} was Succuessful')
                    st.success('All Usernames Scraped Successfully')

            flag = True

            st.divider()

            st.subheader("2. Enter Message(s)")

            number_of_message = st.number_input("How Many Messages Do You Want to Enter",min_value=1, step=1)
            st.info("The bot will randomly select a message from the entered messages to send for each direct message")

            messages = []
            uploaded_images = []

            for i in range(number_of_message):

                message = st.text_area(f"Enter Message {i+1}",placeholder='Enter your desired Message here',key=f"message_{i}")
                uploaded_image = st.file_uploader(f"Attach an Image with Message {i+1}",key=f"image_paths_{i}")

                if uploaded_image is not None:
                    
                    image_path = 'images/' + uploaded_image.name
                    uploaded_images.append(image_path)
                
                elif uploaded_image is None:
                    
                    image_path = None
                    uploaded_images.append(image_path)

                messages.append(message)
                
            combined_list = list(zip(messages, uploaded_images))
            
            st.warning("Attached Image(s) must be in the 'Images' folder")

            if st.button("Enter",help="Press Twice if you are not attaching Image(s)"):
                st.success("Message(s) Set Successfully")
                flag = False

            st.divider()

            st.subheader("3. Start Direct Messeging 🔥")
                    
            if st.button('Start Direct Messeging 🔥',disabled=flag, type="primary"):

                with st.spinner("Direct Messeging has Been Started"):

                    for i in range(accounts_num):
                        
                        try:
                            title=loop.run_until_complete(main(proxy_servers[i], proxy_ports[i], proxy_usernames[i], proxy_passwords[i], reddit_usernames[i], reddit_passwords[i], combined_list))
                            st.success(f"All Messages Sent using account {reddit_usernames[i]}.\nMoving on to Next Account.")
                        except Exception as e:
                            print(e)
                            st.error(f"Unable to Reach Reddit, Please Check the Proxy Associated with Account {reddit_usernames[i]}")
                            st.warning(f"Skipping {reddit_usernames[i]} and Moving on to Next Account")

                        if i == accounts_num:
                            break
                        
                    st.success(f"All Accounts ({accounts_num}) Have Been Used to Send DM's to Users in the Subreddit")
        except Exception as e:
            print(e)
            st.error("You have to Add Account(s) Before you can use this feature")

    elif page == "👀 Frequently Asked Question's":

        image = st.image("assets/bg.png")

        st.title("Frequently Asked Questions")

        st.divider()

        faqs = [
        ("What is RedditReach?", "RedditReach is a bot that automates the process of sending direct chat messages (DMs) on Reddit to multiple users."),
        
        ("How do I get started with RedditReach?", "To get started, navigate using the sidebar on the left of the application."),
        
        ("How can I add Reddit accounts and proxies?", "In the 'Add Account's and Proxies' section, you can add Reddit accounts and their corresponding proxies."),
        
        ("Where can I get proxies for RedditReach?", "You can get 10 free proxies from [Webshare](https://www.webshare.io/) to use with RedditReach."),
        
        ("What do I need to consider when adding Reddit accounts?", "Before adding an account for sending DMs, confirm its eligibility by sending a manual DM on Reddit. Note that new accounts with very low karma (less than 100) may not be permitted to send chat messages by Reddit."),
        
        ("How can I scrape usernames from Reddit?", "In the 'Send Direct Message's' section, you can choose to scrape usernames from posts, comments, or both in specific subreddits."),
        
        ("Can I send messages with attachments using RedditReach?", "Yes, you can attach images with your messages. Ensure that the attached images are in the 'Images' folder."),
        
        ("How many messages can the bot send at once?", "The bot is designed to send as many message as reddit allows for that particular account (1 message per minute) per Reddit account per 24 Hours. It iterates through the list of usernames and sends messages to each one."),
        
        ("Can I customize the messages I send?", "Yes, you can enter your desired messages, and RedditReach will randomly select a message to send for each direct message."),
        
        ("How do I start sending direct messages with RedditReach?", "Click the 'Start Direct Messaging' button in the 'Send Direct Message's' section to begin sending messages using your configured Reddit accounts and proxies."),
        
        ("What happens if a message fails to send?", "If a message fails to send, RedditReach will skip that message and move on to the next one."),
        
        ("Where can I get further assistance or report issues?", "If you need assistance or have suggestions, you can reach out via email at basitcarry@proton.me or on the [RedditReach Discord server](https://discord.gg/eW5bVTFgss)."),
    ]

        for question, answer in faqs:
            st.info(f"**Q:** {question}\n\n**A:** {answer}")
        
        hyperlink_url = "https://discord.gg/eW5bVTFgss"
        st.info(f'Still Need Help? Contact me [here]({hyperlink_url})')
    
    elif page == "⚠️ License Agreement":

        image = st.image("assets/bg.png")

        st.divider()

        st.info(agreement)