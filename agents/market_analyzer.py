from tools.market_monitor import MarketMonitorTool

class MarketAnalyzerAgent:
    def __init__(self, tavily_key):
        self.tool = MarketMonitorTool(tavily_key)

    def analyze_market(self, industry="junk removal", location="Vilnius"):
        market_data = self.tool.monitor_market(industry, location)
        # Process for SEO insights
        insights = f"Market trends: {market_data.get('keywords', [])}. News: {market_data.get('news', 'None')}."
        return insights

# Usage: agent = MarketAnalyzerAgent("key"); insights = agent.analyze_market()