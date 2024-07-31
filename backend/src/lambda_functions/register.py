# backend/src/lambda_functions/register.py

import json
from ..utils.db_operations import create_user
from ..utils.auth import get_password_hash
from ..models.user import UserCreate

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_create = UserCreate(**body)
        password_hash = get_password_hash(user_create.password)
        user = create_user(user_create, password_hash)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'User created successfully',
                'user_id': user.id
            })
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }