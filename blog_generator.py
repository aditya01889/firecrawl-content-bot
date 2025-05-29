import os
from langchain_openai import ChatOpenAI
from prompt_template import blog_prompt
from utils import sanitize_filename, save_markdown
from dotenv import load_dotenv
from config import OPENROUTER_API_KEY, BASE_URL, MODEL_NAME
load_dotenv()

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

def generate_blog(topic: str) -> str:
    prompt = blog_prompt.format(topic=topic)
    response = llm.invoke(prompt)
    filename = sanitize_filename(topic) + ".md"
    return save_markdown(filename, response.content)