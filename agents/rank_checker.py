from tavily import TavilyClient

class RankCheckerAgent:
    def __init__(self, tavily_key):
        if tavily_key and not tavily_key.startswith("YOUR"):
            self.tavily = TavilyClient(api_key=tavily_key)
        else:
            self.tavily = None

    def check_rank(self, query="site:manupupww.github.io junk removal", location="Vilnius"):
        if not self.tavily:
            return 10  # Mock low rank
        # Use Tavily for geo search
        try:
            results = self.tavily.search(query=f"{query} {location}", search_depth="advanced", include_locations=True)
            # Parse rank (simplified)
            for i, result in enumerate(results.get('results', [])):
                if 'manupupww.github.io' in result['url']:
                    return i + 1
            return 10  # Default low rank
        except Exception as e:
            return 10  # Error, assume low rank

    def run_loop(self):
        while True:
            rank = self.check_rank()
            if rank >= 1:
                break
            # Trigger update
            return rank