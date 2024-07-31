from automation.instagram import InstagramDMSender
from automation.twitter import TwitterDMSender
from utils.csv_handler import read_recipients
from utils.logger import setup_logger

logger = setup_logger()

def main():
    csv_path = input("Enter the path to your CSV file: ")
    message = input("Enter the message you want to send: ")
    
    recipients = read_recipients(csv_path)
    
    instagram_credentials = {
        'username': input("Enter your Instagram username: "),
        'password': input("Enter your Instagram password: ")
    }
    
    twitter_credentials = {
        'username': input("Enter your Twitter username: "),
        'password': input("Enter your Twitter password: ")
    }
    
    instagram_sender = InstagramDMSender(instagram_credentials)
    twitter_sender = TwitterDMSender(twitter_credentials)
    
    for recipient in recipients:
        try:
            if recipient['platform'].lower() == 'instagram':
                instagram_sender.send_dm(recipient['username'], message)
            elif recipient['platform'].lower() == 'twitter':
                twitter_sender.send_dm(recipient['username'], message)
            else:
                logger.warning(f"Unsupported platform: {recipient['platform']} for user {recipient['username']}")
            
            logger.info(f"Sent message to {recipient['username']} on {recipient['platform']}")
        except Exception as e:
            logger.error(f"Failed to send message to {recipient['username']} on {recipient['platform']}: {str(e)}")

if __name__ == "__main__":
    main()