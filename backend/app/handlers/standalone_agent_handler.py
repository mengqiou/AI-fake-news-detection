import uuid
from datetime import datetime
from typing import Any, Dict

from ..agents.agent_factory import instantiate_agent, invoke_agent
from ..tools.tool_loader import gather_agent_tools
from ..utils.config_utils import get_agent_by_config_id


def handle_standalone_agent_request(config_id: str, user_input: str) -> Dict[str, Any]:
    """
    Handle a one-off agent workflow request.

    This handler fires a standalone agent that executes its investigation based on:
    - User input
    - System prompt
    - Available tools

    No further user interaction is allowed (unlike conversational agents).

    Args:
        config_id: The agent configuration ID
        user_input: The user's input/query for the agent

    Returns:
        Dictionary containing:
        - success: Boolean indicating success/failure
        - result: Agent's output
        - metadata: Execution metadata
        - execution_id: Unique execution ID

    Raises:
        ValueError: If config_id or user_input is invalid
        RuntimeError: If agent execution fails
    """
    try:
        # Generate unique execution ID
        execution_id = str(uuid.uuid4())

        # Step 1: Get the agent configuration by configId
        agent_config = get_agent_by_config_id(config_id)

        if not agent_config:
            return {
                "success": False,
                "error": f"Agent configuration not found for config_id: {config_id}",
                "result": None,
                "metadata": {},
            }

        # Step 2: Gather all tools (MCP + custom)
        tools = gather_agent_tools(agent_config)

        # Step 3: Instantiate the agent
        agent = instantiate_agent(agent_config, tools)

        # Step 4: Invoke the agent with user input
        execution_result = invoke_agent(agent, user_input)

        # Step 5: Persist the execution history to DynamoDB
        saved_execution_id = _persist_execution_to_dynamodb(
            config_id=config_id,
            execution_id=execution_id,
            user_input=user_input,
            result=execution_result,
        )

        return {
            "success": True,
            "execution_id": saved_execution_id,
            "result": execution_result.get("result"),
            "metadata": execution_result.get("metadata", {}),
        }

    except ValueError as e:
        return {
            "success": False,
            "error": f"Validation error: {str(e)}",
            "result": None,
            "metadata": {},
        }
    except RuntimeError as e:
        return {
            "success": False,
            "error": f"Execution error: {str(e)}",
            "result": None,
            "metadata": {},
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "result": None,
            "metadata": {},
        }


def _persist_execution_to_dynamodb(
    config_id: str, execution_id: str, user_input: str, result: Dict[str, Any]
) -> str:
    """
    Persist agent execution to DynamoDB using execution history commands.

    Args:
        config_id: Agent configuration ID
        execution_id: Unique execution ID
        user_input: User's input
        result: Execution result from invoke_agent

    Returns:
        execution_id where the execution was stored
    """
    from ..db_commands.execution_history_commands import save_execution_history

    execution_id = save_execution_history(
        config_id=config_id,
        execution_id=execution_id,
        user_input=user_input,
        result=result,
    )

    return execution_id
