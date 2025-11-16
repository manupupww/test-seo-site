from tools.geo_search import GeoSearchTool

class GeoAgent:
    def __init__(self, tavily_key):
        self.tool = GeoSearchTool(tavily_key)

    def optimize_for_location(self, location="Vilnius", industry="junk removal"):
        """Complete geo-optimization workflow"""
        try:
            # Get local keywords
            keywords = self.tool.get_local_keywords(location, industry)
            print(f"Local Keywords: {keywords}")

            # Analyze local competition
            competition = self.tool.analyze_local_competition(location, industry)
            print(f"Local Competition: {competition}")

            # Generate geo content ideas
            content_ideas = self.tool.generate_geo_content_ideas(location, industry)
            print(f"Content Ideas: {content_ideas}")

            return {
                "keywords": keywords,
                "competition": competition,
                "content_ideas": content_ideas,
                "location": location,
                "industry": industry,
                "status": "Geo optimization data collected successfully"
            }
        except Exception as e:
            print(f"Geo optimization failed: {str(e)}")
            return {"error": str(e)}

# Usage: agent = GeoAgent("key"); result = agent.optimize_for_location()