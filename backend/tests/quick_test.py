"""
Quick test script for fake news detection agent.

This is a minimal test to quickly verify the agent is working.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.handlers.standalone_agent_handler import \
    handle_standalone_agent_request
from app.utils.pretty_print import (print_message, print_section,
                                    print_separator, print_tool_history)


def quick_test():
    """Run a quick test with a simple fake news example."""

    print("\n" + "=" * 60)
    print("QUICK TEST: Fake News Detection Agent")
    print("=" * 60 + "\n")

    # Simple fake news example
    user_input = """
Please analyze this news for fake news or misinformation:

PLATFORM: Twitter
CONTENT: "BREAKING: Drinking bleach cures COVID-19! Scientists don't want you to know!"

Provide your credibility assessment.
"""

    print("Testing with a clearly fake news example...\n")
    print("Input:", user_input[:100] + "...")
    print("\nCalling agent...\n")

    try:
        result = handle_standalone_agent_request(
            config_id="fake-news-detector-v1", user_input=user_input
        )

        if result["success"]:
            print("✅ SUCCESS!\n")

            # Show agent's thinking process
            metadata = result.get("metadata", {})
            full_state = result.get("full_state", {})

            print_section("AGENT EXECUTION TRACE", length=60)
            print(f"Total Iterations: {metadata.get('iterations', 0)}")
            print(f"Tool Calls Made: {metadata.get('tool_calls', 0)}")
            print(f"Total Messages: {metadata.get('total_messages', 0)}")
            print()

            # Show tool usage details using utility
            if full_state and full_state.get("tool_results"):
                print_tool_history(full_state)

            # Show message flow using utility
            if full_state and "messages" in full_state:
                print_section("MESSAGE FLOW (Agent's Thinking)", length=60)
                for i, msg in enumerate(full_state["messages"], 1):
                    print_message(msg, i, truncate_length=200)

            print_section("FINAL AGENT RESPONSE", length=60)
            print(result["result"])
            print_separator(length=60)
            print(f"Execution ID: {result['execution_id']}")
            print_separator(length=60)
            print()
        else:
            print("❌ FAILED")
            print(f"Error: {result.get('error')}\n")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}\n")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    quick_test()
