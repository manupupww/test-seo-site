#!/usr/bin/env python3
"""
Simple test script to demonstrate the SEO agent framework
"""
import os
import sys
sys.path.append('.')

# Mock environment variables for testing
os.environ['GOOGLE_GENAI_API_KEY'] = 'mock_key'
os.environ['TAVILY_API_KEY'] = 'mock_key'
os.environ['FIRECRAWL_API_KEY'] = 'mock_key'
os.environ['GITHUB_TOKEN'] = 'mock_token'

try:
    from agents.orchestrator import OrchestratorAgent
    print("SUCCESS: OrchestratorAgent imported successfully")

    # Test initialization
    orchestrator = OrchestratorAgent(
        competitor_keys={
            "firecrawl_key": "mock_key",
            "tavily_key": "mock_key",
            "competitors": ["https://example-competitor.com"]
        },
        website_api_config={
            "api_url": "https://api.github.com/repos/manupupww/test-seo-site/contents",
            "api_key": "mock_token"
        }
    )
    print("SUCCESS: OrchestratorAgent initialized successfully")

    # Test workflow (this will use mock responses)
    print("Running SEO optimization workflow...")
    result = orchestrator.run_workflow()
    print(f"SUCCESS: Workflow completed: {result}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()