"""
Example: Using pretty_print utility to display agent execution.

This shows different ways to format agent output.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.agent_factory import instantiate_agent
from app.tools.tool_loader import gather_agent_tools
from app.utils.config_utils import get_agent_by_config_id
from app.utils.pretty_print import (print_agent_execution,
                                    print_compact_execution, print_section,
                                    print_tools_only)
from langchain_core.messages import HumanMessage


def example_full_trace():
    """Example 1: Full execution trace."""
    print_section("EXAMPLE 1: Full Execution Trace", "=", 80)

    # Setup
    agent_config = get_agent_by_config_id("fake-news-detector-v1")
    tools = gather_agent_tools(agent_config)
    agent = instantiate_agent(agent_config, tools)

    # Run agent
    initial_state = {
        "messages": [HumanMessage(content="Is '5G causes COVID' true?")],
        "user_input": "Is '5G causes COVID' true?",
        "tool_results": [],
        "final_output": "",
        "iteration_count": 0,
    }

    final_state = agent.invoke(initial_state)

    # Print everything
    print_agent_execution(final_state)


def example_compact():
    """Example 2: Compact output."""
    print_section("EXAMPLE 2: Compact Output (Summary + Final Only)", "=", 80)

    agent_config = get_agent_by_config_id("fake-news-detector-v1")
    tools = gather_agent_tools(agent_config)
    agent = instantiate_agent(agent_config, tools)

    initial_state = {
        "messages": [HumanMessage(content="Verify: Drinking bleach cures diseases")],
        "user_input": "Verify: Drinking bleach cures diseases",
        "tool_results": [],
        "final_output": "",
        "iteration_count": 0,
    }

    final_state = agent.invoke(initial_state)

    # Compact print
    print_compact_execution(final_state)


def example_tools_only():
    """Example 3: Tools only."""
    print_section("EXAMPLE 3: Tool Execution Only", "=", 80)

    agent_config = get_agent_by_config_id("fake-news-detector-v1")
    tools = gather_agent_tools(agent_config)
    agent = instantiate_agent(agent_config, tools)

    initial_state = {
        "messages": [HumanMessage(content="Check claim: Moon landing was faked")],
        "user_input": "Check claim: Moon landing was faked",
        "tool_results": [],
        "final_output": "",
        "iteration_count": 0,
    }

    final_state = agent.invoke(initial_state)

    # Just tools
    print_tools_only(final_state)


def example_custom():
    """Example 4: Custom combination."""
    print_section("EXAMPLE 4: Custom Combination", "=", 80)

    agent_config = get_agent_by_config_id("fake-news-detector-v1")
    tools = gather_agent_tools(agent_config)
    agent = instantiate_agent(agent_config, tools)

    initial_state = {
        "messages": [HumanMessage(content="Is this fake: NASA found aliens")],
        "user_input": "Is this fake: NASA found aliens",
        "tool_results": [],
        "final_output": "",
        "iteration_count": 0,
    }

    final_state = agent.invoke(initial_state)

    # Custom: Only summary, tools, and final
    print_agent_execution(
        final_state,
        show_summary=True,
        show_tools=True,
        show_messages=False,  # Skip message history
        show_final=True,
        truncate_length=300,
    )


def main():
    """Run examples."""
    print("\n" + "=" * 80)
    print("PRETTY PRINT UTILITY EXAMPLES")
    print("=" * 80)
    print("\nThis demonstrates different ways to format agent output.\n")

    # Choose which example to run
    print("Examples:")
    print("  1. Full trace (everything)")
    print("  2. Compact (summary + final)")
    print("  3. Tools only")
    print("  4. Custom combination")
    print("  5. Run all examples")

    choice = input("\nChoice (1-5): ").strip()

    if choice == "1":
        example_full_trace()
    elif choice == "2":
        example_compact()
    elif choice == "3":
        example_tools_only()
    elif choice == "4":
        example_custom()
    elif choice == "5":
        example_full_trace()
        input("\nPress Enter for next example...")
        example_compact()
        input("\nPress Enter for next example...")
        example_tools_only()
        input("\nPress Enter for next example...")
        example_custom()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExited by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
