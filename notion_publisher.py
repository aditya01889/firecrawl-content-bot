import os
import requests
from dotenv import load_dotenv
from config import NOTION_API_KEY, NOTION_DATABASE_ID

load_dotenv()


def parse_markdown_to_rich_text(text: str):
    """Parse markdown text into Notion rich text format with formatting."""
    rich_text = []
    i = 0
    n = len(text)
    
    while i < n:
        # Handle code blocks (```)
        if text.startswith('```', i):
            # End of current text if any
            if i > 0 and rich_text and rich_text[-1].get('text', {}).get('content'):
                rich_text[-1]['text']['content'] = rich_text[-1]['text']['content'].rstrip()
            
            # Find end of code block
            end = text.find('```', i + 3)
            if end == -1:  # Unclosed code block
                code = text[i+3:].strip()
                i = n
            else:
                code = text[i+3:end].strip()
                i = end + 3
                
            # Add code block
            return [
                {
                    "type": "text",
                    "text": {
                        "content": code
                    },
                    "annotations": {
                        "code": True
                    }
                }
            ]
            
        # Handle inline code (`)
        elif text[i] == '`':
            # End of current text if any
            if i > 0 and rich_text and rich_text[-1].get('text', {}).get('content'):
                rich_text[-1]['text']['content'] = rich_text[-1]['text']['content'].rstrip()
            
            # Find end of inline code
            end = text.find('`', i + 1)
            if end == -1:  # Unclosed inline code
                code = text[i+1:].strip()
                i = n
            else:
                code = text[i+1:end].strip()
                i = end + 1
                
            # Add inline code
            rich_text.append({
                "type": "text",
                "text": {
                    "content": code
                },
                "annotations": {
                    "code": True
                }
            })
            
        else:
            # Add regular text
            if not rich_text or not rich_text[-1].get('text', {}).get('content'):
                rich_text.append({
                    "type": "text",
                    "text": {
                        "content": ""
                    }
                })
            rich_text[-1]['text']['content'] += text[i]
            i += 1
    
    return rich_text

def split_content_to_blocks(content: str):
    """Split content into Notion blocks with proper markdown parsing."""
    # Split by double newlines first
    paragraphs = content.split('\n\n')
    blocks = []
    in_code_block = False
    current_code_block = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # Handle code blocks
        if para.startswith('```'):
            if in_code_block:
                # End of code block
                code_content = '\n'.join(current_code_block)
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": code_content}}],
                        "language": "plain text"
                    }
                })
                in_code_block = False
                current_code_block = []
            else:
                # Start of code block
                in_code_block = True
                continue
        elif in_code_block:
            # Inside code block, collect lines
            current_code_block.append(para)
            continue
            
        # Handle headings
        if para.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": parse_markdown_to_rich_text(para[2:].strip())
                }
            })
        elif para.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": parse_markdown_to_rich_text(para[3:].strip())
                }
            })
        elif para.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": parse_markdown_to_rich_text(para[4:].strip())
                }
            })
        # Handle lists
        elif para.startswith("- ") or para.startswith("* "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": parse_markdown_to_rich_text(para[2:].strip())
                }
            })
        elif para[0].isdigit() and ". " in para[:5]:
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": parse_markdown_to_rich_text(para[para.find(" ")+1:].strip())
                }
            })
        # Handle quotes
        elif para.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": parse_markdown_to_rich_text(para[2:].strip())
                }
            })
        # Handle toggles
        elif para.startswith("<details>") and "</details>" in para:
            summary = para[para.find("<summary>")+9:para.find("</summary>")].strip()
            content = para[para.find("</summary>")+10:para.find("</details>")].strip()
            blocks.append({
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": parse_markdown_to_rich_text(summary),
                    "children": split_content_to_blocks(content)
                }
            })
        # Default to paragraph
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": parse_markdown_to_rich_text(para)
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
