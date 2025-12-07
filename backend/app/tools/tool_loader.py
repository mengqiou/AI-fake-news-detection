from typing import List, Dict, Any
from ..entity.AgentConfig import AgentConfig


def load_mcp_tools(tool_names: List[str]) -> Dict[str, Any]:
    """
    Load MCP (Model Context Protocol) tools.
    
    Args:
        tool_names: List of MCP tool names to load
        
    Returns:
        Dictionary of loaded MCP tools
    """
    # TODO: Implement MCP tool loading
    # - Connect to MCP server
    # - Fetch available tools
    # - Filter by tool_names
    return {}


def load_custom_tools(tool_names: List[str]) -> Dict[str, Any]:
    """
    Load custom/internal tools.
    
    Args:
        tool_names: List of custom tool names to load
        
    Returns:
        Dictionary of loaded custom tools
    """
    from .search_tool import search_internet
    from .summary_tool import summary_long_text
    from .platform_verification_tool import verify_on_platform
    
    # Available custom tools
    available_tools = {
        "search_internet": search_internet,
        "summary_long_text": summary_long_text,
        "verify_on_platform": verify_on_platform,
    }
    
    # Filter by requested tool names, or return all if empty
    if not tool_names:
        return available_tools
    
    loaded_tools = {}
    for tool_name in tool_names:
        if tool_name in available_tools:
            loaded_tools[tool_name] = available_tools[tool_name]
    
    return loaded_tools


def gather_agent_tools(agent_config: AgentConfig) -> Dict[str, Any]:
    """
    Gather all tools that the agent has access to.
    Combines both MCP tools and custom tools.
    
    Args:
        agent_config: The agent configuration containing tool names
        
    Returns:
        Dictionary of all available tools for the agent
    """
    all_tools = {}
    
    # Load MCP tools
    mcp_tools = load_mcp_tools(agent_config.tools)
    all_tools.update(mcp_tools)
    
    # Load custom tools
    custom_tools = load_custom_tools(agent_config.tools)
    all_tools.update(custom_tools)
    
    return all_tools
