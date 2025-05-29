from langchain.prompts import PromptTemplate

blog_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    Write a detailed, SEO-optimized blog post on the topic: "{topic}".
    Make it developer-focused, with examples using Firecrawl.
    Include:
    - Introduction
    - Problem Statement
    - How Firecrawl helps
    - Code Examples
    - Conclusion
    - Meta Description (at end)
    """
)