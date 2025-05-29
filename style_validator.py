from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from config import OPENROUTER_API_KEY, BASE_URL, MODEL_NAME

load_dotenv()

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

def validate_style(markdown: str) -> str:
    prompt = f"""
You are a markdown blog formatter. Your job is to improve the technical content while preserving all styling and formatting:

1. PRESERVE ALL EXISTING STYLING including:
   - Headers (keep all # levels exactly as is)
   - Code blocks (```) and inline code (`)
   - Links, images, and other markdown formatting
   - Lists, blockquotes, and other structural elements

2. Make these improvements:
   - Ensure developer tone: clear, concise, and technical
   - Fix generic statements by making them specific
   - Add code formatting where missing (but don't modify existing code blocks)
   - Maintain consistent spacing and formatting
   - Don't add or remove sections, just improve the content

3. Return ONLY the improved markdown with all original styling preserved.

INPUT MARKDOWN:
===
{markdown}

IMPROVED MARKDOWN (preserve all styling):
"""
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error in style validation: {str(e)}")
        return markdown  # Return original if there's an error