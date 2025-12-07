# Setup & Verification Scripts

This directory contains scripts for initial setup and connection verification.

## Purpose

Scripts here are used for:
- ✅ Verifying AWS credentials
- ✅ Testing Bedrock connectivity
- ✅ Checking model access
- ✅ Development/debugging without full agent setup

## Scripts

### `test_bedrock_boto3.py`
**Simplest Bedrock test** - Uses raw boto3 API

```bash
python setup/test_bedrock_boto3.py
```

**What it does:**
- Tests AWS credentials
- Sends "Hi" to Nova Micro model
- Shows raw Bedrock API response
- **Use this first** to verify your setup

**When to use:**
- First-time setup
- Debugging credentials
- Testing model access
- No LangChain dependencies

---

### `test_bedrock_connection.py`
**LangChain Bedrock test** - Uses langchain_aws

```bash
python setup/test_bedrock_connection.py
```

**What it does:**
- Tests with LangChain library (same as agent uses)
- Verifies langchain_aws is installed
- Sends "Hi" via ChatBedrock
- **Use after boto3 test passes**

**When to use:**
- Verifying LangChain integration
- Testing agent's LLM setup
- After boto3 test succeeds

---

### `test_offline_stub.py`
**Offline development test** - No DynamoDB required

```bash
python setup/test_offline_stub.py
```

**What it does:**
- Tests agent logic without DynamoDB
- Uses mocked prompts and configs
- Faster iteration during development
- No AWS dependencies

**When to use:**
- Developing agent logic
- Testing without AWS access
- Quick iteration on prompt changes
- CI/CD where DynamoDB isn't available

---

## Typical Setup Flow

### 1. First Time Setup

```bash
# Step 1: Test AWS connection
python setup/test_bedrock_boto3.py

# Step 2: Test LangChain integration
python setup/test_bedrock_connection.py

# Step 3: Update your first agent configuration
python scripts/update_config.py all fake_news_detector_v1

# Step 4: Run integration tests
python tests/quick_test.py
```

### 2. Troubleshooting

If agent tests fail, run setup tests to isolate the issue:

```bash
# Test 1: Can you connect to AWS?
python setup/test_bedrock_boto3.py

# Test 2: Is LangChain working?
python setup/test_bedrock_connection.py

# Test 3: Is agent logic working?
python setup/test_offline_stub.py
```

## Common Issues

### ❌ "Credentials not found"
→ Run: `python setup/test_bedrock_boto3.py`  
→ Fix: Check `.env` file has AWS credentials

### ❌ "langchain_aws not found"
→ Run: `pip install langchain-aws`  
→ Then: `python setup/test_bedrock_connection.py`

### ❌ "Model not found"
→ Go to AWS Bedrock Console > Model access  
→ Enable Amazon Nova Micro model

### ❌ "Agent config not found"
→ Run: `python scripts/update_config.py all fake_news_detector_v1`

## Development Workflow

```bash
# 1. Make changes to prompt or config templates
vim configs/prompts/fake_news_detector_v1.txt

# 2. Test offline (no AWS)
python setup/test_offline_stub.py

# 3. Update configuration in DynamoDB
python scripts/update_config.py all fake_news_detector_v1

# 4. Run full integration test
python tests/quick_test_verbose.py
```

## These are NOT integration tests

Scripts here are **setup/verification only**. They don't test the full agent workflow.

For integration tests, see: `tests/`
