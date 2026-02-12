"""
Platform Verification Tool

This tool allows the agent to search and verify claims against a "given platform"
(e.g., fact-checking database, trusted news sources, or verification APIs).

In a real implementation, this would connect to:
- Fact-checking APIs (Snopes, FactCheck.org, PolitiFact)
- News wire APIs (Reuters, AP)
- Custom verification database
- Social media platform APIs with verified content

For testing, we stub it with sample data.
"""

from typing import Any, Dict, Optional

from langchain_core.tools import tool

# Mock verification database - simulates a "given platform"
# In production, this would be replaced with actual API calls
VERIFICATION_PLATFORM_DB = {
    "bleach cures covid": {
        "status": "FALSE",
        "verified_by": "CDC, WHO, FDA",
        "summary": "Drinking or injecting bleach is extremely dangerous and does not cure COVID-19. This has been thoroughly debunked by medical authorities.",
        "source_urls": [
            "https://www.cdc.gov/coronavirus/2019-ncov/faq.html",
            "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters",
        ],
        "confidence": "HIGH",
    },
    "5g causes covid": {
        "status": "FALSE",
        "verified_by": "WHO, FCC, Scientific Community",
        "summary": "There is no scientific evidence linking 5G technology to COVID-19. Viruses cannot travel on radio waves or mobile networks.",
        "source_urls": [
            "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters"
        ],
        "confidence": "HIGH",
    },
    "5g towers mind control": {
        "status": "FALSE",
        "verified_by": "Scientific Community, FCC",
        "summary": "This is a conspiracy theory with no scientific basis. 5G technology uses radio waves and cannot control minds or spread viruses.",
        "source_urls": [],
        "confidence": "HIGH",
    },
    "nasa webb telescope carbon dioxide exoplanet": {
        "status": "TRUE",
        "verified_by": "NASA, ESA, Nature Journal",
        "summary": "NASA's James Webb Space Telescope detected carbon dioxide in the atmosphere of exoplanet WASP-39 b in August 2022. Published in peer-reviewed journals.",
        "source_urls": [
            "https://www.nasa.gov/webb",
            "https://www.nature.com/articles/s41586-022-05269-w",
        ],
        "confidence": "HIGH",
    },
    "uk inflation 4.2 percent november 2023": {
        "status": "TRUE",
        "verified_by": "Office for National Statistics (ONS), BBC",
        "summary": "UK inflation fell to 4.2% in November 2023, down from 4.6% in October, according to official ONS statistics.",
        "source_urls": [
            "https://www.ons.gov.uk/economy/inflationandpriceindices",
            "https://www.bbc.com/news/business",
        ],
        "confidence": "HIGH",
    },
    "vaccine kidnappers door scam": {
        "status": "FALSE",
        "verified_by": "Police Departments, Fact-checking orgs",
        "summary": "This is a common WhatsApp hoax that has circulated in various forms. No credible reports of such incidents exist. Vaccines are not administered door-to-door in this manner.",
        "source_urls": [],
        "confidence": "HIGH",
    },
}


def normalize_search_query(query: str) -> str:
    """Normalize query for matching against database."""
    return query.lower().strip()


def search_in_verification_platform(query: str) -> Optional[Dict[str, Any]]:
    """
    Search the verification platform for a claim.

    This is a simplified version. In production, this would:
    - Make API calls to fact-checking services
    - Search news archives
    - Query verification databases

    Args:
        query: The claim or news to verify

    Returns:
        Verification result or None if not found
    """
    normalized_query = normalize_search_query(query)

    # Check for partial matches in our database
    for key, value in VERIFICATION_PLATFORM_DB.items():
        # Check if key terms match
        key_terms = key.split()
        query_terms = normalized_query.split()

        # If most key terms are in the query, consider it a match
        matches = sum(1 for term in key_terms if term in query_terms)
        if matches >= max(2, len(key_terms) * 0.6):  # At least 60% match
            return value

    return None


@tool
def verify_on_platform(claim: str) -> str:
    """
    Verify a claim or news article against the trusted verification platform.

    This tool searches a dedicated fact-checking and verification database
    to determine if the claim has been verified or debunked.

    Use this tool when you need to check if a claim:
    - Has been fact-checked by trusted sources
    - Appears in verified news databases
    - Has been debunked or confirmed

    Args:
        claim: The claim, news headline, or statement to verify

    Returns:
        Verification result from the platform including:
        - Status (TRUE/FALSE/UNVERIFIED)
        - Sources that verified it
        - Supporting evidence and URLs
        - Confidence level
    """
    result = search_in_verification_platform(claim)

    if result is None:
        return f"""PLATFORM VERIFICATION RESULT:
Status: UNVERIFIED
Message: This claim was not found in the verification platform database.
Recommendation: Cannot verify this claim on the dedicated platform. The claim may be:
  - Too new to have been fact-checked yet
  - Not widely circulated enough to be in the database
  - Requires additional investigation from other sources

Without verification from the platform, treat this claim with caution."""

    # Format the verification result
    status_emoji = "✅" if result["status"] == "TRUE" else "❌"

    output = f"""PLATFORM VERIFICATION RESULT:
{status_emoji} Status: {result['status']}
Verified By: {result['verified_by']}
Confidence: {result['confidence']}

Summary:
{result['summary']}
"""

    if result.get("source_urls"):
        output += "\nSources:\n"
        for url in result["source_urls"]:
            output += f"  - {url}\n"

    return output


# Export for tool registration
def get_platform_verification_tool():
    """Get the platform verification tool for agent use."""
    return verify_on_platform
