import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('rate_limits')

RATE_LIMITS = {
    'twitter': 1000,  # Example: 1000 DMs per 24 hours
    'instagram': 500  # Example: 500 DMs per 24 hours
}

def check_rate_limit(user_id, platform):
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    response = table.get_item(
        Key={
            'user_id': user_id,
            'date': start_of_day.isoformat()
        }
    )
    
    if 'Item' not in response:
        table.put_item(
            Item={
                'user_id': user_id,
                'date': start_of_day.isoformat(),
                platform: 0
            }
        )
        return True
    
    current_count = response['Item'].get(platform, 0)
    if current_count >= RATE_LIMITS[platform]:
        return False
    
    table.update_item(
        Key={
            'user_id': user_id,
            'date': start_of_day.isoformat()
        },
        UpdateExpression=f'SET {platform} = {platform} + :inc',
        ExpressionAttributeValues={':inc': 1}
    )
    
    return True