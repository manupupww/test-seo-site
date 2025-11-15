from firecrawl import FirecrawlApp

class FirecrawlTool:
    def __init__(self, api_key):
        self.app = FirecrawlApp(api_key=api_key)

    def scrape_site(self, url):
        result = self.app.scrape_url(url, params={'formats': ['markdown']})
        return result['markdown']