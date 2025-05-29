# 🔥 Firecrawl Content Bot

An autonomous content creation pipeline that generates developer-focused blog posts, enhances them for SEO, and publishes to Notion with proper formatting.

## 🚀 Features

- **Topic Ideation**: Finds trending developer topics
- **Content Generation**: Creates high-quality technical blog posts
- **SEO Enhancement**: Optimizes content with relevant keywords and metadata
- **Style Validation**: Ensures consistent, developer-friendly formatting
- **Notion Publishing**: Seamlessly publishes to Notion with proper formatting
- **Performance Tracking**: Monitors post performance (views, engagement)

## 🧱 Project Structure

```
firecrawl-content-bot/
├── blog_generator.py     # Generates blog content using LLM
├── seo_enhancer.py       # Enhances content for SEO
├── style_validator.py    # Validates and fixes style
├── notion_publisher.py   # Publishes to Notion with formatting
├── analytics_tracker.py  # Tracks post performance
├── config.py            # Configuration and settings
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # This file
```

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/aditya01889/firecrawl-content-bot.git
   cd firecrawl-content-bot
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update with your API keys:
     ```
     OPENROUTER_API_KEY=your_openrouter_key
     FIRECRAWL_API_KEY=your_firecrawl_key
     NOTION_API_KEY=your_notion_api_key
     NOTION_DATABASE_ID=your_notion_database_id
     ```

5. **Run the application**
   ```bash
   streamlit run ui.py
   ```

## 🔧 Usage

1. Launch the Streamlit UI
2. Enter a topic or use the "Fetch Trending Topics" button
3. Click "Generate Blog" to create content
4. Use "Enhance SEO" to optimize the content
5. Click "Publish to Notion" to publish the final version
6. Check analytics with the "Check Analytics" button

## 🛡️ Security Note

- Never commit your `.env` file to version control
- The `.gitignore` is pre-configured to exclude sensitive files
- Rotate your API keys if they are accidentally exposed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

python blog_agent.py


🧠 How It Works
Topic Ideation:

Scrapes trending posts using requests + BeautifulSoup

Filters topics via keyword matching

Content Generation:

Uses LangChain + OpenRouter with GPT-3.5 Turbo

Converts topic into a long-form blog

SEO & Style:

Two-stage LLM flow: first improves SEO, then checks tone

Ensures markdown code formatting and dev readability

Publishing & Tracking:

Publishes to Notion via notion-publisher.py

Scrapes published URL with Firecrawl to log content stats

📦 To-Do / Roadmap
 Add prompt_template.py to modularize LLM prompts

 Add GitHub trend scraper for topic_ideator

 Add Notion auto-tagging by topic/category

 Add historical analytics dashboard (views, edits, comments)

 Add Discord/Slack webhook for publishing notifications

 Add refinement logic via Notion feedback/comments

🤝 Integrations
LLMs via OpenRouter: Efficient GPT-3.5 content generation

Firecrawl: Smart scraping & analytics for published blog posts

Notion API: Seamless publishing to your workspace

💡 Ideal For
Developer-focused startups who need content but don’t have bandwidth

Indie hackers launching tools and needing SEO traction

Technical marketers looking to scale blog creation

📄 License
MIT — free to use, modify, and adapt for your own autonomous content workflows.

