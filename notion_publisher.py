import os
import requests
from dotenv import load_dotenv
from config import NOTION_API_KEY, NOTION_DATABASE_ID

load_dotenv()


def parse_markdown_to_rich_text(text: str):
    """Parse markdown text into Notion rich text format with formatting."""
    if not text or not text.strip():
        return [{"type": "text", "text": {"content": text or ""}}]
    
    # Default text annotations
    default_annotations = {
        "bold": False,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default"
    }
    
    # If the text is just a code block, return it as plain text
    if text.strip().startswith('```') and text.strip().endswith('```'):
        code_content = text.strip().strip('```').strip()
        return [{
            "type": "text",
            "text": {"content": code_content},
            "annotations": {**default_annotations, "code": True}
        }]
    
    # Simple case: no markdown formatting
    if not any(char in text for char in ['`', '**', '__', '*', '_']):
        return [{
            "type": "text",
            "text": {"content": text},
            "annotations": default_annotations
        }]
    
    # Handle inline code and other formatting
    rich_text = []
    i = 0
    n = len(text)
    current_text = ""
    
    while i < n:
        # Handle inline code (`)
        if text[i] == '`' and (i == 0 or text[i-1] != '`'):
            # Add any accumulated text
            if current_text:
                rich_text.append({
                    "type": "text",
                    "text": {"content": current_text},
                    "annotations": default_annotations
                })
                current_text = ""
            
            # Find end of inline code
            end = text.find('`', i + 1)
            if end == -1:  # Unclosed inline code
                code = text[i+1:]
                i = n
            else:
                code = text[i+1:end]
                i = end + 1
            
            # Add inline code
            if code.strip():
                rich_text.append({
                    "type": "text",
                    "text": {"content": code},
                    "annotations": {**default_annotations, "code": True}
                })
            continue
            
        # Add character to current text
        current_text += text[i]
        i += 1
    
    # Add any remaining text
    if current_text:
        rich_text.append({
            "type": "text",
            "text": {"content": current_text},
            "annotations": default_annotations
        })
    
    # If we didn't add any rich text, return a simple text node
    if not rich_text:
        return [{
            "type": "text",
            "text": {"content": text},
            "annotations": default_annotations
        }]
    
    return rich_text

def split_content_to_blocks(content: str):
    """Split content into Notion blocks with proper markdown parsing."""
    print("\n=== SPLIT_CONTENT_TO_BLOCKS START ===")
    # Remove any Windows-style line endings and normalize line endings
    content = content.replace('\r\n', '\n')
    
    # Split into lines first to better handle code blocks
    lines = content.split('\n')
    blocks = []
    current_paragraph = []
    in_code_block = False
    current_code_block = []
    code_block_count = 0
    
    def add_paragraph():
        nonlocal current_paragraph
        if current_paragraph:
            text = '\n'.join(current_paragraph).strip()
            if text:  # Only add non-empty paragraphs
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": parse_markdown_to_rich_text(text)
                    }
                })
            current_paragraph = []
    
    for line in lines:
        line = line.strip()
        
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                # End of code block
                code_block_count += 1
                print(f"\n=== CODE BLOCK {code_block_count} ===")
                
                # Join all code lines
                code_content = '\n'.join(current_code_block)
                
                # Check if first line is a language specifier
                language = 'plain text'
                valid_languages = {
                    'python', 'javascript', 'typescript', 'java', 'c', 'c++', 'c#', 'go', 'ruby',
                    'php', 'swift', 'kotlin', 'rust', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
                    'json', 'yaml', 'markdown', 'bash', 'shell', 'powershell', 'plain text'
                }
                
                if current_code_block and '```' not in current_code_block[0]:
                    possible_lang = current_code_block[0].strip().lower()
                    # Only use the language if it's in our valid set
                    if possible_lang and possible_lang != '```' and possible_lang in valid_languages:
                        language = possible_lang
                        code_content = '\n'.join(current_code_block[1:])  # Remove language line
                    elif possible_lang and possible_lang != '```':
                        # If language is specified but not in valid list, treat as plain text
                        print(f"Warning: Unsupported language '{possible_lang}', defaulting to 'plain text'")
                        code_content = '\n'.join(current_code_block)  # Keep the language line as part of content
                
                code_content = code_content.strip('`').strip()
                
                if code_content:  # Only add non-empty code blocks
                    code_block = {
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": code_content},
                                "annotations": {"code": True, "color": "default"}
                            }],
                            "language": language,
                            "caption": []
                        }
                    }
                    blocks.append(code_block)
                    print(f"Added code block with {len(code_content)} characters")
                
                in_code_block = False
                current_code_block = []
            else:
                # Start of code block
                add_paragraph()  # Add any pending paragraph
                in_code_block = True
                current_code_block = []
                language = line[3:].strip()
                if language:
                    print(f"Starting code block with language: {language}")
                else:
                    print("Starting code block with no language specified")
            continue
            
        if in_code_block:
            current_code_block.append(line)
            continue
            
        # Handle headings
        if line.startswith('### '):
            add_paragraph()
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:].strip()}}]}
            })
            continue
        elif line.startswith('## '):
            add_paragraph()
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}]}
            })
            continue
        elif line.startswith('# '):
            add_paragraph()
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]}
            })
            continue
            
        # Handle lists
        if line.startswith('- ') or line.startswith('* '):
            add_paragraph()
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": parse_markdown_to_rich_text(line[2:].strip())}
            })
            continue
            
        # Handle numbered lists (only if line is not empty)
        if line and line[0].isdigit() and ". " in line[:5]:
            add_paragraph()
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": parse_markdown_to_rich_text(line[line.find(" ")+1:].strip())}
            })
            continue
            
        # Handle quotes
        if line.startswith('> '):
            add_paragraph()
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": parse_markdown_to_rich_text(line[2:].strip())}
            })
            continue
            
        # If we get here, it's a regular line of text
        if line:  # Only add non-empty lines
            current_paragraph.append(line)
    
    # Add any remaining paragraph
    if not in_code_block:
        add_paragraph()
    
    print(f"Generated {len(blocks)} blocks")
    print(f"Found {code_block_count} code blocks")
    return blocks

