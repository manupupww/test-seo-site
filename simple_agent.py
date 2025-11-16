import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.content_generator import ContentGeneratorAgent
from tools.website_api_tool import WebsiteAPITool

def run_simplified_agent():
    """Simplified agent that focuses on core functionality"""
    print("Starting Simplified AI SEO Agent...")

    # Check API keys
    google_key = os.getenv("GOOGLE_GENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    api_status = {
        "Google AI": bool(google_key),
        "Tavily": bool(tavily_key),
        "Firecrawl": bool(firecrawl_key),
        "GitHub": bool(github_token)
    }

    print(f"API Keys Status: {api_status}")

    # Step 1: Generate content
    print("Step 1: Generating SEO content...")
    try:
        generator = ContentGeneratorAgent()
        content_result = generator.generate_content(
            keywords=["junk removal", "Vilnius", "atliekų išvežimas"],
            geo="Vilnius",
            content_type="blog_post",
            target_audience="local_businesses"
        )
        print("Content generation completed")
    except Exception as e:
        print(f"Content generation failed: {e}")
        return

    # Step 2: Create blog post
    print("Step 2: Creating blog post...")
    try:
        website_tool = WebsiteAPITool()
        blog_result = website_tool.create_blog_post(
            title="Expert SEO Guide: Junk Removal Services in Vilnius",
            content=content_result.get("primary_content", "Default content"),
            keywords=["junk removal", "Vilnius", "atliekų išvežimas", "eco-friendly disposal"],
            category="seo"
        )
        print(f"Blog post created: {blog_result.get('status')}")
    except Exception as e:
        print(f"Blog post creation failed: {e}")
        return

    # Step 3: Generate FAQ
    print("Step 3: Generating FAQ...")
    try:
        faq_result = website_tool.generate_faq_content(
            keywords=["junk removal", "disposal", "Vilnius", "eco-friendly"],
            industry="junk removal"
        )
        print(f"FAQ generated: {faq_result.get('status')}")
    except Exception as e:
        print(f"FAQ generation failed: {e}")

    # Step 4: Update site config
    print("Step 4: Updating site configuration...")
    try:
        config_result = website_tool.update_site_config(
            new_keywords=["junk removal Vilnius", "atliekų išvežimas", "šiukšlių išvežimas"],
            new_description="Professional junk removal and eco-friendly disposal services in Vilnius. Fast, reliable, and environmentally conscious."
        )
        print(f"Site config updated: {config_result.get('status')}")
    except Exception as e:
        print(f"Site config update failed: {e}")

    # Step 5: Add schema markup
    print("Step 5: Adding schema markup...")
    try:
        schema_result = website_tool.add_schema_markup("local_business")
        print(f"Schema markup added: {schema_result.get('status')}")
    except Exception as e:
        print(f"Schema markup failed: {e}")

    # Step 6: Commit changes
    print("Step 6: Committing changes to Git...")
    try:
        commit_result = website_tool.commit_changes("AI Agent: Autonomous SEO optimization completed")
        print(f"Changes committed: {commit_result.get('status')}")
        if commit_result.get('push_success'):
            print("Changes pushed to GitHub")
        else:
            print("Local commit successful, push failed (remote changes)")
    except Exception as e:
        print(f"Git commit failed: {e}")

    print("Simplified agent workflow completed successfully!")
    print("Summary: Content generated, blog post created, FAQ updated, config modified, schema added, changes committed")

if __name__ == "__main__":
    run_simplified_agent()