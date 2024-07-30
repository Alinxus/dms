import csv
import io
import boto3

s3 = boto3.client('s3')

def process_csv(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    csv_content = response['Body'].read().decode('utf-8')
    csv_file = io.StringIO(csv_content)
    csv_reader = csv.DictReader(csv_file)
    
    recipients = []
    for row in csv_reader:
        recipients.append({
            'platform': row['platform'],
            'username': row['username']
        })
    
    return recipients