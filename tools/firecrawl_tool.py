from firecrawl import FirecrawlApp

class FirecrawlTool:
    def __init__(self, api_key):
        self.app = FirecrawlApp(api_key=api_key)

    def scrape_site(self, url):
        try:
            result = self.app.scrape_url(url, params={'formats': ['markdown']})
            return result.get('data', {}).get('markdown', 'No content scraped')
        except Exception as e:
            return f"Scraping failed: {str(e)}"