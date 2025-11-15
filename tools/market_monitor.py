import requests
import os

class MarketMonitorTool:
    def __init__(self, tavily_key):
        self.tavily = tavily_key

    def monitor_market(self, industry="junk removal", location="Vilnius"):
        # Use Tavily for market trends and news
        query = f"{industry} trends {location} 2025"
        try:
            # Simulate API call (Tavily search)
            # In real: results = tavily.search(query, search_depth="advanced")
            # For now, mock with real-like data
            trends = {
                "keywords": ["eco-friendly junk removal", "sustainable waste", "local disposal services"],
                "news": "New regulations on waste disposal in Vilnius.",
                "competitor_moves": "Competitors adopting green practices."
            }
            return trends
        except Exception as e:
            return {"error": str(e)}

# Usage: tool = MarketMonitorTool("key"); data = tool.monitor_market()