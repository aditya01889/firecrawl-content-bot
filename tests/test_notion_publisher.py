import pytest
from notion_publisher import parse_markdown_to_rich_text, split_content_to_blocks

def test_parse_markdown_to_rich_text():
    # Test inline code
    result = parse_markdown_to_rich_text("This is `code` text")
    assert len(result) == 3
    assert result[0]["type"] == "text"
    assert result[0]["text"]["content"] == "This is "
    assert result[1]["annotations"]["code"] is True
    assert result[1]["text"]["content"] == "code"
    assert result[2]["text"]["content"] == " text"

def test_parse_markdown_to_rich_text_with_code_blocks():
    # Should ignore code block markers since they're handled by split_content_to_blocks
    result = parse_markdown_to_rich_text("```python\nprint('hello')\n```")
    assert len(result) == 1
    assert result[0]["type"] == "text"
    assert "```" not in result[0]["text"]["content"]

def test_split_content_to_blocks_with_code():
    # Test with a Python code block
    content = """# Code Example

Here's some Python code:

```python
def hello():
    print("Hello, world!")
```

And here's some text after."""
    
    blocks = split_content_to_blocks(content)
    assert len(blocks) == 3
    assert blocks[0]["type"] == "heading_1"
    assert blocks[1]["type"] == "paragraph"
    assert blocks[2]["type"] == "code"
    assert blocks[2]["code"]["language"] == "python"
    assert "print" in blocks[2]["code"]["rich_text"][0]["text"]["content"]

def test_split_content_to_blocks_with_inline_code():
    # Test with inline code in a paragraph
    content = "Use `print()` to output text"
    blocks = split_content_to_blocks(content)
    assert len(blocks) == 1
    assert blocks[0]["type"] == "paragraph"
    rich_text = blocks[0]["paragraph"]["rich_text"]
    assert len(rich_text) == 3
    assert rich_text[0]["text"]["content"] == "Use "
    assert rich_text[1]["annotations"]["code"] is True
    assert rich_text[1]["text"]["content"] == "print()"
    assert rich_text[2]["text"]["content"] == " to output text"

if __name__ == "__main__":
    pytest.main(["-v"])
