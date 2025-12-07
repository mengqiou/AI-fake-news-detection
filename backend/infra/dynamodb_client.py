import boto3
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_dynamodb_client():
    """
    Get DynamoDB client.
    
    Returns:
        boto3 DynamoDB client
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client('dynamodb', region_name=region)


def get_dynamodb_resource():
    """
    Get DynamoDB resource (higher-level interface).
    
    Returns:
        boto3 DynamoDB resource
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    return boto3.resource('dynamodb', region_name=region)
