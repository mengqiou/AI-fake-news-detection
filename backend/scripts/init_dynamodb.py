#!/usr/bin/env python3
"""
Initialize DynamoDB tables for the fake news detection system.

Creates the required DynamoDB tables:
- agent-configs: Agent configuration storage
- ai-prompts: System prompt storage
- execution-history: Agent execution logs

Usage:
    python scripts/init_dynamodb.py
"""
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

def create_table_if_not_exists(dynamodb_resource, table_name, key_schema, attribute_definitions):
    """Helper to create table if it doesn't exist"""
    try:
        table = dynamodb_resource.Table(table_name)
        table.load()
        print(f"   ✓ Table '{table_name}' already exists")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"   Creating table '{table_name}'...")
            table = dynamodb_resource.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
            print(f"   ✓ Table '{table_name}' created successfully")
            return table
        else:
            raise

def test_dynamodb():
    """Test DynamoDB access and create tables"""
    print("=" * 60)
    print("Testing DynamoDB and Creating Tables")
    print("=" * 60)
    
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    dynamodb = boto3.client('dynamodb', region_name=aws_region)
    dynamodb_resource = boto3.resource('dynamodb', region_name=aws_region)
    
    # Get table names from environment
    agent_config_table = os.getenv('AGENT_CONFIG_TABLE', 'agent-configs')
    prompts_table = os.getenv('PROMPTS_TABLE', 'ai-prompts')
    execution_table = os.getenv('EXECUTION_TABLE', 'execution-history')
    
    print(f"\nAWS Region: {aws_region}")
    print(f"Tables to create:")
    print(f"  - {agent_config_table}")
    print(f"  - {prompts_table}")
    print(f"  - {execution_table}")
    
    # Test 1: List tables permission
    print(f"\n1. Testing ListTables permission...")
    try:
        response = dynamodb.list_tables()
        tables = response.get('TableNames', [])
        print(f"   ✓ Can list tables ({len(tables)} found)")
    except ClientError as e:
        print(f"   ❌ ListTables failed: {e}")
        return False
    
    # Test 2: Create agent-configs table
    print(f"\n2. Creating/Checking agent-configs table...")
    try:
        create_table_if_not_exists(
            dynamodb_resource,
            agent_config_table,
            key_schema=[
                {'AttributeName': 'config_id', 'KeyType': 'HASH'}
            ],
            attribute_definitions=[
                {'AttributeName': 'config_id', 'AttributeType': 'S'}
            ]
        )
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 3: Create prompts table
    print(f"\n3. Creating/Checking prompts table...")
    try:
        create_table_if_not_exists(
            dynamodb_resource,
            prompts_table,
            key_schema=[
                {'AttributeName': 'prompt_id', 'KeyType': 'HASH'}
            ],
            attribute_definitions=[
                {'AttributeName': 'prompt_id', 'AttributeType': 'S'}
            ]
        )
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 4: Create execution-history table
    print(f"\n4. Creating/Checking execution-history table...")
    try:
        create_table_if_not_exists(
            dynamodb_resource,
            execution_table,
            key_schema=[
                {'AttributeName': 'execution_id', 'KeyType': 'HASH'}
            ],
            attribute_definitions=[
                {'AttributeName': 'execution_id', 'AttributeType': 'S'}
            ]
        )
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 5: Test read/write operations
    print(f"\n5. Testing read/write operations...")
    try:
        # Test agent-configs table
        table = dynamodb_resource.Table(agent_config_table)
        test_item = {
            'config_id': 'test-connection-123',
            'name': 'Test Config',
            'description': 'Connection test'
        }
        table.put_item(Item=test_item)
        print(f"   ✓ Successfully wrote to {agent_config_table}")
        
        response = table.get_item(Key={'config_id': 'test-connection-123'})
        if 'Item' in response:
            print(f"   ✓ Successfully read from {agent_config_table}")
        
        table.delete_item(Key={'config_id': 'test-connection-123'})
        print(f"   ✓ Test data cleaned up")
        
    except ClientError as e:
        print(f"   ❌ Read/write test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All DynamoDB Tests Passed!")
    print("=" * 60)
    print("\nTables created:")
    print(f"  ✓ {agent_config_table}")
    print(f"  ✓ {prompts_table}")
    print(f"  ✓ {execution_table}")
    return True


if __name__ == "__main__":
    success = test_dynamodb()
    exit(0 if success else 1)
