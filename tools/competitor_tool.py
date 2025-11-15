from firecrawl import FirecrawlApp
from tavily import TavilyClient

class CompetitorTool:
    def __init__(self, firecrawl_key, tavily_key):
        if firecrawl_key and not firecrawl_key.startswith("YOUR"):
            self.firecrawl = FirecrawlApp(api_key=firecrawl_key)
        else:
            self.firecrawl = None
        if tavily_key and not tavily_key.startswith("YOUR"):
            self.tavily = TavilyClient(api_key=tavily_key)
        else:
            self.tavily = None

    def monitor_competitor(self, competitor_url, query):
        # Scrape competitor site
        if self.firecrawl:
            try:
                scraped = self.firecrawl.scrape_url(competitor_url, params={'formats': ['markdown']})
                content = scraped.get('data', {}).get('markdown', 'No content')
            except:
                content = 'Scraping failed'
        else:
            content = 'Mock scraped content'

        # Analyze SERP for competitor
        if self.tavily:
            try:
                serp = self.tavily.search(query, search_depth="advanced")
                rank = 1 if any(competitor_url in r['url'] for r in serp.get('results', [])) else 10
            except:
                rank = 10
        else:
            rank = 10

        # Simple insights
        insights = f"Content length: {len(content)}, Rank: {rank}"

        return {"content": content, "rank": rank, "insights": insights}

# Usage: tool = CompetitorTool(firecrawl_key, tavily_key); data = tool.monitor_competitor("competitor.com", "coffee SEO")