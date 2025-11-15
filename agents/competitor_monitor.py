from tools.competitor_tool import CompetitorTool

class CompetitorMonitorAgent:
    def __init__(self, firecrawl_key, tavily_key, competitors):
        self.tool = CompetitorTool(firecrawl_key, tavily_key)
        self.competitors = competitors  # List of URLs

    def monitor_all(self):
        insights = []
        for url in self.competitors:
            try:
                data = self.tool.monitor_competitor(url, "junk removal SEO Vilnius")
                insights.append(data)
            except Exception as e:
                insights.append(f"Error monitoring {url}: {str(e)}")
        return insights