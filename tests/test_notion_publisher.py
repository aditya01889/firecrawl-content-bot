import pytest
from notion_publisher import parse_markdown_to_rich_text, split_content_to_blocks

def test_parse_markdown_to_rich_text():
    # Test inline code
    result = parse_markdown_to_rich_text("This is `code` text")
    assert len(result) == 3
    assert result[0]["type"] == "text"
    assert result[1]["annotations"]["code"] is True
    assert result[1]["text"]["content"] == "code"

def test_split_content_to_blocks():
    # Test code block
    content = """# Heading
    
    This is a paragraph
    
    ```python
    def test():
        pass
    ```
    
    Another paragraph"""
    
    blocks = split_content_to_blocks(content)
    assert len(blocks) == 3
    assert blocks[0]["type"] == "heading_1"
    assert blocks[1]["type"] == "paragraph"
    assert blocks[2]["type"] == "code"

if __name__ == "__main__":
    pytest.main(["-v"])
