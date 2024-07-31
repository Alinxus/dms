# backend/src/lambda_functions/get_session_data.py

import json
from automation.instagram import InstagramAutomation
from automation.twitter import TwitterDmSender
from automation.linkedin import LinkedInAutomation

def lambda_handler(event, context):
    # Parse input
    body = json.loads(event['body'])
    platform = body['platform']
    username = body['username']
    password = body['password']
    
    # Initialize appropriate automation class
    if platform == 'instagram':
        automation = InstagramAutomation(username, password)
    elif platform == 'twitter':
        automation = TwitterDmSender(username, password)
    elif platform == 'linkedin':
        automation = LinkedInAutomation(username, password)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid platform specified')
        }
    
    try:
        # Setup browser
        automation.setup_browser()
        
        # Login
        automation.login()
        
        # Get session data
        session_data = automation.get_session_data()
        
        return {
            'statusCode': 200,
            'body': json.dumps(session_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error getting session data: {str(e)}')
        }
    finally:
        # Clean up
        automation.close()