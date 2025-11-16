import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== API Keys Validation ===")

# Check Google AI
google_key = os.getenv("GOOGLE_GENAI_API_KEY")
print(f"Google AI Key: {'Set' if google_key else 'Not set'}")
if google_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=google_key)
        # Use a known working model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        print("Google AI: Working")
    except Exception as e:
        print(f"Google AI: Failed - {str(e)[:100]}")

# Check Tavily
tavily_key = os.getenv("TAVILY_API_KEY")
print(f"Tavily Key: {'Set' if tavily_key else 'Not set'}")
if tavily_key:
    try:
        from tavily import TavilyClient
        tavily = TavilyClient(api_key=tavily_key)
        result = tavily.search("test query", max_results=1)
        print("Tavily: Working")
    except Exception as e:
        print(f"Tavily: Failed - {str(e)[:100]}")

# Check Firecrawl
firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
print(f"Firecrawl Key: {'Set' if firecrawl_key else 'Not set'}")
if firecrawl_key:
    try:
        from firecrawl import FirecrawlApp
        app = FirecrawlApp(api_key=firecrawl_key)
        # Try different method signatures
        if hasattr(app, 'scrape_url'):
            result = app.scrape_url("https://example.com")
            print("Firecrawl: Working")
        elif hasattr(app, 'scrape'):
            result = app.scrape("https://example.com")
            print("Firecrawl: Working")
        else:
            print("Firecrawl: Method not found")
    except Exception as e:
        print(f"Firecrawl: Failed - {str(e)[:100]}")

# Check GitHub
github_token = os.getenv("GITHUB_TOKEN")
print(f"GitHub Token: {'Set' if github_token else 'Not set'}")
if github_token:
    try:
        import requests
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        if response.status_code == 200:
            print("GitHub: Working")
        else:
            print(f"GitHub: Failed - Status {response.status_code}")
    except Exception as e:
        print(f"GitHub: Failed - {str(e)[:100]}")

# Check GA4
ga4_property = os.getenv("GA4_PROPERTY_ID")
google_token = os.getenv("GOOGLE_ACCESS_TOKEN")
print(f"GA4 Property ID: {ga4_property or 'Not set'}")
print(f"GA4 Access Token: {'Set' if google_token else 'Not set'}")
if ga4_property and ga4_property != "YOUR_GA4_PROPERTY_ID" and google_token:
    print("GA4: Potentially working (needs full test)")
else:
    print("GA4: Not configured (using mock data)")

print("=== Validation Complete ===")