def publish_to_notion(title: str, content: str) -> str:
    print(f"🚀 Publishing to Notion: {title}")
    print("=== ORIGINAL CONTENT ===")
    print(content[:500] + ("..." if len(content) > 500 else ""))
    print("=======================")
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # First, create the page with just the title
    page_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]}
        }
    }
    
    # Create the page first
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=page_data
    )
    
    if response.status_code != 200:
        print("❌ Failed to create Notion page:", response.text)
        return ""
    
    page_id = response.json()["id"]
    notion_url = response.json().get("url", "")
    
    print(f"✅ Notion page created: {notion_url}")
    
    # Now add the content blocks
    print("=== SPLITTING INTO BLOCKS ===")
    blocks = split_content_to_blocks(content)
    print(f"Generated {len(blocks)} blocks")
    if not blocks:
        print("⚠️ No blocks generated from content")
        return notion_url
        
    # Debug: Print block summary
    code_blocks = [b for b in blocks if b.get('type') == 'code']
    print(f"Found {len(code_blocks)} code blocks in content")
    
    # Print first few blocks for debugging
    print("\n=== SAMPLE BLOCKS ===")
    for i, block in enumerate(blocks[:min(5, len(blocks))]):
        block_type = block.get('type')
        print(f"Block {i+1}: {block_type}")
        if block_type == 'code':
            code_block = block.get('code', {})
            lang = code_block.get('language', 'plain text')
            content = code_block.get('rich_text', [{}])[0].get('text', {}).get('content', '')
            print(f"  Language: {lang}")
            print(f"  Content: {content[:100]}..." if len(content) > 100 else f"  Content: {content}")
    print("=====================")
    
    
    # Process blocks to ensure proper formatting
    print("=== PROCESSING BLOCKS ===")
    processed_blocks = []
    for i, block in enumerate(blocks):
        block_type = block.get('type')
        print(f"\nProcessing block {i+1}/{len(blocks)} - Type: {block_type}")
        
        # For code blocks, ensure they have the correct structure
        if block_type == "code":
            print("\n🔍 Found code block")
            code_block = block.get("code", {})
            
            # Get code content
            code_content = ""
            rich_text = code_block.get("rich_text", [])
            if isinstance(rich_text, list) and rich_text and isinstance(rich_text[0], dict):
                code_content = rich_text[0].get("text", {}).get("content", "")
            
            # Get language (default to 'plain text' if not specified)
            language = code_block.get("language", "plain text").lower()
            if not language or language == '``' or '`' in language:
                language = 'plain text'
            
            print(f"  Language: {language}")
            print(f"  Content: {code_content[:100]}{'...' if len(code_content) > 100 else ''}")
            
            # Only create a code block if we have content
            if code_content.strip():
                new_block = {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": code_content
                            },
                            "annotations": {
                                "code": True,
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "color": "default"
                            }
                        }],
                        "language": language,
                        "caption": []
                    }
                }
                processed_blocks.append(new_block)
                print("✅ Added code block")
            else:
                print("⚠️  Skipping empty code block")
        else:
            # For non-code blocks, just add them as they are
            processed_blocks.append(block)
            print(f"Added non-code block of type {block.get('type')}")
    
    print(f"\nTotal blocks after processing: {len(processed_blocks)}")
    print("=========================")
    
    # Add blocks to the page in chunks (Notion has a limit of 100 blocks per request)
    CHUNK_SIZE = 50
    for i in range(0, len(processed_blocks), CHUNK_SIZE):
        chunk = processed_blocks[i:i + CHUNK_SIZE]
        
        # Debug: Print the chunk being sent to Notion
        print(f"\n=== SENDING CHUNK {i//CHUNK_SIZE + 1} ===")
        print(f"Chunk size: {len(chunk)} blocks")
        for j, block in enumerate(chunk):
            print(f"  Block {j+1}: {block['type']}")
            if block['type'] == 'code':
                print(f"    Language: {block['code'].get('language', 'plain text')}")
        
        # Update the page with the blocks
        update_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        try:
            response = requests.patch(
                update_url,
                headers=headers,
                json={"children": chunk},
                timeout=30
            )
            
            if response.status_code not in (200, 201):
                print(f"⚠️ Failed to add blocks {i}-{i+len(chunk)} to Notion page:")
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.text}")
                print(f"Request payload: {chunk}")
            else:
                print(f"✅ Successfully added blocks {i}-{i+len(chunk)}")
                
        except Exception as e:
            print(f"⚠️ Exception while adding blocks {i}-{i+len(chunk)}:")
            print(str(e))
    
    print("✅ Successfully added all blocks to Notion page")
    return notion_url
