import os
import requests
from dotenv import load_dotenv
from config import NOTION_API_KEY, NOTION_DATABASE_ID

load_dotenv()


def split_content_to_blocks(content: str):
    paragraphs = content.split('\n\n')
    blocks = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Markdown-style heading support
        if para.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": para[2:].strip()}}]
                }
            })
        elif para.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": para[3:].strip()}}]
                }
            })
        elif para.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": para[4:].strip()}}]
                }
            })
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": para}}]
                }
            })
    return blocks

def publish_to_notion(title: str, content: str) -> str:
    print(f"🚀 Publishing to Notion: {title}")
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    blocks = split_content_to_blocks(content)
    if not blocks:
        print("⚠️ No blocks generated from content")
        return ""

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]}
        },
        "children": blocks
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

    if response.status_code != 200:
        print("❌ Failed to publish to Notion:", response.text)
        return ""

    notion_url = response.json().get("url", "")
    print(f"✅ Notion page created: {notion_url}")
    return notion_url
