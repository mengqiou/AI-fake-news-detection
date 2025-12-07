from typing import Optional, List
from decimal import Decimal
from infra.dynamodb_client import get_dynamodb_resource
from ..entity.AgentConfig import AgentConfig, SubAgentConfig, KnowledgeBaseConfig
import os


def get_table_name() -> str:
    """Get the DynamoDB table name from environment."""
    return os.getenv("AGENT_CONFIG_TABLE", "agent-configs")


def create_agent_config(agent_config: AgentConfig) -> None:
    """
    Create a new agent configuration in DynamoDB.
    
    Args:
        agent_config: The agent configuration to create
        
    Raises:
        Exception: If creation fails
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(get_table_name())
    
    try:
        # Convert dataclass to dict (convert floats to Decimal for DynamoDB)
        item = {
            'config_id': agent_config.config_id,
            'name': agent_config.name,
            'description': agent_config.description,
            'tools': agent_config.tools,
            'prompt_id': agent_config.prompt_id,
            'knowledge_base': {
                'enabled': agent_config.knowledge_base.enabled,
                'vector_store': agent_config.knowledge_base.vector_store,
                'index_name': agent_config.knowledge_base.index_name,
                'embedding_model': agent_config.knowledge_base.embedding_model,
                'top_k': agent_config.knowledge_base.top_k
            } if agent_config.knowledge_base else None,
            'llm_provider': agent_config.llm_provider,
            'model_id': agent_config.model_id,
            'temperature': Decimal(str(agent_config.temperature)),  # Convert float to Decimal
            'max_tokens': agent_config.max_tokens,
            'max_iterations': agent_config.max_iterations,
            'sub_agents': [
                {
                    'name': sa.name,
                    'description': sa.description,
                    'config_id': sa.config_id,
                    'agent_config_id': sa.agent_config_id,
                    'tools': sa.tools,
                    'prompt_id': sa.prompt_id,
                    'knowledge_base': {
                        'enabled': sa.knowledge_base.enabled,
                        'vector_store': sa.knowledge_base.vector_store,
                        'index_name': sa.knowledge_base.index_name,
                        'embedding_model': sa.knowledge_base.embedding_model,
                        'top_k': sa.knowledge_base.top_k
                    } if sa.knowledge_base else None,
                    'llm_provider': sa.llm_provider,
                    'model_id': sa.model_id,
                    'temperature': Decimal(str(sa.temperature)),  # Convert float to Decimal
                    'max_tokens': sa.max_tokens,
                    'max_iterations': sa.max_iterations
                }
                for sa in agent_config.sub_agents
            ]
        }
        
        table.put_item(Item=item)
    except Exception as e:
        raise Exception(f"Failed to create agent config: {str(e)}")


def get_agent_config(config_id: str) -> Optional[AgentConfig]:
    """
    Retrieve an agent configuration by config_id.
    
    Args:
        config_id: The agent configuration ID
        
    Returns:
        AgentConfig if found, None otherwise
        
    Raises:
        Exception: If retrieval fails
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(get_table_name())
    
    try:
        response = table.get_item(Key={'config_id': config_id})
        
        if 'Item' not in response:
            return None
        
        item = response['Item']
        
        # Convert knowledge_base dict to KnowledgeBaseConfig
        kb = item.get('knowledge_base')
        knowledge_base = KnowledgeBaseConfig(
            enabled=kb.get('enabled', False),
            vector_store=kb.get('vector_store', 'chroma'),
            index_name=kb.get('index_name', ''),
            embedding_model=kb.get('embedding_model', 'text-embedding-3-small'),
            top_k=kb.get('top_k', 5)
        ) if kb else None
        
        # Convert sub_agents dicts to SubAgentConfig objects
        sub_agents = [
            SubAgentConfig(
                name=sa['name'],
                description=sa['description'],
                config_id=sa['config_id'],
                agent_config_id=sa['agent_config_id'],
                tools=sa.get('tools', []),
                prompt_id=sa.get('prompt_id', ''),
                knowledge_base=KnowledgeBaseConfig(
                    enabled=sa['knowledge_base'].get('enabled', False),
                    vector_store=sa['knowledge_base'].get('vector_store', 'chroma'),
                    index_name=sa['knowledge_base'].get('index_name', ''),
                    embedding_model=sa['knowledge_base'].get('embedding_model', 'text-embedding-3-small'),
                    top_k=sa['knowledge_base'].get('top_k', 5)
                ) if sa.get('knowledge_base') else None,
                llm_provider=sa.get('llm_provider', 'anthropic'),
                model_id=sa.get('model_id', 'claude-3-5-sonnet-20241022'),
                temperature=float(sa.get('temperature', 0.7)),  # Convert Decimal to float
                max_tokens=sa.get('max_tokens', 4096),
                max_iterations=sa.get('max_iterations', 10)
            )
            for sa in item.get('sub_agents', [])
        ]
        
        # Convert to AgentConfig dataclass
        return AgentConfig(
            name=item['name'],
            description=item['description'],
            config_id=item['config_id'],
            tools=item.get('tools', []),
            prompt_id=item.get('prompt_id', ''),
            sub_agents=sub_agents,
            knowledge_base=knowledge_base,
            llm_provider=item.get('llm_provider', 'anthropic'),
            model_id=item.get('model_id', 'claude-3-5-sonnet-20241022'),
            temperature=float(item.get('temperature', 0.7)),  # Convert Decimal to float
            max_tokens=item.get('max_tokens', 4096),
            max_iterations=item.get('max_iterations', 10)
        )
    except Exception as e:
        raise Exception(f"Failed to get agent config: {str(e)}")


