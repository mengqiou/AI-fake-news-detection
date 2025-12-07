## 🔍 Platform Verification - How It Works

## The "Given Platform" Concept

Your AI agent doesn't just analyze content in isolation - it has access to a **"given platform"** (verification database) where it can search for fact-checked claims.

### Architecture

```
┌─────────────┐
│    User     │
│  "Bleach    │
│  cures      │
│  COVID?"    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     AI Agent                        │
│  1. Receives claim                  │
│  2. Uses verify_on_platform tool    │
│  3. Gets platform response          │
│  4. Provides assessment             │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Verification Platform Database     │
│  (Fact-checking sources)            │
│                                     │
│  ✅ TRUE: Verified claims           │
│  ❌ FALSE: Debunked claims          │
│  ❓ UNVERIFIED: Not in database     │
└─────────────────────────────────────┘
```

## Example Workflow

### Example 1: Fake News IN Database

**User Input:**
```
"I heard that drinking bleach cures COVID-19"
```

**Agent Workflow:**
1. Agent receives claim
2. Agent calls `verify_on_platform("drinking bleach cures COVID-19")`
3. Platform returns:
   ```
   ❌ Status: FALSE
   Verified By: CDC, WHO, FDA
   Summary: Extremely dangerous, thoroughly debunked
   ```
4. Agent provides assessment:
   ```
   Platform Verification: FOUND - Status FALSE
   Credibility Score: 0/100
   This claim has been debunked by the verification platform
   ```

### Example 2: Real News IN Database

**User Input:**
```
"NASA's Webb Telescope detected CO2 on an exoplanet"
```

**Agent Workflow:**
1. Agent receives claim
2. Agent calls `verify_on_platform("nasa webb telescope carbon dioxide")`
3. Platform returns:
   ```
   ✅ Status: TRUE
   Verified By: NASA, ESA, Nature Journal
   Sources: nasa.gov, nature.com
   ```
4. Agent provides assessment:
   ```
   Platform Verification: FOUND - Status TRUE
   Credibility Score: 95/100
   This claim is verified by the platform with credible sources
   ```

### Example 3: Claim NOT IN Database

**User Input:**
```
"Eating chocolate improves memory by 50%"
```

**Agent Workflow:**
1. Agent receives claim
2. Agent calls `verify_on_platform("chocolate improves memory 50%")`
3. Platform returns:
   ```
   ❓ Status: UNVERIFIED
   Message: Claim not found in verification platform
   ```
4. Agent provides assessment:
   ```
   Platform Verification: NOT FOUND
   Cannot verify on the dedicated platform
   Credibility Score: 40/100
   Needs more investigation - no verification available
   ```

## The Tool: `verify_on_platform`

### Purpose
Searches the verification database for claims that have been fact-checked.

### Usage by Agent
```python
# Agent automatically calls this when analyzing claims
result = verify_on_platform("5G causes COVID")

# Returns structured verification data:
# - Status (TRUE/FALSE/UNVERIFIED)
# - Who verified it
# - Evidence and sources
# - Confidence level
```

### Stubbed Database (Demo)
For testing, we include common fake news examples:
- ❌ "Bleach cures COVID" → FALSE
- ❌ "5G mind control" → FALSE  
- ❌ "Vaccine kidnapper scam" → FALSE
- ✅ "NASA Webb CO2 detection" → TRUE
- ✅ "UK inflation 4.2%" → TRUE

### Production Implementation
In a real system, this would connect to:
- **Fact-checking APIs**: Snopes, FactCheck.org, PolitiFact
- **News APIs**: Reuters, AP, trusted news sources
- **Social Media APIs**: Verified content from platforms
- **Custom Database**: Your own curated fact-checks

## Key Benefits

### 1. **Authoritative Source**
Instead of just "guessing," the agent checks an actual database.

### 2. **Clear Provenance**
"I found this on the verification platform" vs. "I think this might be fake"

### 3. **Transparent**
Users can see: "Verified by CDC, WHO" with source links

### 4. **Handles Unknowns**
Agent explicitly says "Cannot verify on platform" when claim not found

## Testing Platform Verification

### Quick Test
```bash
python tests/test_platform_verification.py
```

This runs through:
1. Fake news that's in the platform
2. Real news that's in the platform
3. Claims not in the platform

### What to Expect

**For claims IN platform:**
```
Platform Verification: ✅ FOUND
Status: FALSE/TRUE
Verified by: [sources]
Agent uses platform's verdict
```

**For claims NOT in platform:**
```
Platform Verification: ❓ NOT FOUND
Cannot verify on the dedicated platform
Agent recommends caution and further investigation
```

## Customizing the Platform

### Adding New Verified Claims

Edit `backend/app/tools/platform_verification_tool.py`:

```python
VERIFICATION_PLATFORM_DB = {
    "your claim here": {
        "status": "FALSE",  # or "TRUE"
        "verified_by": "Source names",
        "summary": "Explanation of verification",
        "source_urls": ["http://..."],
        "confidence": "HIGH"
    },
    # ... more claims
}
```

### Connecting to Real APIs

Replace the stubbed database with API calls:

```python
def search_in_verification_platform(query: str):
    # Instead of checking VERIFICATION_PLATFORM_DB
    
    # Call actual fact-checking API
    snopes_result = requests.get(
        "https://api.snopes.com/search",
        params={"q": query}
    ).json()
    
    # Process and return
    return format_snopes_response(snopes_result)
```

## Integration with Social Media Platforms

### Twitter/X Example
```python
# When webhook receives a tweet
@app.post("/webhook/twitter")
def twitter_webhook(tweet_data):
    # Extract claim from tweet
    claim = tweet_data['text']
    
    # Send to agent with platform verification
    result = handle_standalone_agent_request(
        config_id="fake-news-detector-v1",
        user_input=f"Verify this claim: {claim}"
    )
    
    # Agent searches platform and responds
    if "FALSE" in result['result']:
        # Flag the tweet, add warning label
        twitter_api.flag_misinformation(tweet_data['id'])
```

### Facebook Example
```python
# When content moderation queue receives a post
def moderate_post(post):
    # Send to agent
    result = handle_standalone_agent_request(
        config_id="fake-news-detector-v1",
        user_input=f"Verify this claim: {post.content}"
    )
    
    # Check if platform verified
    if "Platform Verification: FOUND - Status FALSE" in result['result']:
        return {"action": "flag", "reason": "Verified as false by platform"}
    elif "Platform Verification: NOT FOUND" in result['result']:
        return {"action": "review", "reason": "Needs human review"}
    else:
        return {"action": "approve"}
```

## Summary

The "given platform" is the **source of truth** that your agent consults:
- ✅ Agent searches platform first
- 📊 Platform provides verified data
- 🤖 Agent interprets and explains
- 👤 User gets transparent, authoritative answer

This is the key difference from just "asking an AI" - your agent has a real database to verify against!
