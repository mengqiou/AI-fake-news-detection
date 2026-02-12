"""
Test Platform Verification - Shows how agent verifies against "given platform"

This demonstrates the workflow:
1. User provides a news claim
2. Agent uses verify_on_platform tool to search the verification database
3. Agent returns result based on what it found (or didn't find) on the platform
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.handlers.standalone_agent_handler import \
    handle_standalone_agent_request


def test_claim(claim_description: str, claim_text: str):
    """Test a single claim against the verification platform."""

    print("\n" + "=" * 80)
    print(f"TEST: {claim_description}")
    print("=" * 80)
    print(f"\nClaim: {claim_text}")
    print("\n" + "-" * 80)
    print("Sending to agent with verification platform tool...")
    print("-" * 80 + "\n")

    user_input = f"""Please verify this claim:

"{claim_text}"

Use the verification platform to check if this claim has been fact-checked or verified."""

    try:
        result = handle_standalone_agent_request(
            config_id="fake-news-detector-v1", user_input=user_input
        )

        if result["success"]:
            print("✅ VERIFICATION COMPLETE\n")
            print("=" * 80)
            print("AGENT RESPONSE:")
            print("=" * 80)
            print(result["result"])
            print("\n" + "=" * 80)
            print("TOOL USAGE:")
            print("=" * 80)
            print(f"Tool calls made: {result['metadata'].get('tool_calls', 0)}")
            if result["metadata"].get("tool_results"):
                print("\nTool Results:")
                for tool_result in result["metadata"].get("tool_results", []):
                    print(f"  - {tool_result.get('tool_name')}: Called successfully")
            print("=" * 80 + "\n")
        else:
            print("❌ VERIFICATION FAILED")
            print(f"Error: {result.get('error')}\n")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}\n")
        import traceback

        traceback.print_exc()

    input("Press Enter to continue to next test...")


def main():
    """Run platform verification tests."""

    print("\n" + "=" * 80)
    print(" " * 15 + "PLATFORM VERIFICATION TEST SUITE")
    print("=" * 80)
    print("""
This test demonstrates how the agent uses the "given platform" (verification database)
to check claims.

The agent will:
1. Receive a claim from you
2. Use the verify_on_platform tool to search the verification database
3. Report what it found (or didn't find) on the platform
4. Provide its assessment based on the platform's response
""")
    print("=" * 80 + "\n")

    # Test 1: Claim that EXISTS in platform and is FALSE
    test_claim("FAKE NEWS - In Verification Platform", "Drinking bleach cures COVID-19")

    # Test 2: Claim that EXISTS in platform and is TRUE
    test_claim(
        "REAL NEWS - In Verification Platform",
        "NASA's Webb Telescope detected carbon dioxide on an exoplanet",
    )

    # Test 3: Claim that DOES NOT EXIST in platform
    test_claim(
        "UNVERIFIED - Not in Platform",
        "A new study shows that eating chocolate improves memory by 50%",
    )

    # Test 4: Another FALSE claim in platform
    test_claim(
        "CONSPIRACY THEORY - In Verification Platform",
        "5G towers are used to control people's minds",
    )

    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETE")
    print("=" * 80)
    print("""
Key Observations:
- When claim IS in platform: Agent uses verification platform's result
- When claim NOT in platform: Agent states "Cannot verify on dedicated platform"
- Agent always tries to use verify_on_platform tool first
- Platform verification is the primary source of truth
""")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    PLATFORM VERIFICATION DEMO                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

This demonstrates the "given platform" concept:
- The agent has access to a verification database (the "given platform")
- When you give it a claim, it searches that platform first
- It reports what the platform says (or that it couldn't find anything)
- This mimics real-world fact-checking services like Snopes, PolitiFact, etc.

In production, this would be:
  - API calls to fact-checking services
  - Searches of verified news databases  
  - Queries to social media platform verification APIs
  
For this demo, we use a stubbed database with common fake news examples.
""")

    main()
