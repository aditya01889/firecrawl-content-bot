import requests
from bs4 import BeautifulSoup
import json
import re
import random
from collections import Counter

KEYWORDS = [
    "scraping", "data extraction", "automation", "firecrawl",
    "web crawl", "llm", "agent", "workflow", "dev tool"
]

def score_topic(text):
    words = re.findall(r'\w+', text.lower())
    keyword_count = sum(words.count(kw.lower()) for kw in KEYWORDS)
    return keyword_count

def matches_keywords(text):
    return score_topic(text) > 0

def clean_title(title):
    return re.sub(r"\s+", " ", title.strip())

def get_hn_trends():
    print("🔍 Fetching Hacker News...")
    try:
        response = requests.get("https://news.ycombinator.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        titles = [tag.get_text() for tag in soup.select(".titleline a")]
        return [clean_title(t) for t in titles if matches_keywords(t)]
    except Exception as e:
        print(f"⚠️ HN fetch error: {e}")
        return []

def get_reddit_trends():
    print("🔍 Fetching Reddit...")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get("https://www.reddit.com/r/webdev/.json", headers=headers)
        data = response.json()
        posts = data["data"]["children"]
        titles = [post["data"]["title"] for post in posts]
        return [clean_title(t) for t in titles if matches_keywords(t)]
    except Exception as e:
        print(f"⚠️ Reddit fetch error: {e}")
        return []

def get_devto_trends():
    print("🔍 Fetching Dev.to...")
    try:
        response = requests.get("https://dev.to/api/articles?tag=webscraping")
        articles = response.json()
        titles = [article["title"] for article in articles]
        return [clean_title(t) for t in titles if matches_keywords(t)]
    except Exception as e:
        print(f"⚠️ Dev.to fetch error: {e}")
        return []

def get_firecrawl_trends():
    print("🔍 Fetching Firecrawl trends...")
    try:
        response = requests.get("https://trending.firecrawl.dev/topics")
        if response.status_code == 200:
            topics = response.json().get("topics", [])
            return [clean_title(t) for t in topics if matches_keywords(t)]
    except Exception as e:
        print(f"⚠️ Firecrawl fetch error: {e}")
    return []

def get_trending_topics():
    all_topics = []
    all_topics.extend(get_firecrawl_trends())
    all_topics.extend(get_hn_trends())
    all_topics.extend(get_reddit_trends())
    all_topics.extend(get_devto_trends())

    scored_topics = [(topic, score_topic(topic)) for topic in set(all_topics)]
    sorted_topics = sorted(scored_topics, key=lambda x: x[1], reverse=True)
    top_topics = [t[0] for t in sorted_topics if t[1] > 0]

    return top_topics[:10]
