# AI Fake News Detection Agent

An intelligent AI agent that detects fake news by verifying claims against a trusted verification platform using AWS Bedrock and LangGraph.

## What It Does

Analyzes news articles and claims to detect misinformation by:
- Searching a fact-checking verification database
- Analyzing source credibility and evidence
- Detecting manipulation tactics and red flags
- Providing credibility scores and recommendations

## Quick Start

```bash
cd backend

# 1. Test AWS connection
python setup/test_bedrock_boto3.py

# 2. Initialize DynamoDB tables
python scripts/init_dynamodb.py

# 3. Update agent configuration in DynamoDB
python scripts/update_config.py all fake_news_detector_v1

# 4. Test locally
python tests/quick_test.py
```

> **Note**: Production deployment (Lambda, API Gateway, etc.) is work in progress.

## Architecture

```
User Input → Agent → verify_on_platform tool → Analysis → Credibility Score
                ↓
         DynamoDB (config, prompts)
                ↓
         AWS Bedrock (Nova Micro LLM)
```

## Key Features

- ✅ **Platform Verification** - Searches fact-checking database before analysis
- ✅ **AWS Bedrock** - Cost-effective LLM (Amazon Nova Micro)
- ✅ **Template-Based Config** - Version-controlled JSON/text templates
- ✅ **Tool Architecture** - Extensible with custom verification tools

## Example Output

```
Platform Verification: ❌ FALSE
Verified By: CDC, WHO, FDA

Credibility Score: 0/100
Recommendation: DANGEROUS MISINFORMATION
```

## Tech Stack

- **LLM**: AWS Bedrock (Amazon Nova Micro)
- **Framework**: LangGraph
- **Storage**: AWS DynamoDB
- **Language**: Python 3.14

## Documentation

📖 **See `backend/README.md` for complete documentation** including:
- Detailed setup instructions
- Configuration management
- Testing guide
- Development workflow
- Troubleshooting
- API reference

**Quick links:**
- Configuration: `backend/configs/README.md`
- Testing: `backend/tests/README.md`
- Platform Verification: `backend/docs/platform_verification.md`

## Project Structure

```
backend/
├── app/          # Application code
├── configs/      # Configuration templates
├── scripts/      # Deployment CLI
├── setup/        # Setup tests
├── tests/        # Integration tests
└── docs/         # Documentation
```

## License

MIT

---

**For full documentation, see [`backend/README.md`](backend/README.md)**
