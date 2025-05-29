import os
from langchain_openai import ChatOpenAI
from prompt_template import blog_prompt
from utils import sanitize_filename, save_markdown
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def generate_blog(topic: str) -> str:
    prompt = blog_prompt.format(topic=topic)
    response = llm.invoke(prompt)
    filename = sanitize_filename(topic) + ".md"
    return save_markdown(filename, response.content)