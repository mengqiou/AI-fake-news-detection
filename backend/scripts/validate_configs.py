"""
Validate configuration templates for CI/CD pipeline.

Checks:
- All JSON configs are valid and have required fields
- All prompts exist and are non-empty
"""

import json
import sys
from pathlib import Path


def validate_agent_configs():
    """Validate all agent configuration JSON files."""
    configs_dir = Path(__file__).parent.parent / "configs" / "agents"

    if not configs_dir.exists():
        print(f"❌ Directory not found: {configs_dir}")
        return False

    json_files = list(configs_dir.glob("*.json"))
    if not json_files:
        print(f"⚠️  No JSON config files found in {configs_dir}")
        return True

    all_valid = True
    for config_file in json_files:
        try:
            with open(config_file) as f:
                data = json.load(f)

            # Check required fields
            required_fields = ["name", "config_id", "llm_provider"]
            for field in required_fields:
                if field not in data:
                    print(f"❌ {config_file.name}: missing required field '{field}'")
                    all_valid = False
                    continue

            if all_valid:
                print(f"✅ {config_file.name} valid")

        except json.JSONDecodeError as e:
            print(f"❌ {config_file.name}: invalid JSON - {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {config_file.name}: error - {e}")
            all_valid = False

    return all_valid


def validate_prompts():
    """Validate all prompt template files."""
    prompts_dir = Path(__file__).parent.parent / "configs" / "prompts"

    if not prompts_dir.exists():
        print(f"❌ Directory not found: {prompts_dir}")
        return False

    txt_files = list(prompts_dir.glob("*.txt"))
    if not txt_files:
        print(f"⚠️  No prompt files found in {prompts_dir}")
        return True

    all_valid = True
    for prompt_file in txt_files:
        try:
            content = prompt_file.read_text()

            if len(content.strip()) == 0:
                print(f"❌ {prompt_file.name}: empty prompt")
                all_valid = False
            else:
                print(f"✅ {prompt_file.name} valid ({len(content)} chars)")

        except Exception as e:
            print(f"❌ {prompt_file.name}: error - {e}")
            all_valid = False

    return all_valid


def main():
    """Run all validations."""
    print("=" * 70)
    print("VALIDATING CONFIGURATION TEMPLATES")
    print("=" * 70)

    print("\n📋 Validating Agent Configs:")
    configs_valid = validate_agent_configs()

    print("\n📝 Validating Prompts:")
    prompts_valid = validate_prompts()

    print("\n" + "=" * 70)
    if configs_valid and prompts_valid:
        print("✅ ALL VALIDATIONS PASSED")
        print("=" * 70)
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
