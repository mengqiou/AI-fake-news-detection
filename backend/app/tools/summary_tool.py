from typing import Optional
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os


@tool
def summary_long_text(text: str, max_length: int = 500) -> str:
    """
    Summarize long text to manage context window.
    Use this tool when you encounter articles or text longer than 1000 characters.
    
    Args:
        text: The long text to summarize
        max_length: Maximum length of summary in words (default: 500)
        
    Returns:
        A concise summary of the text
    """
    if not text or len(text) < 1000:
        return text
    
    try:
        # Initialize LLM for summarization (using faster/cheaper model)
        # TODO: Configure model from environment
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        prompt = f"""Summarize the following text in {max_length} words or less. 
Focus on key facts, claims, and important details.

Text:
{text}

Summary:"""
        
        response = llm.invoke(prompt)
        summary = response.content
        
        return summary
        
    except Exception as e:
        # Fallback: return first N characters if LLM fails
        fallback_length = max_length * 5  # Roughly 5 chars per word
        return f"[Summary unavailable: {str(e)}]\n\nFirst {fallback_length} chars:\n{text[:fallback_length]}..."
