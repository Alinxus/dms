# backend/src/lambda_functions/login.py

import json
from ..utils.db_operations import get_user_by_email
from ..utils.auth import verify_password, create_access_token
from ..models.user import UserLogin

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_login = UserLogin(**body)
        user = get_user_by_email(user_login.email)
        
        if not user or not verify_password(user_login.password, user.password_hash):
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid email or password'})
            }
        
        access_token = create_access_token(user)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'access_token': access_token,
                'token_type': 'bearer'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }