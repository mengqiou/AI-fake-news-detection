# Backend - AI Fake News Detection Agent

AI agent system for detecting fake news using AWS Bedrock and LangGraph.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure AWS (edit .env)
cp .env.example .env  # If you have one
# Set: AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# 3. Initialize DynamoDB tables
python scripts/init_dynamodb.py

# 4. Update agent configuration in DynamoDB
python scripts/update_config.py all fake_news_detector_v1

# 5. Test
python tests/quick_test.py
```

## Project Structure

```
backend/
├── app/                    # Application code
│   ├── agents/            # Agent workflow logic (LangGraph)
│   ├── db_commands/       # DynamoDB operations
│   ├── entity/            # Data models
│   ├── handlers/          # Request handlers
│   ├── tools/             # Agent tools (verification, search, etc.)
│   └── utils/             # Utilities (pretty_print, config_utils)
│
├── configs/               # Configuration templates (version controlled)
│   ├── prompts/          # System prompt templates (.txt)
│   └── agents/           # Agent config templates (.json)
│
├── infra/                # AWS infrastructure clients
│   └── dynamodb_client.py
│
├── scripts/              # Operational scripts
│   ├── update_config.py  # Update configs in DynamoDB
│   └── init_dynamodb.py  # Create DynamoDB tables
│
├── setup/                # Setup & verification tests
│   ├── test_bedrock_boto3.py
│   └── test_bedrock_connection.py
│
├── tests/                # Integration tests
│   ├── quick_test.py
│   ├── quick_test_verbose.py
│   └── test_platform_verification.py
│
├── examples/             # Code examples
│   └── pretty_print_example.py
│
└── docs/                 # Documentation
    ├── platform_verification.md
    └── testing_guide.md
```

## Core Concepts

### 1. **Template-Based Configuration**
Configuration lives in `configs/` as version-controlled templates:
- **Prompts**: Plain text files with system instructions
- **Agents**: JSON files with model settings, tools, parameters

Update with: `python scripts/update_config.py all <name>`

### 2. **Platform Verification**
The agent searches a verification database (fact-checking platform) to verify claims:
- Claims IN platform → Use platform's verdict
- Claims NOT in platform → Report "cannot verify"

See: `docs/platform_verification.md`

### 3. **Agent Workflow**
Built with LangGraph:
1. Receives user input
2. Calls tools (e.g., `verify_on_platform`)
3. Analyzes results
4. Returns credibility assessment

### 4. **AWS Infrastructure**
- **DynamoDB**: Stores configs, prompts, execution history
- **Bedrock**: LLM inference (Amazon Nova Micro)
- **IAM**: Permissions for Bedrock + DynamoDB

## Common Tasks

### Update Configuration
```bash
# List available templates
python scripts/update_config.py list

# Update agent + prompt
python scripts/update_config.py all fake_news_detector_v1

# Update only prompt
python scripts/update_config.py prompt fake_news_detector_v1

# Update only agent config
python scripts/update_config.py agent fake_news_detector_v1
```

### Initialize DynamoDB
```bash
# Create all required tables
python scripts/init_dynamodb.py
```

### Testing
```bash
# Setup tests (run first)
python setup/test_bedrock_boto3.py        # AWS connection
python setup/test_bedrock_connection.py   # LangChain integration

# Integration tests
python tests/quick_test.py                # Smoke test (30s)
python tests/quick_test_verbose.py        # Detailed trace
python tests/test_platform_verification.py # Multiple scenarios
```

### Create New Agent
```bash
# 1. Copy templates
cp configs/prompts/fake_news_detector_v1.txt configs/prompts/my_agent_v1.txt
cp configs/agents/fake_news_detector_v1.json configs/agents/my_agent_v1.json

# 2. Edit templates
vim configs/prompts/my_agent_v1.txt
vim configs/agents/my_agent_v1.json

# 3. Update configuration in DynamoDB
python scripts/update_config.py all my_agent_v1
```

### View Agent Execution Details
```python
from app.utils.pretty_print import print_agent_execution

final_state = agent.invoke(initial_state)
print_agent_execution(final_state)
# Shows: iterations, tool calls, messages, final response
```

## Development Workflow

```bash
# 1. Make changes to templates
vim configs/prompts/fake_news_detector_v1.txt

# 2. Test offline (no AWS)
python setup/test_offline_stub.py

# 3. Update configuration in DynamoDB
python scripts/update_config.py all fake_news_detector_v1

# 4. Test with verbose output
python tests/quick_test_verbose.py
```

## Key Files

- **`scripts/update_config.py`** - Update configs in DynamoDB
- **`scripts/init_dynamodb.py`** - DynamoDB table initialization
- **`app/handlers/standalone_agent_handler.py`** - Main agent handler
- **`app/agents/agent_factory.py`** - Agent instantiation
- **`app/tools/platform_verification_tool.py`** - Verification tool
- **`app/utils/pretty_print.py`** - Execution trace formatter

## Tech Stack

- **Framework**: LangGraph (agent workflow)
- **LLM**: AWS Bedrock (Amazon Nova Micro)
- **Storage**: AWS DynamoDB
- **Language**: Python 3.14
- **Libraries**: langchain-aws, boto3, python-dotenv

## Environment Variables

Required in `.env`:
```bash
# AWS Configuration
AWS_REGION=ap-southeast-2
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# DynamoDB Tables
AGENT_CONFIG_TABLE=agent-configs
PROMPTS_TABLE=ai-prompts
EXECUTION_TABLE=execution-history

# Optional: LLM API Keys (if using Anthropic/OpenAI)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
```

## Dependencies

See `requirements.txt`:
- `langchain-core`, `langchain`, `langgraph` - Agent framework
- `langchain-aws` - AWS Bedrock integration
- `boto3` - AWS SDK
- `python-dotenv` - Environment management

## Documentation Map

- **Overview**: This file
- **Configs**: `configs/README.md`
- **Setup**: `setup/README.md`
- **Tests**: `tests/README.md`
- **Utils**: `app/utils/README.md`
- **Examples**: `examples/README.md`
- **Concepts**: `docs/platform_verification.md`
- **Reference**: `docs/testing_guide.md`

## Troubleshooting

### Tests failing?
1. Run `python setup/test_bedrock_boto3.py` - Check AWS
2. Run `python setup/test_bedrock_connection.py` - Check LangChain
3. Run `python scripts/init_dynamodb.py` - Check tables exist
4. Run `python scripts/update_config.py all fake_news_detector_v1` - Update config

### Agent not using tools?
- Check `configs/agents/*.json` has tools listed
- Update: `python scripts/update_config.py agent <name>`

### Model errors?
- Ensure model is enabled in AWS Bedrock console
- Check model ID matches available models in your region
- Amazon Nova Micro: `amazon.nova-micro-v1:0`


## Run Agent Locally

**Command Structure:**
```bash
python scripts/update_config.py <command> <config_name>
```

**Commands:**
- `list` - List available configurations
- `prompt <name>` - Update only the prompt in DynamoDB
- `agent <name>` - Update only the agent config in DynamoDB
- `all <name>` - Update both prompt and agent config (recommended)

**Workflow:**
```bash
# 1. Edit templates
vim configs/prompts/fake_news_detector_v1.txt
vim configs/agents/fake_news_detector_v1.json

# 2. Update both prompt + agent config in DynamoDB
python scripts/update_config.py all fake_news_detector_v1

# 3. Test
python tests/quick_test.py              # Quick test
python tests/quick_test_verbose.py      # Detailed trace
```

## Next Steps
1. **Build API**: Create REST API or Lambda wrapper
2. **Production**: Connect to real fact-checking APIs

## Contributing

When adding features:
1. Add code to appropriate `app/` subdirectory
2. Create configuration template in `configs/`
3. Add tests in `tests/`
4. Update relevant README
5. Add example if complex

---

**Ready to start?** Run: `python scripts/update_config.py all fake_news_detector_v1` 🚀
