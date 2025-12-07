# Agent Configuration Templates

This directory contains configuration templates for AI agents and their prompts.

## Directory Structure

```
configs/
├── prompts/          # System prompt templates
│   └── fake_news_detector_v1.txt
└── agents/           # Agent configuration templates
    └── fake_news_detector_v1.json
```

## Prompt Templates (`prompts/`)

Prompt templates define the system instructions for agents.

**Format**: Plain text (`.txt`) files

**Naming Convention**: `{agent_name}_{version}.txt`

**Example**: `fake_news_detector_v1.txt`

### Structure:
- Role definition
- Available tools
- Analysis workflow
- Output format
- Guidelines

## Agent Configuration Templates (`agents/`)

Agent configurations define the agent's settings and behavior.

**Format**: JSON (`.json`) files

**Naming Convention**: `{agent_name}_{version}.json`

**Example**: `fake_news_detector_v1.json`

### Required Fields:

```json
{
  "name": "Human-readable agent name",
  "description": "What this agent does",
  "config_id": "unique-agent-id",
  "prompt_id": "reference-to-prompt-in-dynamodb",
  "tools": ["list", "of", "tool", "names"],
  "sub_agents": [],
  "knowledge_base": {
    "enabled": false,
    "vector_store": "chroma",
    "index_name": "",
    "embedding_model": "amazon.titan-embed-text-v1",
    "top_k": 5
  },
  "llm_provider": "bedrock",
  "model_id": "amazon.nova-micro-v1:0",
  "temperature": 0.5,
  "max_tokens": 2048,
  "max_iterations": 8
}
```

### Field Descriptions:

- **name**: Display name for the agent
- **description**: Brief description of agent's purpose
- **config_id**: Unique identifier (used as DynamoDB key)
- **prompt_id**: ID of the system prompt in DynamoDB prompts table
- **tools**: Array of tool names the agent can use
- **sub_agents**: Array of sub-agent configurations (for hierarchical agents)
- **knowledge_base**: RAG configuration (optional)
- **llm_provider**: `"bedrock"`, `"anthropic"`, or `"openai"`
- **model_id**: Model identifier (e.g., `"amazon.nova-micro-v1:0"`)
- **temperature**: 0.0 (deterministic) to 1.0 (creative)
- **max_tokens**: Maximum tokens in response
- **max_iterations**: Maximum agent loop iterations

## Available Tools

Current tools:
- `verify_on_platform`: Search verification database for fact-checked claims
- `search_internet`: Web search capability (if enabled)
- `summary_long_text`: Summarize long content (if enabled)

## Deployment

To update configurations in DynamoDB:

```bash
# Update a single agent config
python scripts/update_config.py agent fake_news_detector_v1

# Update a single prompt
python scripts/update_config.py prompt fake_news_detector_v1

# Update both (prompt + agent config)
python scripts/update_config.py all fake_news_detector_v1

# List all available configs
python scripts/update_config.py list
```

## Creating New Configurations

### 1. Create a new prompt:

```bash
cp configs/prompts/fake_news_detector_v1.txt configs/prompts/my_agent_v1.txt
# Edit the file with your prompt
```

### 2. Create a new agent config:

```bash
cp configs/agents/fake_news_detector_v1.json configs/agents/my_agent_v1.json
# Edit the JSON with your settings
```

### 3. Update in DynamoDB:

```bash
python scripts/update_config.py all my_agent_v1
```

## Version Management

Use version suffixes to manage different versions:
- `fake_news_detector_v1.json` - Initial version
- `fake_news_detector_v2.json` - Updated version
- `fake_news_detector_v1_experimental.json` - Experimental variant

## Best Practices

1. **Always version your configs**: Use `_v1`, `_v2`, etc.
2. **Keep prompt and config IDs in sync**: If prompt is `my-agent-prompt-v1`, config should reference it
3. **Test before deploying**: Use test scripts to verify configs work
4. **Document changes**: Add comments in JSON describing what changed
5. **Backup**: Configs in git serve as version control

## Examples

See `fake_news_detector_v1.json` for a complete working example with:
- Platform verification tool
- AWS Bedrock model configuration
- Optimized settings for fake news detection
