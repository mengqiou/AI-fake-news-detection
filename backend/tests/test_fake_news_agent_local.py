"""
Local test script for the fake news detection agent.

This script simulates a platform (Twitter, Facebook, etc.) triggering the agent
to verify whether a piece of news is fake or not.

Usage:
    python tests/test_fake_news_agent_local.py
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from datetime import datetime

from app.handlers.standalone_agent_handler import \
    handle_standalone_agent_request

# Sample fake news examples from different platforms
SAMPLE_NEWS_ARTICLES = {
    "twitter_fake": {
        "platform": "Twitter",
        "content": """
        BREAKING: Scientists confirm that drinking bleach cures COVID-19! 
        The CDC is hiding this from you! Share before they delete this! 
        #COVID #Truth #WakeUp
        """,
        "metadata": {
            "author": "@truthseeker9999",
            "likes": 50000,
            "retweets": 25000,
            "verified": False,
        },
    },
    "facebook_misleading": {
        "platform": "Facebook",
        "content": """
        Did you know that 5G towers are controlling your mind? 
        A leaked government document shows they're using 5G to spread the virus.
        My uncle works for the military and confirmed this is true.
        Share this before Facebook deletes it!
        """,
        "metadata": {
            "author": "Truth Warriors United",
            "shares": 10000,
            "reactions": 35000,
        },
    },
    "news_site_real": {
        "platform": "Reuters",
        "content": """
        NASA's James Webb Space Telescope has detected carbon dioxide in the atmosphere 
        of an exoplanet for the first time. The planet, WASP-39 b, is a hot gas giant 
        orbiting a star 700 light-years away. This discovery was published in Nature 
        and represents a significant step in understanding exoplanet atmospheres.
        
        Source: https://www.nasa.gov/webb
        Published: August 25, 2022
        """,
        "metadata": {
            "author": "NASA/ESA",
            "source": "Official NASA Release",
            "peer_reviewed": True,
        },
    },
    "whatsapp_rumor": {
        "platform": "WhatsApp",
        "content": """
        ⚠️ URGENT WARNING ⚠️
        
        Police are warning about a new scam where kidnappers are offering free 
        COVID vaccines at your door. They inject you with poison instead!
        
        Forward to all your family groups immediately!
        
        - Forwarded many times
        """,
        "metadata": {"forwarded": True, "source": "Unknown"},
    },
    "credible_news": {
        "platform": "BBC News",
        "content": """
        UK inflation rate falls to 4.2% in November 2023
        
        The UK's inflation rate fell to 4.2% in November, down from 4.6% in October,
        according to the Office for National Statistics. This is the lowest rate since
        September 2021. The decline was largely driven by falling fuel prices.
        
        The Bank of England had forecast inflation to fall to around 4.5% by the end of 2023.
        
        Source: ONS Official Statistics
        Published: December 20, 2023
        Reporter: BBC Economics Correspondent
        """,
        "metadata": {
            "author": "BBC Economics Team",
            "source": "Office for National Statistics",
            "fact_checked": True,
            "citations": ["ONS", "Bank of England"],
        },
    },
}


def format_analysis_request(article_key: str) -> str:
    """
    Format a news article into a structured request for the agent.

    Args:
        article_key: Key of the article in SAMPLE_NEWS_ARTICLES

    Returns:
        Formatted string for agent analysis
    """
    article = SAMPLE_NEWS_ARTICLES[article_key]

    request = f"""Please analyze the following content for potential fake news or misinformation:

PLATFORM: {article['platform']}

CONTENT:
{article['content'].strip()}

METADATA:
{json.dumps(article['metadata'], indent=2)}

