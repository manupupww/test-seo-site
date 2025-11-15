from firecrawl import FirecrawlApp
from tavily import TavilyClient

class CompetitorTool:
    def __init__(self, firecrawl_key, tavily_key):
        self.firecrawl = FirecrawlApp(api_key=firecrawl_key)
        self.tavily = TavilyClient(api_key=tavily_key)

    def monitor_competitor(self, competitor_url, query):
        # Scrape competitor site
        try:
            scraped = self.firecrawl.scrape_url(competitor_url, params={'formats': ['markdown']})
            content = scraped.get('markdown', 'No content')
        except:
            content = 'Scraping failed'

        # Analyze SERP for competitor
        serp = self.tavily.search(query, search_depth="advanced")
        rank = 1 if any(competitor_url in r['url'] for r in serp.get('results', [])) else 10

        # Simple insights
        insights = f"Content length: {len(content)}, Rank: {rank}"

        return {"content": content, "rank": rank, "insights": insights}

# Usage: tool = CompetitorTool(firecrawl_key, tavily_key); data = tool.monitor_competitor("competitor.com", "coffee SEO")