import os
import requests
import time
from dotenv import load_dotenv
from config import FIRECRAWL_API_KEY

load_dotenv()

def track_post_performance(topic: str, url: str):
    print(f"📊 Fetching real analytics for: {topic}")

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    crawl_response = requests.post(
        "https://api.firecrawl.dev/v1/crawl",
        headers=headers,
        json={"url": url}
    )

    if crawl_response.status_code != 200:
        print("❌ Failed to trigger crawl on Firecrawl")
        return None, None

    crawl_data = crawl_response.json()
    crawl_id = crawl_data.get("id")

    if not crawl_id:
        print("❌ No crawl ID returned")
        return None, None

    print(f"🪄 Crawl triggered: {crawl_id} (waiting 5s)")
    time.sleep(5)

    insights_response = requests.get(
        f"https://api.firecrawl.dev/v1/insights/{crawl_id}",
        headers=headers
    )

    if insights_response.status_code != 200:
        print("❌ Failed to fetch insights")
        return None, None

    insights = insights_response.json()
    keywords = insights.get("seo_keywords", [])
    word_count = insights.get("word_count", 0)

    print(f"✅ Keywords: {keywords}")
    print(f"📜 Word Count: {word_count}")

    return len(keywords), word_count

def refine_based_on_feedback(topic: str, url: str, content: str):
    print(f"🔁 Evaluating refinement potential based on Firecrawl insights...")
    # In real version, this could re-edit the blog if keywords are low
    print("📌 No changes applied — full refinement pipeline to come.")
