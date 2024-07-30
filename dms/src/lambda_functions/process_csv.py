import json
import boto3
from ..utils.csv_handler import process_csv
from ..utils.logger import setup_logger

dynamodb = boto3.resource('dynamodb')
logger = setup_logger()

RECIPIENT_TABLE = 'dm_recipients'

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        recipients = process_csv(bucket, key)
        
        table = dynamodb.Table(RECIPIENT_TABLE)
        
        with table.batch_writer() as batch:
            for recipient in recipients:
                batch.put_item(Item={
                    'platform': recipient['platform'],
                    'username': recipient['username'],
                    'status': 'pending'
                })
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Processed {len(recipients)} recipients')
        }
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }