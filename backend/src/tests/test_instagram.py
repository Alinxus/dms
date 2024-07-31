import pytest
from src.automation.instagram import InstagramDMSender

def test_instagram_dm_sender():
    credentials = {
        'username': 'your_test_username',
        'password': 'your_test_password'
    }
    sender = InstagramDMSender(credentials)
    
    # This is a placeholder test. In a real scenario, you'd use a test account
    # and mock the browser interactions.
    assert isinstance(sender, InstagramDMSender)