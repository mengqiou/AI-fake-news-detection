# AI Fake News Detection Agent

An intelligent AI agent that detects fake news by verifying claims against a trusted verification platform using AWS Bedrock and LangGraph.

## What It Does

Analyzes news articles and claims to detect misinformation by:
- Searching a fact-checking verification database
- Analyzing source credibility and evidence
- Detecting manipulation tactics and red flags
- Providing credibility scores and recommendations

## Quick Start

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

📖 **See [`backend/README.md`](backend/README.md) for complete documentation** including:
- Detailed setup instructions
- Configuration management
- Testing guide
- Development workflow
- Troubleshooting
- API reference

**Quick links:**
- Configuration: [`backend/README.md`](backend/README.md)
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


**Important:**
- `main` branch is protected - no direct pushes ⛔
- All changes require pull requests + CI passing
- Follow conventional commit format

## Next Steps (2026-02-13)

1. **Fix double tool-binding bug** — Remove `bind_tools` in either `agent_factory.py` or `agent_workflow.py`, not both
2. **Widen `user_input` to multimodal** — Change `user_input: str` to `Union[str, List[dict]]` in `AgentState` and `invoke_agent` early, before building on top
3. **Add `input_mode` field to `AgentConfig`** — `"text"` or `"multimodal"` to drive model selection and handler routing
4. **Build image handler** — `image_standalone_agent_handler.py` that constructs multimodal `HumanMessage` with text + image
5. **Build evidence-rich tools** — Each tool returns structured data (source, result, URL, confidence), not free text. This is the HD differentiator
6. **Connect real data sources** — Replace mock DB with at least one real API (Google Fact Check, reverse image search, ELA analysis, etc.)
7. **Compute credibility score from evidence** — Score derived from tool outputs, not LLM opinion
8. **Add API layer** — FastAPI endpoints to expose the handlers
9. **Add frontend** — User input form with image upload, structured results display showing the evidence chain

> Items 1-4 are foundational refactors. Items 5-7 are where the grade lives. Items 8-9 are the "full-stack" finish.

## License

MIT

---

**For full documentation, see [`backend/README.md`](backend/README.md)**
