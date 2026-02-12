from typing import Optional

from ..db_commands.agent_config_commands import get_agent_config
from ..entity.AgentConfig import AgentConfig


def get_agent_by_config_id(config_id: str) -> Optional[AgentConfig]:
    """
    Retrieve an agent configuration by its config ID.

    Args:
        config_id: The unique identifier for the agent configuration

    Returns:
        AgentConfig if found, None otherwise

    Raises:
        ValueError: If config_id is empty or invalid
    """
    if not config_id:
        raise ValueError("config_id cannot be empty")

    return get_agent_config(config_id)
