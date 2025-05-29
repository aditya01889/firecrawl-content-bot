from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def enhance_seo(markdown: str) -> str:
    prompt = f"""
    Improve the SEO of this markdown blog without changing its meaning or tone. Ensure keyword richness, add structured headers, use markdown syntax for code blocks if needed, and include meta description at the end if missing.

    ===
    {markdown}
    """
    response = llm.invoke(prompt)
    return response.content