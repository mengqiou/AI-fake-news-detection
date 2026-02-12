"""
Quick test with VERBOSE output - shows agent thinking in real-time.

This version shows step-by-step what the agent is doing.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.agent_factory import instantiate_agent
from app.tools.tool_loader import gather_agent_tools
from app.utils.config_utils import get_agent_by_config_id
from app.utils.pretty_print import print_agent_execution
from langchain_core.messages import HumanMessage


def verbose_test():
    """Run test with verbose output showing agent's thinking."""

    print("\n" + "=" * 70)
    print("VERBOSE TEST: Fake News Detection Agent")
    print("=" * 70 + "\n")

    user_input = """
Please analyze this news for fake news or misinformation:

PLATFORM: Twitter
CONTENT: "BREAKING: Drinking bleach cures COVID-19! Scientists don't want you to know!"

Provide your credibility assessment.
"""

    print("=" * 70)
    print("SETUP PHASE")
    print("=" * 70)

    # Step 1: Load config
    print("\n[Step 1] Loading agent configuration...")
    config_id = "fake-news-detector-v1"
    agent_config = get_agent_by_config_id(config_id)

    if not agent_config:
        print(f"❌ Agent config '{config_id}' not found!")
        print("\nRun: python scripts/setup_first_agent.py")
        sys.exit(1)

    print(f"✅ Loaded: {agent_config.name}")
    print(f"   Model: {agent_config.model_id}")
    print(f"   Tools: {agent_config.tools}")
    print(f"   Max Iterations: {agent_config.max_iterations}")

    # Step 2: Gather tools
    print("\n[Step 2] Gathering tools...")
    tools = gather_agent_tools(agent_config)
    print(f"✅ Loaded {len(tools)} tools: {list(tools.keys())}")

    # Step 3: Instantiate agent
    print("\n[Step 3] Instantiating agent with LLM...")
    agent = instantiate_agent(agent_config, tools)
    print("✅ Agent workflow created")

    # Step 4: Execute
    print("\n" + "=" * 70)
    print("EXECUTION PHASE")
    print("=" * 70)
    print("\nUser Input:")
    print(user_input.strip())
    print("\n" + "-" * 70)

    try:
        # Prepare initial state
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_input": user_input,
            "tool_results": [],
            "final_output": "",
            "iteration_count": 0,
        }

        print("\n[Starting Agent Loop]\n")

        # Invoke agent
        final_state = agent.invoke(initial_state)

        # Pretty print the execution trace
        print_agent_execution(final_state)

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    verbose_test()
