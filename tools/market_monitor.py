import requests
import os
from tavily import TavilyClient

class MarketMonitorTool:
    def __init__(self, tavily_key):
        if tavily_key and not tavily_key.startswith("YOUR"):
            self.tavily = TavilyClient(api_key=tavily_key)
        else:
            self.tavily = None

    def monitor_market(self, industry="junk removal", location="Vilnius"):
        if self.tavily:
            try:
                query = f"{industry} trends {location} 2025"
                results = self.tavily.search(query, search_depth="advanced")
                # Extract trends
                trends = {
                    "keywords": [r.get('title', '') for r in results.get('results', [])[:3]],
                    "news": results.get('results', [{}])[0].get('content', 'No news'),
                    "competitor_moves": "Based on search results"
                }
                return trends
            except Exception as e:
                return {"error": str(e)}
        else:
            # Mock data
            trends = {
                "keywords": ["eco-friendly junk removal", "sustainable waste", "local disposal services"],
                "news": "New regulations on waste disposal in Vilnius.",
                "competitor_moves": "Competitors adopting green practices."
            }
            return trends

# Usage: tool = MarketMonitorTool("key"); data = tool.monitor_market()