def update_agent_config(agent_config: AgentConfig) -> None:
    """
    Update an existing agent configuration.
    
    Args:
        agent_config: The agent configuration to update
        
    Raises:
        Exception: If update fails
    """
    # TODO: Implement update logic
    # For now, just overwrite with put_item
    create_agent_config(agent_config)


def delete_agent_config(config_id: str) -> None:
    """
    Delete an agent configuration.
    
    Args:
        config_id: The agent configuration ID to delete
        
    Raises:
        Exception: If deletion fails
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(get_table_name())
    
    try:
        table.delete_item(Key={'config_id': config_id})
    except Exception as e:
        raise Exception(f"Failed to delete agent config: {str(e)}")


def list_agent_configs() -> List[AgentConfig]:
    """
    List all agent configurations.
    
    Returns:
        List of AgentConfig objects
        
    Raises:
        Exception: If listing fails
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(get_table_name())
    
    try:
        response = table.scan()
        items = response.get('Items', [])
        
        configs = []
        for item in items:
            # Convert knowledge_base dict to KnowledgeBaseConfig
            kb = item.get('knowledge_base')
            knowledge_base = KnowledgeBaseConfig(
                enabled=kb.get('enabled', False),
                vector_store=kb.get('vector_store', 'chroma'),
                index_name=kb.get('index_name', ''),
                embedding_model=kb.get('embedding_model', 'text-embedding-3-small'),
                top_k=kb.get('top_k', 5)
            ) if kb else None
            
            sub_agents = [
                SubAgentConfig(
                    name=sa['name'],
                    description=sa['description'],
                    config_id=sa['config_id'],
                    agent_config_id=sa['agent_config_id'],
                    tools=sa.get('tools', []),
                    prompt_id=sa.get('prompt_id', ''),
                    knowledge_base=KnowledgeBaseConfig(
                        enabled=sa['knowledge_base'].get('enabled', False),
                        vector_store=sa['knowledge_base'].get('vector_store', 'chroma'),
                        index_name=sa['knowledge_base'].get('index_name', ''),
                        embedding_model=sa['knowledge_base'].get('embedding_model', 'text-embedding-3-small'),
                        top_k=sa['knowledge_base'].get('top_k', 5)
                    ) if sa.get('knowledge_base') else None,
                    llm_provider=sa.get('llm_provider', 'anthropic'),
                    model_id=sa.get('model_id', 'claude-3-5-sonnet-20241022'),
                    temperature=float(sa.get('temperature', 0.7)),  # Convert Decimal to float
                    max_tokens=sa.get('max_tokens', 4096),
                    max_iterations=sa.get('max_iterations', 10)
                )
                for sa in item.get('sub_agents', [])
            ]
            
            configs.append(AgentConfig(
                name=item['name'],
                description=item['description'],
                config_id=item['config_id'],
                tools=item.get('tools', []),
                prompt_id=item.get('prompt_id', ''),
                sub_agents=sub_agents,
                knowledge_base=knowledge_base,
                llm_provider=item.get('llm_provider', 'anthropic'),
                model_id=item.get('model_id', 'claude-3-5-sonnet-20241022'),
                temperature=float(item.get('temperature', 0.7)),  # Convert Decimal to float
                max_tokens=item.get('max_tokens', 4096),
                max_iterations=item.get('max_iterations', 10)
            ))
        
        return configs
    except Exception as e:
        raise Exception(f"Failed to list agent configs: {str(e)}")
