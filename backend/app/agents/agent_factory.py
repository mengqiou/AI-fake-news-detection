from typing import Any, Dict, Optional
from ..entity.AgentConfig import AgentConfig
from .agent_workflow import create_agent_workflow
from langchain_aws import ChatBedrock


def instantiate_agent(agent_config: AgentConfig, tools: Dict[str, Any]) -> Any:
    """
    Instantiate an agent from configuration using LangGraph StateGraph.
    
    Args:
        agent_config: The agent configuration
        tools: Dictionary of available tools (MCP + custom)
        
    Returns:
        Initialized LangGraph agent workflow (compiled graph)
        
    Raises:
        ValueError: If agent_config is invalid
    """
    if not agent_config:
        raise ValueError("agent_config cannot be None")
    
    # 1. Load the system prompt from DynamoDB
    from ..db_commands.prompt_commands import load_prompt
    
    system_prompt = load_prompt(agent_config.prompt_id)
    
    # 2. Initialize the LLM based on agent config
    if agent_config.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model=agent_config.model_id,
            temperature=float(agent_config.temperature),  # Ensure float for JSON serialization
            max_tokens=int(agent_config.max_tokens)
        )
    elif agent_config.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=agent_config.model_id,
            temperature=float(agent_config.temperature),  # Ensure float for JSON serialization
            max_tokens=int(agent_config.max_tokens)
        )
    elif agent_config.llm_provider == "bedrock":
        llm = ChatBedrock(
            model_id=agent_config.model_id,
            model_kwargs={
                "temperature": float(agent_config.temperature),  # Ensure float for JSON serialization
                "max_tokens": int(agent_config.max_tokens)
            }
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {agent_config.llm_provider}")
    
    # 3. Bind tools to LLM if any tools are available
    if tools:
        tool_list = list(tools.values())
        llm = llm.bind_tools(tool_list)
    
    # 4. Create the StateGraph workflow 
    agent_workflow = create_agent_workflow(
        llm=llm,
        tools=tools,
        system_prompt=system_prompt,
        max_iterations=agent_config.max_iterations
    )
    
    return agent_workflow


def invoke_agent(agent: Any, user_input: str) -> Dict[str, Any]:
    """
    Execute the agent with user input and return results.
    
    Args:
        agent: The instantiated LangGraph agent
        user_input: User's input/query for the agent
        
    Returns:
        Dictionary containing:
        - result: Agent's response/output
        - metadata: Execution metadata (steps, tool calls, etc.)
        
    Raises:
        ValueError: If user_input is empty
        RuntimeError: If agent execution fails
    """
    if not user_input:
        raise ValueError("user_input cannot be empty")
    
    if not agent:
        raise ValueError("agent cannot be None")
    
    try:
        # Prepare initial state for the StateGraph
        from langchain_core.messages import HumanMessage
        
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_input": user_input,
            "tool_results": [],
            "final_output": "",
            "iteration_count": 0
        }
        
        # Invoke the workflow (the agent is the compiled graph)
        final_state = agent.invoke(initial_state)

        # TODO: persist the whole agent iteration like tool calls, messages, etc. to AWS S3
        
        # Extract the final response
        final_message = final_state["messages"][-1]
        result_content = final_message.content if hasattr(final_message, "content") else str(final_message)
        
        # Format output for persistence to AWS S3
        return {
            "result": result_content,
            "metadata": {
                "iterations": final_state.get("iteration_count", 0),
                "tool_calls": len(final_state.get("tool_results", [])),
                "tool_results": final_state.get("tool_results", []),
                "total_messages": len(final_state.get("messages", []))
            },
            "full_state": final_state
        }
        
    except Exception as e:
        raise RuntimeError(f"Agent execution failed: {str(e)}") from e