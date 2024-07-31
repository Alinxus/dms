import boto3
import json
from botocore.exceptions import ClientError

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