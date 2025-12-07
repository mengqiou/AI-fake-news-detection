from typing import Dict, Any, List, Optional
from decimal import Decimal
from infra.dynamodb_client import get_dynamodb_resource
from datetime import datetime
import os


def convert_decimals_to_float(obj: Any) -> Any:
    """
    Recursively convert Decimal objects to float for JSON serialization.
    
    Args:
        obj: Object that may contain Decimal values
        
    Returns:
        Object with all Decimals converted to floats
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals_to_float(item) for item in obj]
    else:
        return obj


def get_execution_table_name() -> str:
    """Get the DynamoDB execution history table name from environment."""
    return os.getenv("EXECUTION_TABLE", "execution-history")


def save_execution_history(
    config_id: str,
    execution_id: str,
    user_input: str,
    result: Dict[str, Any],
    table_name: str = None
) -> str:
    """
    Save agent execution history to DynamoDB.
    
    Args:
        config_id: Agent configuration ID
        execution_id: Unique execution ID
        user_input: User's input
        result: Execution result from invoke_agent
        table_name: DynamoDB table name (optional, uses env var if not provided)
        
    Returns:
        execution_id that was saved
        
    Raises:
        Exception: If DynamoDB write fails
    """
    dynamodb = get_dynamodb_resource()
    table_name = table_name or get_execution_table_name()
    table = dynamodb.Table(table_name)
    
    # Create execution item
    timestamp = datetime.utcnow().isoformat()
    
    try:
        # Convert any Decimal values to float for proper serialization
        metadata = convert_decimals_to_float(result.get("metadata", {}))
        result_content = convert_decimals_to_float(result.get("result"))
        
        table.put_item(
            Item={
                'execution_id': execution_id,
                'config_id': config_id,
                'user_input': user_input,
                'result': result_content,
                'metadata': metadata,
                'timestamp': timestamp
            }
        )
        return execution_id
    except Exception as e:
        raise Exception(f"Failed to save execution history to DynamoDB: {str(e)}")


def load_execution_history(
    execution_id: str,
    table_name: str = None
) -> Optional[Dict[str, Any]]:
    """
    Load a specific execution history from DynamoDB.
    
    Args:
        execution_id: Unique execution ID
        table_name: DynamoDB table name (optional, uses env var if not provided)
        
    Returns:
        Execution history as dictionary, or None if not found
        
    Raises:
        Exception: If DynamoDB retrieval fails
    """
    dynamodb = get_dynamodb_resource()
    table_name = table_name or get_execution_table_name()
    table = dynamodb.Table(table_name)
    
    try:
        response = table.get_item(Key={'execution_id': execution_id})
        
        if 'Item' not in response:
            return None
        
        return response['Item']
    except Exception as e:
        raise Exception(f"Failed to load execution history from DynamoDB: {str(e)}")


def list_execution_history(
    config_id: str,
    table_name: str = None,
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    List execution history for a specific agent config.
    
    Args:
        config_id: Agent configuration ID
        table_name: DynamoDB table name (optional, uses env var if not provided)
        max_results: Maximum number of results to return
        
    Returns:
        List of execution history dictionaries
        
    Raises:
        Exception: If DynamoDB query fails
    """
    dynamodb = get_dynamodb_resource()
    table_name = table_name or get_execution_table_name()
    table = dynamodb.Table(table_name)
    
    try:
        # Query by config_id using GSI (Global Secondary Index)
        # Note: This requires a GSI on config_id
        response = table.query(
            IndexName='config_id-index',
            KeyConditionExpression='config_id = :config_id',
            ExpressionAttributeValues={
                ':config_id': config_id
            },
            Limit=max_results,
            ScanIndexForward=False  # Sort descending by sort key
        )
        
        executions = response.get('Items', [])
        
        # Sort by timestamp descending (most recent first)
        executions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return executions
    except Exception as e:
        # Fallback to scan if GSI doesn't exist yet
        try:
            response = table.scan(
                FilterExpression='config_id = :config_id',
                ExpressionAttributeValues={
                    ':config_id': config_id
                },
                Limit=max_results
            )
            executions = response.get('Items', [])
            executions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return executions
        except Exception as scan_error:
            raise Exception(f"Failed to list execution history from DynamoDB: {str(scan_error)}")


def delete_execution_history(
    execution_id: str,
    table_name: str = None
) -> None:
    """
    Delete a specific execution history from DynamoDB.
    
    Args:
        execution_id: Unique execution ID
        table_name: DynamoDB table name (optional, uses env var if not provided)
        
    Raises:
        Exception: If DynamoDB deletion fails
    """
    dynamodb = get_dynamodb_resource()
    table_name = table_name or get_execution_table_name()
    table = dynamodb.Table(table_name)
    
    try:
        table.delete_item(Key={'execution_id': execution_id})
    except Exception as e:
        raise Exception(f"Failed to delete execution history from DynamoDB: {str(e)}")
