from typing import Optional
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup


@tool
def search_internet(url: str, keyword: str) -> str:
    """
    Search the internet by fetching content from a URL and looking for a keyword.
    
    Args:
        url: The URL to fetch and search
        keyword: The keyword or phrase to search for in the content
        
    Returns:
        Text result containing the keyword context or full content
    """
    try:
        # Fetch the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Search for keyword
        if keyword.lower() in text.lower():
            # Find context around keyword (500 chars before and after)
            keyword_pos = text.lower().find(keyword.lower())
            start = max(0, keyword_pos - 500)
            end = min(len(text), keyword_pos + len(keyword) + 500)
            context = text[start:end]
            return f"Found '{keyword}' in URL {url}:\n\n{context}"
        else:
            return f"Keyword '{keyword}' not found in {url}. Returning first 1000 chars:\n\n{text[:1000]}"
            
    except Exception as e:
        return f"Error searching {url}: {str(e)}"
