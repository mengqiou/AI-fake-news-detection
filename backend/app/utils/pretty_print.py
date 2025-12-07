"""
Pretty print utilities for agent execution traces.

Shows agent's thinking process, tool calls, and results in a readable format.
"""

from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


def print_separator(char: str = "=", length: int = 70):
    """Print a separator line."""
    print(char * length)


def print_section(title: str, char: str = "=", length: int = 70):
    """Print a section header."""
    print("\n" + char * length)
    print(title)
    print(char * length)


def print_execution_summary(final_state: Dict[str, Any]):
    """
    Print a summary of agent execution.
    
    Args:
        final_state: The final state from agent.invoke()
    """
    print_section("EXECUTION SUMMARY")
    
    print(f"\nTotal Iterations: {final_state.get('iteration_count', 0)}")
    print(f"Total Messages: {len(final_state.get('messages', []))}")
    print(f"Tool Calls: {len(final_state.get('tool_results', []))}")


def print_tool_history(final_state: Dict[str, Any]):
    """
    Print all tool calls and their results.
    
    Args:
        final_state: The final state from agent.invoke()
    """
    tool_results = final_state.get('tool_results', [])
    
    if not tool_results:
        print("\n(No tools were called)")
        return
    
    print_section("TOOL EXECUTION HISTORY")
    
    for i, tool_result in enumerate(tool_results, 1):
        print(f"\n[Tool Call {i}]")
        print(f"Tool: {tool_result.get('tool_name', 'unknown')}")
        print(f"\nOutput:")
        print(tool_result.get('output', '(no output)'))
        print("-" * 70)


def print_message(msg: Any, index: int, truncate_length: int = 500):
    """
    Print a single message with formatting.
    
    Args:
        msg: The message object
        index: Message number
        truncate_length: Max length before truncating content
    """
    msg_type = type(msg).__name__
    
    # Emoji for different message types
    emoji = {
        "HumanMessage": "👤",
        "AIMessage": "🤖",
        "ToolMessage": "🔧",
        "SystemMessage": "⚙️"
    }.get(msg_type, "📝")
    
    print(f"\n{emoji} [Message {index}] {msg_type}")
    
    # Print content
    if hasattr(msg, 'content'):
        content = str(msg.content)
        if len(content) > truncate_length:
            print(f"{content[:truncate_length]}...")
            print(f"[truncated, {len(content)} chars total]")
        else:
            print(content)
    
    # Show tool calls if present (for AIMessage)
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print(f"\n🔧 Tool Calls Requested: {len(msg.tool_calls)}")
        for tc in msg.tool_calls:
            tool_name = tc.get('name', 'unknown')
            tool_args = tc.get('args', {})
            print(f"  • {tool_name}")
            if tool_args:
                print(f"    Args: {tool_args}")
    
    print("-" * 70)


def print_message_history(final_state: Dict[str, Any], truncate_length: int = 500):
    """
    Print the complete message history showing agent's thinking.
    
    Args:
        final_state: The final state from agent.invoke()
        truncate_length: Max length before truncating message content
    """
    messages = final_state.get('messages', [])
    
    if not messages:
        print("\n(No messages found)")
        return
    
    print_section("MESSAGE HISTORY (Agent's Thinking)")
    
    for i, msg in enumerate(messages, 1):
        print_message(msg, i, truncate_length)


def print_final_response(final_state: Dict[str, Any]):
    """
    Print the final agent response.
    
    Args:
        final_state: The final state from agent.invoke()
    """
    print_section("FINAL AGENT RESPONSE")
    
    messages = final_state.get('messages', [])
    if not messages:
        print("(No response)")
        return
    
    final_message = messages[-1]
    result_content = final_message.content if hasattr(final_message, "content") else str(final_message)
    
    print(result_content)
    print_separator()


def print_agent_execution(
    final_state: Dict[str, Any],
    show_summary: bool = True,
    show_tools: bool = True,
    show_messages: bool = True,
    show_final: bool = True,
    truncate_length: int = 500
):
    """
    Print complete agent execution trace with all details.
    
    This is the main function to use for pretty printing agent results.
    
    Args:
        final_state: The final state from agent.invoke()
        show_summary: Whether to show execution summary
        show_tools: Whether to show tool execution history
        show_messages: Whether to show message history
        show_final: Whether to show final response
        truncate_length: Max length before truncating message content
        
    Example:
        ```python
        from app.utils.pretty_print import print_agent_execution
        
        final_state = agent.invoke(initial_state)
        print_agent_execution(final_state)
        ```
    """
    if show_summary:
        print_execution_summary(final_state)
    
    if show_tools:
        print_tool_history(final_state)
    
    if show_messages:
        print_message_history(final_state, truncate_length)
    
    if show_final:
        print_final_response(final_state)


def print_compact_execution(final_state: Dict[str, Any]):
    """
    Print a compact version of execution - summary and final response only.
    
    Args:
        final_state: The final state from agent.invoke()
        
    Example:
        ```python
        from app.utils.pretty_print import print_compact_execution
        
        final_state = agent.invoke(initial_state)
        print_compact_execution(final_state)
        ```
    """
    print_agent_execution(
        final_state,
        show_summary=True,
        show_tools=False,
        show_messages=False,
        show_final=True
    )


def print_tools_only(final_state: Dict[str, Any]):
    """
    Print only tool execution history.
    
    Args:
        final_state: The final state from agent.invoke()
        
    Example:
        ```python
        from app.utils.pretty_print import print_tools_only
        
        final_state = agent.invoke(initial_state)
        print_tools_only(final_state)
        ```
    """
    print_tool_history(final_state)


# Convenience function aliases
pretty_print = print_agent_execution
compact_print = print_compact_execution
