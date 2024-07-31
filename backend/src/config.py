# backend/src/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# DynamoDB Tables
DYNAMODB_TABLE_USERS = os.getenv('DYNAMODB_TABLE_USERS', 'mass_dm_sender_users')
DYNAMODB_TABLE_ACCOUNTS = os.getenv('DYNAMODB_TABLE_ACCOUNTS', 'mass_dm_sender_accounts')
DYNAMODB_TABLE_MESSAGES = os.getenv('DYNAMODB_TABLE_MESSAGES', 'mass_dm_sender_messages')
DYNAMODB_TABLE_CAMPAIGNS = os.getenv('DYNAMODB_TABLE_CAMPAIGNS', 'mass_dm_sender_campaigns')

# Authentication
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = 60 * 60 * 24  # 24 hours

# SQS Queues
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Pricing Tiers
PRICING_TIERS = {
    'basic': {
        'max_accounts': 3,
        'max_messages_per_day': 100,
        'price': 9.99
    },
    'pro': {
        'max_accounts': 10,
        'max_messages_per_day': 500,
        'price': 29.99
    },
    'enterprise': {
        'max_accounts': 50,
        'max_messages_per_day': 2000,
        'price': 99.99
    }
}

# Rate Limiting
RATE_LIMIT_MESSAGES_PER_MINUTE = 10

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')