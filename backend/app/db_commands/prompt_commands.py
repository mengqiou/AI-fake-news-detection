from infra.dynamodb_client import get_dynamodb_resource
import os


def get_prompts_table_name() -> str:
    """Get the DynamoDB prompts table name from environment."""
    return os.getenv("PROMPTS_TABLE", "ai-prompts")


def save_prompt(prompt_id: str, content: str, table_name: str = None) -> None:
    """
    Save a prompt to DynamoDB.
    
    Args:
        prompt_id: The prompt identifier (e.g., "fake-news-detector-v1")
        content: The prompt content to save
        table_name: DynamoDB table name (optional, uses env var if not provided)
        
    Raises:
        Exception: If DynamoDB write fails
    """
    dynamodb = get_dynamodb_resource()
    table_name = table_name or get_prompts_table_name()
    table = dynamodb.Table(table_name)
    
    try:
        table.put_item(
            Item={
                'prompt_id': prompt_id,
                'content': content,
                'prompt_type': 'agent'
            }
        )
    except Exception as e:
        raise Exception(f"Failed to save prompt {prompt_id} to DynamoDB: {str(e)}")


def load_prompt(prompt_id: str, table_name: str = None) -> str:
    """
    Load a prompt from DynamoDB by prompt_id.
    
    Args:
        prompt_id: The prompt identifier (e.g., "fake-news-detector-v1")
        table_name: DynamoDB table name (optional, uses env var if not provided)
        
    Returns:
        The prompt content as string
        
    Raises:
        Exception: If prompt not found or DynamoDB error
    """
    dynamodb = get_dynamodb_resource()
    table_name = table_name or get_prompts_table_name()
    table = dynamodb.Table(table_name)
    
    try:
        response = table.get_item(Key={'prompt_id': prompt_id})
        
        if 'Item' not in response:
            raise Exception(f"Prompt {prompt_id} not found")
        
        return response['Item']['content']
    except Exception as e:
        raise Exception(f"Failed to load prompt {prompt_id} from DynamoDB: {str(e)}")
