"""
Configuration Update CLI

Update agent configurations and prompts in AWS DynamoDB from template files.

Usage:
    python scripts/update_config.py agent <name>     # Update agent config only
    python scripts/update_config.py prompt <name>    # Update prompt only
    python scripts/update_config.py all <name>       # Update both prompt and agent
    python scripts/update_config.py list             # List available configs
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db_commands.agent_config_commands import create_agent_config
from app.db_commands.prompt_commands import save_prompt
from app.entity.AgentConfig import AgentConfig, KnowledgeBaseConfig

CONFIGS_DIR = Path(__file__).parent.parent / "configs"
PROMPTS_DIR = CONFIGS_DIR / "prompts"
AGENTS_DIR = CONFIGS_DIR / "agents"


def list_configs():
    """List all available configuration templates."""
    print("\n" + "=" * 70)
    print("AVAILABLE CONFIGURATION TEMPLATES")
    print("=" * 70 + "\n")

    print("Prompts:")
    if PROMPTS_DIR.exists():
        prompt_files = list(PROMPTS_DIR.glob("*.txt"))
        if prompt_files:
            for f in sorted(prompt_files):
                name = f.stem
                size = f.stat().st_size
                print(f"  • {name} ({size} bytes)")
        else:
            print("  (none)")
    else:
        print("  (directory not found)")

    print("\nAgent Configs:")
    if AGENTS_DIR.exists():
        agent_files = list(AGENTS_DIR.glob("*.json"))
        if agent_files:
            for f in sorted(agent_files):
                name = f.stem
                size = f.stat().st_size
                print(f"  • {name} ({size} bytes)")
        else:
            print("  (none)")
    else:
        print("  (directory not found)")

    print("\n" + "=" * 70)
    print("Usage:")
    print("  python scripts/update_config.py all <name>")
    print("  Example: python scripts/update_config.py all fake_news_detector_v1")
    print("=" * 70 + "\n")


def deploy_prompt(name: str):
    """Update a prompt template in DynamoDB."""
    prompt_file = PROMPTS_DIR / f"{name}.txt"

    if not prompt_file.exists():
        print(f"❌ Prompt template not found: {prompt_file}")
        print(f"\nAvailable prompts:")
        for f in PROMPTS_DIR.glob("*.txt"):
            print(f"  • {f.stem}")
        return False

    print(f"\n📝 Updating prompt: {name}")
    print(f"   File: {prompt_file}")

    # Read prompt content
    with open(prompt_file, "r") as f:
        prompt_content = f.read()

    # Derive prompt_id from filename
    # Convention: fake_news_detector_v1 -> fake-news-detector-prompt-v1
    prompt_id = (
        name.replace("_", "-") + "-prompt"
        if not "prompt" in name
        else name.replace("_", "-")
    )

    print(f"   Prompt ID: {prompt_id}")
    print(f"   Length: {len(prompt_content)} characters")

    try:
        save_prompt(prompt_id, prompt_content)
        print(f"✅ Prompt updated successfully!")
        print(f"   Table: {os.getenv('PROMPTS_TABLE', 'ai-prompts')}")
        return True
    except Exception as e:
        print(f"❌ Failed to update prompt: {e}")
        return False


def deploy_agent(name: str):
    """Update an agent configuration in DynamoDB."""
    agent_file = AGENTS_DIR / f"{name}.json"

    if not agent_file.exists():
        print(f"❌ Agent config template not found: {agent_file}")
        print(f"\nAvailable agents:")
        for f in AGENTS_DIR.glob("*.json"):
            print(f"  • {f.stem}")
        return False

    print(f"\n🤖 Updating agent config: {name}")
    print(f"   File: {agent_file}")

    # Read and parse JSON
    with open(agent_file, "r") as f:
        config_data = json.load(f)

    print(f"   Agent: {config_data.get('name')}")
    print(f"   Config ID: {config_data.get('config_id')}")
    print(f"   Model: {config_data.get('model_id')}")
    print(f"   Tools: {config_data.get('tools', [])}")

    try:
        # Convert to AgentConfig object
        kb_data = config_data.get("knowledge_base", {})
        knowledge_base = (
            KnowledgeBaseConfig(
                enabled=kb_data.get("enabled", False),
                vector_store=kb_data.get("vector_store", "chroma"),
                index_name=kb_data.get("index_name", ""),
                embedding_model=kb_data.get(
                    "embedding_model", "text-embedding-3-small"
                ),
                top_k=kb_data.get("top_k", 5),
            )
            if kb_data
            else None
        )

        agent_config = AgentConfig(
            name=config_data["name"],
            description=config_data["description"],
            config_id=config_data["config_id"],
            tools=config_data.get("tools", []),
            prompt_id=config_data["prompt_id"],
            sub_agents=[],  # TODO: Handle sub-agents if needed
            knowledge_base=knowledge_base,
            llm_provider=config_data.get("llm_provider", "anthropic"),
            model_id=config_data.get("model_id", "claude-3-5-sonnet-20241022"),
            temperature=config_data.get("temperature", 0.7),
            max_tokens=config_data.get("max_tokens", 4096),
            max_iterations=config_data.get("max_iterations", 10),
        )

        create_agent_config(agent_config)
        print(f"✅ Agent config updated successfully!")
        print(f"   Table: {os.getenv('AGENT_CONFIG_TABLE', 'agent-configs')}")
        return True

    except Exception as e:
        print(f"❌ Failed to update agent config: {e}")
        import traceback

        traceback.print_exc()
        return False


def deploy_all(name: str):
    """Update both prompt and agent configuration in DynamoDB."""
    print("\n" + "=" * 70)
    print(f"UPDATING CONFIGURATION: {name}")
    print("=" * 70)

    # Update prompt first
    prompt_success = deploy_prompt(name)

    # Then update agent config
    agent_success = deploy_agent(name)

    print("\n" + "=" * 70)
    if prompt_success and agent_success:
        print("✅ UPDATE COMPLETE")
        print("=" * 70)
        print(f"\nAgent '{name}' is ready to use!")
        print("\nTest it:")
        print("  python tests/quick_test.py")
        print("  python tests/quick_test_verbose.py")
    else:
        print("❌ UPDATE FAILED")
        print("=" * 70)
        if not prompt_success:
            print("\n⚠️  Prompt update failed")
        if not agent_success:
            print("\n⚠️  Agent config update failed")
    print()


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("CONFIGURATION UPDATE CLI")
        print("=" * 70)
        print("\nUsage:")
        print("  python scripts/update_config.py list")
        print("  python scripts/update_config.py prompt <name>")
        print("  python scripts/update_config.py agent <name>")
        print("  python scripts/update_config.py all <name>")
        print("\nExamples:")
        print("  python scripts/update_config.py list")
        print("  python scripts/update_config.py all fake_news_detector_v1")
        print("=" * 70 + "\n")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        list_configs()

    elif command == "prompt":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify config name")
            print("Usage: python scripts/update_config.py prompt <name>")
            sys.exit(1)
        name = sys.argv[2]
        deploy_prompt(name)

    elif command == "agent":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify config name")
            print("Usage: python scripts/update_config.py agent <name>")
            sys.exit(1)
        name = sys.argv[2]
        deploy_agent(name)

    elif command == "all":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify config name")
            print("Usage: python scripts/update_config.py all <name>")
            sys.exit(1)
        name = sys.argv[2]
        deploy_all(name)

    else:
        print(f"❌ Unknown command: {command}")
        print("\nValid commands: list, prompt, agent, all")
        sys.exit(1)


if __name__ == "__main__":
    main()
