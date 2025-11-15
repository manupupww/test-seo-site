from tavily import TavilyClient

class GeoSearchTool:
    def __init__(self, api_key):
        self.client = TavilyClient(api_key=api_key)

    def search_rank(self, query, location):
        results = self.client.search(
            query=query,
            search_depth="advanced",
            include_locations=True,
            location=location
        )
        # Extract rank
        for i, result in enumerate(results['results']):
            if 'target_site' in result['url']:  # Replace with actual site
                return i + 1
        return 10  # Default low rank