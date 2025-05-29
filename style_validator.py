from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def validate_style(markdown: str) -> str:
    prompt = f"""
You are a markdown blog formatter. Your job is to:
- Ensure developer tone: clear, concise, and technical.
- Fix generic statements by making them specific.
- Add markdown-based code formatting where necessary.
- Use consistent heading levels, bullet points, and paragraph spacing.
- Return the cleaned and styled markdown, not a review.

INPUT:
===
{markdown}

OUTPUT:
"""
    response = llm.invoke(prompt)
    return response.content