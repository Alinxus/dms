import json
import boto3
from ..automation.instagram import InstagramDMSender
from ..automation.twitter import TwitterDMSender
from ..utils.logger import setup_logger

dynamodb = boto3.resource('dynamodb')
logger = setup_logger()

RECIPIENT_TABLE = 'dm_recipients'

def lambda_handler(event, context):
    body = json.loads(event['body'])
    platform = body['platform']
    message = body['message']
    batch_size = body.get('batch_size', 10)  # Default to 10 if not specified
    
    # You'll need to handle credentials separately, perhaps fetching from a secure store
    credentials = get_credentials(platform)

    sender_class = {
        'instagram': InstagramDMSender,
        'twitter': TwitterDMSender,
    }.get(platform)

    if not sender_class:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Unsupported platform: {platform}'})
        }

    table = dynamodb.Table(RECIPIENT_TABLE)
    response = table.scan(
        FilterExpression='platform = :platform AND #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':platform': platform, ':status': 'pending'},
        Limit=batch_size
    )

    sender = sender_class(credentials)
    sent_count = 0

    for item in response['Items']:
        try:
            sender.send_dm(item['username'], message)
            table.update_item(
                Key={'platform': item['platform'], 'username': item['username']},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'sent'}
            )
            sent_count += 1
        except Exception as e:
            logger.error(f"Error sending DM to {item['username']} on {platform}: {str(e)}")
            table.update_item(
                Key={'platform': item['platform'], 'username': item['username']},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'failed'}
            )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Sent {sent_count} messages')
    }

def get_credentials(platform):
    # Implement secure credential retrieval here
    pass

def lambda_handler(event, context):
    body = json.loads(event['body'])
    platform = body['platform']
    message = body['message']
    batch_size = body.get('batch_size', 10)
    user_id = body['user_id']
    
    try:
        credentials = get_credentials(platform, user_id)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

    if not check_rate_limit(user_id, platform):
        return {
            'statusCode': 429,
            'body': json.dumps({'error': 'Rate limit exceeded'})
        }

    # ... (rest of the function remains the same)

    for item in response['Items']:
        if not check_rate_limit(user_id, platform):
            break
        try:
            sender.send_dm(item['username'], message)
            # ... (update status in DynamoDB)
            sent_count += 1
        except Exception as e:
            # ... (error handling)
             return {
        'statusCode': 200,
        'body': json.dumps(f'Sent {sent_count} messages')
    }
