# backend/src/lambda_functions/process_queue.py

import json
from ..utils.queue_manager import dequeue_messages, delete_message
from ..utils.db_operations import update_message_status
from ..config import RATE_LIMIT_MESSAGES_PER_MINUTE
import boto3
import time

lambda_client = boto3.client('lambda')

def process_queue(event, context):
    try:
        messages = dequeue_messages(RATE_LIMIT_MESSAGES_PER_MINUTE)
        
        for message in messages:
            message_body = json.loads(message['Body'])
            
            # Invoke the send_dm Lambda function asynchronously
            lambda_client.invoke(
                FunctionName='send_dm',
                InvocationType='Event',
                Payload=json.dumps({'Records': [{'body': json.dumps(message_body)}]})
            )
            
            # Delete the message from the queue
            delete_message(message['ReceiptHandle'])
            
            # Update message status to 'processing'
            update_message_status(message_body['message_id'], 'processing')
            
            # Sleep to respect rate limits
            time.sleep(60 / RATE_LIMIT_MESSAGES_PER_MINUTE)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Processed {len(messages)} messages'})
        }
    except Exception as e:
        print(f"Error processing queue: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def lambda_handler(event, context):
    return process_queue(event, context)