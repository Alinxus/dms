import boto3
import json
from botocore.exceptions import ClientError

from datetime import datetime, timedelta
from ..config import AWS_REGION, SQS_QUEUE_URL

import logging

from botocore.exceptions import ClientError
from ..config import AWS_REGION, DYNAMODB_TABLE_USERS, DYNAMODB_TABLE_MESSAGES, DYNAMODB_TABLE_ACCOUNTS,DYNAMODB_TABLE_CAMPAIGNS
from ..models.campaign import User, UserCreate
import uuid
from ..models.campaign import Message, MessageCreate
from ..models.campaign import Campaign, CampaignCreate
from ..models.campaign import Account, AccountCreate, AccountResponse
import time
import csv

def read_recipients(file_path):
    recipients = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipients.append({
                'platform': row['platform'],
                'username': row['username']
            })
    return recipients

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
users_table = dynamodb.Table(DYNAMODB_TABLE_USERS)
accounts_table = dynamodb.Table(DYNAMODB_TABLE_ACCOUNTS)
messages_table = dynamodb.Table(DYNAMODB_TABLE_MESSAGES)
campaigns_table = dynamodb.Table(DYNAMODB_TABLE_CAMPAIGNS)

def create_account(account: AccountCreate) -> Account:
    account_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    
    item = {
        'id': account_id,
        'user_id': account.user_id,
        'platform': account.platform,
        'username': account.username,
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    try:
        accounts_table.put_item(Item=item)
        return Account(**item)
    except ClientError as e:
        print(f"Error creating account: {e}")
        raise

def get_user_accounts(user_id: str) -> list[Account]:
    try:
        response = accounts_table.query(
            IndexName='UserIdIndex',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
        return [Account(**item) for item in response['Items']]
    except ClientError as e:
        print(f"Error getting user accounts: {e}")
        return []
    
def get_user_campaigns(user_id: str) -> list[Account]:
    try:
        response = accounts_table.query(
            IndexName='UserIdIndex',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
        return [Campaign(**item) for item in response['Items']]
    except ClientError as e:
        print(f"Error getting user campaign: {e}")
        return []


def create_campaign(campaign: CampaignCreate) -> Campaign:
    campaign_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    
    item = {
        'id': campaign_id,
        'user_id': campaign.user_id,
        'name': campaign.name,
        'message_template': campaign.message_template,
        'status': 'created',
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    try:
        campaigns_table.put_item(Item=item)
        return Campaign(**item)
    except ClientError as e:
        print(f"Error creating campaign: {e}")
        raise
def update_user(user: User) -> User:
    timestamp = str(int(time.time()))
    user.updated_at = timestamp
    
    try:
        users_table.put_item(Item=user.dict())
        return user
    except ClientError as e:
        print(f"Error updating user: {e}")
        return None


def create_user(user: UserCreate) -> User:
    user_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    
    item = {
        'id': user_id,
        'platform': user.platform,
        user_id: user.id,
        'recipient': user.recipient,
        'content': user.content,
        'status': 'queued',
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    try:
        messages_table.put_item(Item=item)
        return Message(**item)
    except ClientError as e:
        print(f"Error creating message: {e}")
        raise


def create_message(message: MessageCreate) -> Message:
    message_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    
    item = {
        'id': message_id,
        'user_id': message.user_id,
        'platform': message.platform,
        'recipient': message.recipient,
        'content': message.content,
        'status': 'queued',
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    try:
        messages_table.put_item(Item=item)
        return Message(**item)
    except ClientError as e:
        print(f"Error creating message: {e}")
        raise

def get_messages_by_user(user_id: str, status: list[str] = None) -> list[Message]:
    try:
        if status:
            response = messages_table.query(
                IndexName='UserStatusIndex',
                KeyConditionExpression='user_id = :uid AND #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':uid': user_id, ':status': status}
            )
        else:
            response = messages_table.query(
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={':uid': user_id}
            )
        
        return [Message(**item) for item in response['Items']]
    except ClientError as e:
        print(f"Error getting messages: {e}")
        return []

def update_message_status(message_id: str, new_status: str) -> Message:
    timestamp = str(int(time.time()))
    
    try:
        response = messages_table.update_item(
            Key={'id': message_id},
            UpdateExpression='SET #status = :status, updated_at = :updated_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': new_status, ':updated_at': timestamp},
            ReturnValues='ALL_NEW'
        )
        return Message(**response['Attributes'])
    except ClientError as e:
        print(f"Error updating message status: {e}")
        return None



def setup_logger():
    logger = logging.getLogger('mass_dm_sender')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

sqs = boto3.client('sqs', region_name=AWS_REGION)

def enqueue_message(message: dict):
    try:
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message)
        )
        return response['MessageId']
    except Exception as e:
        print(f"Error enqueueing message: {e}")
        raise

def dequeue_messages(max_messages: int = 10):
    try:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=20
        )
        return response.get('Messages', [])
    except Exception as e:
        print(f"Error dequeuing messages: {e}")
        raise

def delete_message(receipt_handle: str):
    try:
        sqs.delete_message(
            QueueUrl=SQS_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
    except Exception as e:
        print(f"Error deleting message: {e}")
        raise

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

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        raise ValueError("Secret not found in expected format")

def get_platform_credentials(platform):
    secret_name = f"{platform.lower()}_credentials"
    return get_secret(secret_name)