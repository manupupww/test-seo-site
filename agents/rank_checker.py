from tavily import TavilyClient

class RankCheckerAgent:
    def __init__(self, tavily_key):
        self.tavily = TavilyClient(api_key=tavily_key)

    def check_rank(self, query="site:manupupww.github.io junk removal", location="Vilnius"):
        # Use Tavily for geo search
        results = self.tavily.search(query=f"{query} {location}", search_depth="advanced", include_locations=True)
        # Parse rank (simplified)
        for i, result in enumerate(results.get('results', [])):
            if 'manupupww.github.io' in result['url']:
                return i + 1
        return 10  # Default low rank

    def run_loop(self):
        while True:
            rank = self.check_rank()
            if rank >= 1:
                break
            # Trigger update
            return rank