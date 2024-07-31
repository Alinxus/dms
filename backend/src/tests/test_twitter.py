import pytest
from src.automation.twitter import TwitterDMSender

def test_twitter_dm_sender():
    credentials = {
        'username': 'your_test_twitter_username',
        'password': 'your_test_twitter_password'
    }
    sender = TwitterDMSender(credentials)
    
    # This is a placeholder test. In a real scenario, you'd use a test account
    # and mock the browser interactions.
    assert isinstance(sender, TwitterDMSender)