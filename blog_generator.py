import os
import json
import requests
import logging
from typing import Dict, Any
from prompt_template import blog_prompt
from utils import sanitize_filename, save_markdown
from config import OPENROUTER_API_KEY, BASE_URL, MODEL_NAME

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug: Print the API key and base URL
if not OPENROUTER_API_KEY:
    logger.error("ERROR: No API Key found in environment variables!")
else:
    logger.info(f"Using API Key: {OPENROUTER_API_KEY[:10]}...")
    logger.info(f"Using Base URL: {BASE_URL}")
    logger.info(f"Using Model: {MODEL_NAME}")
    
    # Verify the API key format
    if not OPENROUTER_API_KEY.startswith('sk-or-v1-'):
        logger.warning("WARNING: The API key format doesn't match the expected OpenRouter format.")

def generate_blog(topic: str) -> str:
    try:
        # Create a prompt with the topic
        prompt = blog_prompt.format(topic=topic)
        
        # Log the request details
        logger.info(f"Sending request to {BASE_URL}/chat/completions")
        
        # Prepare the request payload first
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that writes blog posts."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        # Prepare the request headers
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-github-username/firecrawl-content-bot",
            "X-Title": "Firecrawl Content Bot"
        }
        
        # Log headers and payload (without the actual API key for security)
        safe_headers = headers.copy()
        safe_headers['Authorization'] = f"Bearer {OPENROUTER_API_KEY[:10]}..."
        logger.debug(f"Request headers: {safe_headers}")
        logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        
        # Make the API request
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        # Check for errors
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        
        # Extract the content
        content = response_data['choices'][0]['message']['content'].strip()
        
        if not content:
            raise ValueError("Received empty response from the API")
        
        # Save and return the content
        filename = sanitize_filename(topic) + ".md"
        save_markdown(filename, content)
        return content
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.text
                error_msg += f"\nStatus Code: {e.response.status_code}"
                error_msg += f"\nResponse: {error_details}"
                logger.error(f"API request failed: {error_msg}")
                
                # Log response headers for debugging
                if e.response.headers:
                    logger.error("Response headers:")
                    for k, v in e.response.headers.items():
                        logger.error(f"  {k}: {v}")
            except Exception as parse_error:
                logger.error(f"Failed to parse error response: {parse_error}")
        else:
            logger.error(f"API request failed: {error_msg}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating blog: {str(e)}", exc_info=True)
        raise