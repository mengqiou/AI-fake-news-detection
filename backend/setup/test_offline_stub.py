"""
Offline stub test - tests agent logic without DynamoDB.

This is useful for development when you don't want to set up DynamoDB
or want to test faster without network calls.

Note: This directly tests the agent workflow, bypassing the handler.
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.entity.AgentConfig import AgentConfig, KnowledgeBaseConfig
from app.agents.agent_factory import instantiate_agent, invoke_agent


# Stub prompt (normally loaded from DynamoDB)
STUB_PROMPT = """You are a Fake News Detection AI Agent. Analyze content for misinformation.

Provide:
1. Credibility Score (0-100)
2. Key Findings
3. Red Flags
4. Evidence Assessment
5. Recommendation

Be objective and evidence-based."""


def create_stub_agent_config() -> AgentConfig:
    """Create an agent config without DynamoDB."""
    return AgentConfig(
        name="Fake News Detector (Stub)",
        description="Test agent without DynamoDB",
        config_id="fake-news-detector-stub",
        tools=[],  # No tools for offline test
        prompt_id="stub-prompt",
        sub_agents=[],
        knowledge_base=KnowledgeBaseConfig(enabled=False),
        llm_provider="bedrock",
        model_id="amazon.nova-micro-v1:0",
        temperature=0.5,
        max_tokens=2048,
        max_iterations=8
    )


def test_offline():
    """Test the agent without DynamoDB dependencies."""
    
    print("\n" + "=" * 70)
    print("OFFLINE STUB TEST - Fake News Detection")
    print("=" * 70)
    print("\nThis test bypasses DynamoDB and uses stubbed data.")
    print("Useful for quick development iteration.\n")
    
    # Create stub config
    agent_config = create_stub_agent_config()
    
    print(f"Agent: {agent_config.name}")
    print(f"Model: {agent_config.model_id}")
    print(f"Provider: {agent_config.llm_provider}\n")
    
    # Mock the prompt loading function
    import app.db_commands.prompt_commands as prompt_commands
    original_load_prompt = prompt_commands.load_prompt
    
    def mock_load_prompt(prompt_id: str) -> str:
        print(f"[STUB] Using stubbed prompt instead of loading from DynamoDB")
        return STUB_PROMPT
    
    # Temporarily replace the function
    prompt_commands.load_prompt = mock_load_prompt
    
    try:
        # Test case
        test_input = """Analyze this for fake news:

PLATFORM: Twitter
CONTENT: "BREAKING: Scientists prove that 5G causes COVID-19! Government coverup exposed!"

Provide your credibility assessment."""
        
        print("=" * 70)
        print("TEST INPUT:")
        print("=" * 70)
        print(test_input)
        print("\n" + "=" * 70)
        print("Instantiating agent...")
        print("=" * 70 + "\n")
        
        # Instantiate agent (this will use our mock)
        tools = {}  # No tools for offline test
        agent = instantiate_agent(agent_config, tools)
        
        print("Agent instantiated successfully!")
        print("\n" + "=" * 70)
        print("Invoking agent with test input...")
        print("=" * 70 + "\n")
        
        # Invoke agent
        result = invoke_agent(agent, test_input)
        
        print("✅ SUCCESS!\n")
        print("=" * 70)
        print("AGENT RESPONSE:")
        print("=" * 70)
        print(result["result"])
        print("\n" + "=" * 70)
        print("METADATA:")
        print("=" * 70)
        print(f"Iterations: {result['metadata'].get('iterations')}")
        print(f"Tool calls: {result['metadata'].get('tool_calls')}")
        print(f"Total messages: {result['metadata'].get('total_messages')}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        
    finally:
        # Restore original function
        prompt_commands.load_prompt = original_load_prompt
    
    print("\n" + "=" * 70)
    print("OFFLINE TEST COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    print("\n⚠️  OFFLINE/STUB MODE")
    print("This test uses mocked data and doesn't require DynamoDB.")
    print("For full integration testing, use test_fake_news_agent_local.py\n")
    
    test_offline()
