# ui.py
import streamlit as st
from topic_ideator import get_trending_topics
from blog_generator import generate_blog
from seo_enhancer import enhance_seo
from style_validator import validate_style
from notion_publisher import publish_to_notion
from analytics_tracker import track_post_performance

st.set_page_config(page_title="Firecrawl Blog Agent", layout="wide")
st.title("🔥 Firecrawl Content Bot")

st.sidebar.header("Configuration")
num_blogs = st.sidebar.slider("Number of Blogs", 1, 5, 1)

if st.sidebar.button("🔍 Fetch Trending Topics"):
    topics = get_trending_topics()
    st.session_state.topics = topics[:num_blogs]
    st.success("Topics fetched!")

if "topics" in st.session_state:
    for topic in st.session_state.topics:
        st.subheader(f"📝 Topic: {topic}")
        if st.button(f"🧠 Generate Blog for '{topic}'"):
            content = generate_blog(topic)
            st.session_state[f"{topic}_content"] = content
            st.markdown(content)

        if f"{topic}_content" in st.session_state:
            content = st.session_state[f"{topic}_content"]

            if st.button(f"🔧 Enhance SEO for '{topic}'"):
                seo_content = enhance_seo(content)
                st.session_state[f"{topic}_seo"] = seo_content
                st.markdown(seo_content)

            if f"{topic}_seo" in st.session_state:
                seo_content = st.session_state[f"{topic}_seo"]
                if st.button(f"✅ Validate Style for '{topic}'"):
                    final_content = validate_style(seo_content)
                    st.session_state[f"{topic}_final"] = final_content
                    st.markdown(final_content)

            if f"{topic}_final" in st.session_state:
                final = st.session_state[f"{topic}_final"]
                if st.button(f"🚀 Publish '{topic}' to Notion"):
                    url = publish_to_notion(topic, final)
                    st.success(f"Published! [🔗 View Blog]({url})")
                    st.session_state[f"{topic}_url"] = url

                if f"{topic}_url" in st.session_state:
                    if st.button(f"📊 Check Analytics for '{topic}'"):
                        views, ctr = track_post_performance(topic, st.session_state[f"{topic}_url"])
                        st.info(f"Views: {views} | CTR: {ctr}%")