Please provide your analysis including:
1. Credibility Score (0-100)
2. Key Findings
3. Red Flags (if any)
4. Evidence Assessment
5. Recommendation (likely true / possibly misleading / likely false / needs investigation)
"""

    return request


def run_test(article_key: str, config_id: str = "fake-news-detector-v1"):
    """
    Run a test with a specific news article.

    Args:
        article_key: Key of the article to test
        config_id: Agent configuration ID
    """
    print("=" * 80)
    print(f"TEST: {article_key.upper()}")
    print("=" * 80)

    article = SAMPLE_NEWS_ARTICLES[article_key]
    print(f"\nPlatform: {article['platform']}")
    print(f"Content Preview: {article['content'].strip()[:150]}...")
    print("\n" + "-" * 80)
    print("Sending to Fake News Detection Agent...")
    print("-" * 80 + "\n")

    # Format the request
    user_input = format_analysis_request(article_key)

    # Call the handler
    try:
        result = handle_standalone_agent_request(
            config_id=config_id, user_input=user_input
        )

        if result["success"]:
            print("✅ ANALYSIS SUCCESSFUL")
            print(f"\nExecution ID: {result['execution_id']}")
            print("\n" + "=" * 80)
            print("AGENT RESPONSE:")
            print("=" * 80)
            print(result["result"])
            print("\n" + "=" * 80)
            print("METADATA:")
            print("=" * 80)
            print(json.dumps(result["metadata"], indent=2))
        else:
            print("❌ ANALYSIS FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 80 + "\n")


def interactive_mode(config_id: str = "fake-news-detector-v1"):
    """
    Interactive mode - user can input their own news to verify.
    """
    print("=" * 80)
    print("FAKE NEWS DETECTION - INTERACTIVE MODE")
    print("=" * 80)
    print("\nEnter a news article, claim, or social media post to analyze.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        print("-" * 80)
        platform = input("Platform (e.g., Twitter, Facebook, News Site): ").strip()

        if platform.lower() in ["quit", "exit"]:
            break

        print("\nEnter the content (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)

        content = "\n".join(lines[:-1])  # Remove last empty line

        if not content.strip():
            print("⚠️  No content provided. Try again.\n")
            continue

        # Format request
        user_input = f"""Please analyze the following content for potential fake news or misinformation:

PLATFORM: {platform}

CONTENT:
{content}

Please provide your analysis including:
1. Credibility Score (0-100)
2. Key Findings  
3. Red Flags (if any)
4. Evidence Assessment
5. Recommendation (likely true / possibly misleading / likely false / needs investigation)
"""

        print("\n" + "-" * 80)
        print("Analyzing...")
        print("-" * 80 + "\n")

        try:
            result = handle_standalone_agent_request(
                config_id=config_id, user_input=user_input
            )

            if result["success"]:
                print("✅ ANALYSIS COMPLETE\n")
                print("=" * 80)
                print("AGENT RESPONSE:")
                print("=" * 80)
                print(result["result"])
                print("\n")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}\n")

        except Exception as e:
            print(f"❌ ERROR: {str(e)}\n")
            import traceback

            traceback.print_exc()


def main():
    """
    Main test runner.
    """
    print("\n" + "=" * 80)
    print(" " * 20 + "FAKE NEWS DETECTION AGENT - LOCAL TEST")
    print("=" * 80 + "\n")

    print("Configuration:")
    print(f"  AWS Region: {os.getenv('AWS_REGION', 'Not set')}")
    print(f"  Agent Config: fake-news-detector-v1")
    print(f"  Timestamp: {datetime.now().isoformat()}")
    print("\n")

    # Show menu
    print("Choose test mode:")
    print("  1. Run all sample tests")
    print("  2. Run specific sample test")
    print("  3. Interactive mode (enter your own news)")
    print("  4. Quick test (just one sample)")

    choice = input("\nYour choice (1-4): ").strip()

    if choice == "1":
        # Run all tests
        for article_key in SAMPLE_NEWS_ARTICLES.keys():
            run_test(article_key)
            input("\nPress Enter to continue to next test...")

    elif choice == "2":
        # Run specific test
        print("\nAvailable samples:")
        for i, key in enumerate(SAMPLE_NEWS_ARTICLES.keys(), 1):
            print(f"  {i}. {key}")

        sample_choice = input("\nEnter number: ").strip()
        try:
            idx = int(sample_choice) - 1
            article_key = list(SAMPLE_NEWS_ARTICLES.keys())[idx]
            run_test(article_key)
        except (ValueError, IndexError):
            print("❌ Invalid choice")

    elif choice == "3":
        # Interactive mode
        interactive_mode()

    elif choice == "4":
        # Quick test with one sample
        print("\n🚀 Running quick test with Twitter fake news sample...\n")
        run_test("twitter_fake")

    else:
        print("❌ Invalid choice")

    print("\n" + "=" * 80)
    print("TEST SESSION COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
