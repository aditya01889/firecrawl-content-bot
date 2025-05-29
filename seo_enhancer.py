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

def enhance_seo(markdown: str) -> str:
    prompt = f"""
    Improve the SEO of this markdown blog without changing its meaning or tone. Ensure keyword richness, add structured headers, use markdown syntax for code blocks if needed, and include meta description at the end if missing.

    ===
    {markdown}
    """
    response = llm.invoke(prompt)
    return response.content