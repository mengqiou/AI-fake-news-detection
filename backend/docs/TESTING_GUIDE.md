# Quick Testing Guide

## 🚀 Quick Start (Fastest Way)

After setting up your agent, test it immediately:

```bash
cd backend
python tests/quick_test.py
```

This will analyze a simple fake news tweet and show you the agent's response in ~15 seconds.

---

## 📋 All Testing Options

### Option 1: Quick Test ⚡
**Best for:** First-time verification
```bash
python tests/quick_test.py
```
- Takes 10-30 seconds
- Tests one simple example
- Shows agent is working

### Option 2: Comprehensive Test Suite 📊
**Best for:** Testing multiple scenarios
```bash
python tests/test_fake_news_agent_local.py
```
- Choose from 4 modes:
  1. Run all samples (5 different news types)
  2. Run specific sample
  3. Interactive mode (enter your own news)
  4. Quick test

**Includes:**
- Twitter fake news
- Facebook misinformation  
- WhatsApp rumors
- BBC credible news
- Reuters scientific news

### Option 3: Offline Stub Test 🔌
**Best for:** Development without DynamoDB
```bash
python tests/test_offline_stub.py
```
- No DynamoDB required
- Uses mocked data
- Faster iteration during development

---

## 🎯 Example Test Flow

### Interactive Testing Example:

```bash
$ python tests/test_fake_news_agent_local.py

Choose test mode:
  1. Run all sample tests
  2. Run specific sample test
  3. Interactive mode (enter your own news)
  4. Quick test (just one sample)

Your choice (1-4): 3

Platform: Twitter
Content: Breaking: Moon landing was faked! [Enter twice when done]

Analyzing...
================================================================================
AGENT RESPONSE:
================================================================================
Credibility Score: 10/100

Key Findings:
- This is a well-known conspiracy theory
- No credible evidence supports this claim
- Thoroughly debunked by experts

Red Flags:
1. Conspiracy theory claim
2. No sources provided
3. Contradicts documented historical evidence

Recommendation: LIKELY FALSE
This is a widely debunked conspiracy theory...
```

---

## 🔧 Before You Test

### 1. Set up the agent (one-time):
```bash
cd backend
python scripts/setup_first_agent.py
```

### 2. Ensure AWS is configured:
Check your `.env` file:
```
AWS_REGION=ap-southeast-2
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### 3. Install dependencies:
```bash
pip install langchain-aws
```

---

## 📊 What to Expect

### For Fake News (Twitter bleach example):
```
Credibility Score: 0-10/100
Red Flags: Dangerous medical misinformation, no sources
Recommendation: LIKELY FALSE - DANGEROUS
```

### For Credible News (BBC/Reuters):
```
Credibility Score: 80-95/100
Red Flags: None or minimal
Recommendation: LIKELY TRUE
```

### For Misleading Content:
```
Credibility Score: 30-50/100
Red Flags: Bias, sensational language, missing context
Recommendation: POSSIBLY MISLEADING
```

---

## 🐛 Common Issues

### "Agent configuration not found"
→ Run: `python scripts/setup_first_agent.py`

### "You must specify a region"
→ Check `.env` has `AWS_REGION=ap-southeast-2`

### "Bedrock access denied"
→ Verify AWS credentials and Bedrock is enabled in your region

### Agent response is slow
→ Normal! First call takes 20-30s (cold start). Subsequent calls are faster (5-15s).

---

## 💡 Next Steps After Testing

1. **Add tools** to agent config (search_internet, fact-check APIs)
2. **Customize prompt** for your specific platform
3. **Build API wrapper** (FastAPI, Flask, or Lambda)
4. **Set up webhooks** from social media platforms
5. **Add monitoring** and alerting

---

## 📈 Testing Your Own Integration

### Simulate Platform Webhook:

```python
# In your platform webhook handler:
from app.handlers.standalone_agent_handler import handle_standalone_agent_request

def twitter_webhook(tweet_data):
    user_input = f"""
    Analyze this tweet:
    
    Platform: Twitter
    Content: {tweet_data['text']}
    Author: {tweet_data['author']}
    Retweets: {tweet_data['retweet_count']}
    
    Assess credibility.
    """
    
    result = handle_standalone_agent_request(
        config_id="fake-news-detector-v1",
        user_input=user_input
    )
    
    if result["success"]:
        # Flag, report, or alert based on result
        credibility = extract_score(result["result"])
        if credibility < 30:
            flag_tweet_as_misinformation(tweet_data['id'])
    
    return result
```

---

## 📖 Full Documentation

See `tests/README.md` for detailed documentation including:
- All test cases explained
- Platform integration examples
- Performance optimization tips
- Cost estimation
- Troubleshooting guide

---

**Ready to test?** Run: `python tests/quick_test.py` 🚀
