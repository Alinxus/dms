# backend/src/utils/db_operations.py

import boto3
from botocore.exceptions import ClientError
from ..config import AWS_REGION, DYNAMODB_TABLE_USERS, DYNAMODB_TABLE_MESSAGES
from ..models.user import User, UserCreate
import uuid
from ..models.message import Message, MessageCreate
from ..models.campaign import Campaign, CampaignCreate
import time

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

def get_user_accounts(user_id: str) -> List[Account]:
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

def get_messages_by_user(user_id: str, status: Optional[str] = None) -> List[Message]:
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

