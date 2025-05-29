from topic_ideator import get_trending_topics
from blog_generator import generate_blog
from seo_enhancer import enhance_seo
from style_validator import validate_style
from notion_publisher import publish_to_notion
from analytics_tracker import track_post_performance, refine_based_on_feedback
from utils import log_error, save_markdown

N = 3  # Number of blogs per run

def main():
    topics = get_trending_topics()
    for i, topic in enumerate(topics[:N], 1):
        print(f"[{i}/{N}] Generating blog for: {topic}")
        try:
            content = generate_blog(topic)
            enhanced = enhance_seo(content)
            final_content = validate_style(enhanced)
            if final_content:
                save_markdown(topic, final_content)
                url = publish_to_notion(topic, final_content)
                print("✅ Published to Notion")
                track_post_performance(topic, url)
                refine_based_on_feedback(topic, url, final_content)
                print("📈 Analytics + Refinement complete")
        except Exception as e:
            print(f"❌ Error: {e}")
            log_error(topic, e)

if __name__ == "__main__":
    main()