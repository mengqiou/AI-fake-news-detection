from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class KnowledgeBaseConfig:
    """
    Configuration for agent's knowledge base (for RAG).
    """

    enabled: bool = False
    vector_store: str = "chroma"  # "chroma", "pinecone", "qdrant"
    index_name: str = ""
    embedding_model: str = "text-embedding-3-small"
    top_k: int = 5  # Number of documents to retrieve


@dataclass
class SubAgentConfig:
    """
    Configuration for a sub-agent.
    Note: A subagent should be a leaf agent and not have any subagents.
    """

    name: str
    description: str
    config_id: str
    agent_config_id: str  # Reference to the parent agent's configId
    tools: List[str] = field(default_factory=list)
    prompt_id: str = ""
    knowledge_base: Optional[KnowledgeBaseConfig] = None

    # LLM Configuration
    llm_provider: str = "anthropic"  # "anthropic", "openai", or "bedrock"
    model_id: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 4096
    max_iterations: int = 10


@dataclass
class AgentConfig:
    """
    Configuration for an agent.
    """

    name: str
    description: str
    config_id: str
    tools: List[str] = field(default_factory=list)
    prompt_id: str = ""
    sub_agents: List[SubAgentConfig] = field(default_factory=list)
    knowledge_base: Optional[KnowledgeBaseConfig] = None

    # LLM Configuration
    llm_provider: str = "anthropic"  # "anthropic", "openai", or "bedrock"
    model_id: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 4096
    max_iterations: int = 10  # Max agent loop iterations
