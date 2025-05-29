import os
from datetime import datetime

OUTPUT_DIR = "output"
LOG_FILE = "error.log"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(topic: str) -> str:
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        topic = topic.replace(ch, "")
    return topic.lower().replace(" ", "_")

def save_markdown(filename: str, content: str) -> str:
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

def log_error(topic: str, error: Exception):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] ❌ Error for topic '{topic}': {str(error)}\n")

def markdown_to_notion_blocks(markdown: str):
    # Basic naive conversion: split by double newline, treat each as paragraph block
    blocks = []
    for paragraph in markdown.split('\n\n'):
        paragraph = paragraph.strip()
        if paragraph:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": paragraph}}]
                }
            })
    return blocks
