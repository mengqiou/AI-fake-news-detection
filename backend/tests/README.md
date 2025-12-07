# Integration Tests

This directory contains end-to-end integration tests for the fake news detection agent.

## Purpose

Tests here verify:
- ✅ Full agent workflow (with DynamoDB, Bedrock, tools)
- ✅ Real-world scenarios
- ✅ Platform verification tool integration
- ✅ Multiple test cases

## Test Scripts

### `quick_test.py`
**Fast smoke test** - Verify agent works

```bash
python tests/quick_test.py
```

**What it tests:**
- Single fake news example
- Full agent execution
- Tool usage
- DynamoDB integration
- Shows detailed execution trace

**Run time:** ~10-30 seconds

**When to use:**
- After deploying config
- Quick verification agent works
- CI/CD smoke test

---

### `quick_test_verbose.py`
**Detailed execution trace** - See agent thinking

```bash
python tests/quick_test_verbose.py
```

**What it shows:**
- Setup phase (loading config, tools)
- Each iteration
- Tool calls with arguments
- Tool results
- Message flow
- Agent's reasoning
- Final response

**Run time:** ~10-30 seconds

**When to use:**
- Debugging agent behavior
- Understanding tool usage
- Developing new prompts
- Teaching/demo purposes

---

### `test_platform_verification.py`
**Platform verification scenarios** - Multiple test cases

```bash
python tests/test_platform_verification.py
```

**What it tests:**
- Fake news IN verification platform
- Real news IN verification platform
- Claims NOT in verification platform
- Multiple platforms (Twitter, Facebook, etc.)

**Run time:** ~2-5 minutes (multiple tests)

**When to use:**
- Testing platform verification tool
- Verifying agent handles all scenarios
- Regression testing
- Demo different outcomes

---

### `test_fake_news_agent_local.py`
**Comprehensive test suite** - Interactive testing

```bash
python tests/test_fake_news_agent_local.py
```

**Features:**
- 5 pre-loaded test cases
- Interactive mode (enter your own news)
- Multiple platforms
- Different content types

**Modes:**
1. Run all samples
2. Run specific sample
3. Interactive mode (enter your own news)
4. Quick test

**When to use:**
- Manual testing
- Trying different news articles
- Demo to stakeholders
- Exploratory testing

---

## Test Categories

### Smoke Tests (Quick)
Run these after any change:
```bash
python tests/quick_test.py
```

### Development Tests (Verbose)
Run when developing/debugging:
```bash
python tests/quick_test_verbose.py
```

### Regression Tests (Comprehensive)
Run before releases:
```bash
python tests/test_platform_verification.py
```

### Manual/Exploratory Tests
Run for demos or manual testing:
```bash
python tests/test_fake_news_agent_local.py
```

## Prerequisites

Before running these tests:

1. **AWS Setup**
   ```bash
   # Verify AWS connection works
   python setup/test_bedrock_boto3.py
   ```

2. **DynamoDB Tables**
   - `ai-prompts` table exists
   - `agent-configs` table exists
   - `execution-history` table exists

3. **Agent Deployed**
   ```bash
   # Update agent configuration
   python scripts/update_config.py all fake_news_detector_v1
   ```

4. **Dependencies**
   ```bash
   pip install langchain-aws boto3 python-dotenv langchain-core langgraph
   ```

## Expected Outputs

### Successful Test Output

```
✅ SUCCESS!

AGENT EXECUTION TRACE:
Total Iterations: 3
Tool Calls Made: 1
Total Messages: 4

TOOL CALLS:
[Tool Call 1]
Tool: verify_on_platform
Output:
❌ Status: FALSE
Verified By: CDC, WHO, FDA
...

FINAL AGENT RESPONSE:
Platform Verification: FOUND - Status FALSE
Credibility Score: 0/100
This claim has been debunked...
```

### Failed Test Output

```
❌ FAILED
Error: Agent configuration not found for config_id: fake-news-detector-v1

→ Run: python scripts/update_config.py all fake_news_detector_v1
```

## Test Data

Sample test cases include:

1. **Twitter Fake News**: "Bleach cures COVID" → Expected: FALSE
2. **Facebook Misinformation**: "5G mind control" → Expected: FALSE
3. **WhatsApp Rumor**: "Vaccine kidnappers" → Expected: FALSE
4. **BBC Real News**: "UK inflation data" → Expected: TRUE
5. **Reuters Science**: "NASA Webb CO2" → Expected: TRUE

## Adding New Tests

### 1. Add to existing test file

```python
# In test_fake_news_agent_local.py
SAMPLE_NEWS_ARTICLES["my_test"] = {
    "platform": "Twitter",
    "content": "Your test content...",
    "metadata": {...}
}
```

### 2. Create new test file

```python
# tests/test_my_scenario.py
from app.handlers.standalone_agent_handler import handle_standalone_agent_request

def test_my_scenario():
    result = handle_standalone_agent_request(
        config_id="fake-news-detector-v1",
        user_input="Test input..."
    )
    assert result["success"]
    # Add assertions...
```

## CI/CD Integration

```bash
# Quick smoke test (30s)
python tests/quick_test.py

# Full regression suite (5min)
python tests/test_platform_verification.py
```

## Performance

Typical run times:
- `quick_test.py`: 10-30 seconds
- `quick_test_verbose.py`: 10-30 seconds  
- `test_platform_verification.py`: 2-5 minutes
- `test_fake_news_agent_local.py`: Interactive (varies)

## Troubleshooting

### Test hangs or times out
- Check Bedrock model is responding: `python setup/test_bedrock_boto3.py`
- Verify network connectivity
- Check AWS service status

### "Agent configuration not found"
```bash
python scripts/update_config.py all fake_news_detector_v1
```

### "Tool not found"
- Check tool is in agent config: `configs/agents/fake_news_detector_v1.json`
- Verify tool exists: `app/tools/platform_verification_tool.py`

### Different results each run
- Agent uses LLM with temperature > 0 (some randomness expected)
- Tool results should be consistent
- Platform verification should be deterministic

## Setup vs Integration Tests

**Setup Tests** (`setup/`): Verify individual components  
**Integration Tests** (`tests/`): Verify complete workflows

Always run setup tests first if integration tests fail!
