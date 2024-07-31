# backend/src/utils/queue_manager.py

import boto3
import json
from ..config import AWS_REGION, SQS_QUEUE_URL

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