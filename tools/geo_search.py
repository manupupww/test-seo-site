from tavily import TavilyClient

class GeoSearchTool:
    def __init__(self, api_key):
        self.client = TavilyClient(api_key=api_key) if api_key and not api_key.startswith("YOUR") else None

    def search_rank(self, query, location, target_url="manupupww.github.io"):
        if not self.client:
            return 5  # Mock rank

        results = self.client.search(
            query=query,
            search_depth="advanced",
            include_locations=True,
            location=location
        )
        # Extract rank
        for i, result in enumerate(results.get('results', [])):
            if target_url in result['url']:
                return i + 1
        return 10  # Default low rank

    def get_local_keywords(self, location="Vilnius", industry="junk removal"):
        """Get location-specific keywords for better local SEO"""
        if not self.client:
            return [f"{industry} {location}", f"{industry} services {location}", f"professional {industry} {location}"]

        query = f"{industry} keywords {location}"
        results = self.client.search(query=query, search_depth="advanced")

        keywords = []
        for result in results.get('results', [])[:5]:
            title = result.get('title', '').lower()
            # Extract potential keywords from titles
            words = title.split()
            for i in range(len(words)-1):
                if location.lower() in words[i:i+2]:
                    keywords.append(' '.join(words[i:i+2]))

        # Add standard local keywords
        base_keywords = [
            f"{industry} {location}",
            f"{industry} services {location}",
            f"professional {industry} {location}",
            f"affordable {industry} {location}",
            f"eco-friendly {industry} {location}",
            f"emergency {industry} {location}",
            f"{industry} company {location}",
            f"best {industry} {location}",
            f"{industry} near me {location}",
            f"local {industry} {location}"
        ]
        keywords.extend(base_keywords)

        return list(set(keywords))[:10]  # Return unique top 10

    def analyze_local_competition(self, location="Vilnius", industry="junk removal"):
        """Analyze local competitors for geo-specific insights"""
        if not self.client:
            return {"competitors": ["Local Competitor 1", "Local Competitor 2"], "insights": "Mock local competition analysis"}

        query = f"{industry} {location} companies"
        results = self.client.search(query=query, search_depth="advanced")

        competitors = []
        for result in results.get('results', [])[:5]:
            competitors.append({
                "name": result.get('title', '').split(' - ')[0],
                "url": result['url'],
                "snippet": result.get('content', '')[:100]
            })

        return {
            "competitors": competitors,
            "insights": f"Found {len(competitors)} local competitors in {location} for {industry}",
            "recommendations": [
                "Target long-tail keywords with location",
                "Get listed on local directories",
                "Collect local reviews and testimonials",
                "Partner with local businesses"
            ]
        }

    def generate_geo_content_ideas(self, location="Vilnius", industry="junk removal"):
        """Generate content ideas optimized for local SEO"""
        content_ideas = [
            f"Why Choose Local {industry.title()} Services in {location}",
            f"The Benefits of Eco-Friendly {industry.title()} in {location}",
            f"Emergency {industry.title()} Services Available 24/7 in {location}",
            f"How Much Does {industry.title()} Cost in {location}?",
            f"Professional {industry.title()} Companies in {location} - Reviews & Ratings",
            f"{location} {industry.title()} Regulations and Best Practices",
            f"Before and After: {industry.title()} Projects in {location}",
            f"Customer Testimonials: {industry.title()} Services in {location}",
            f"The Ultimate Guide to {industry.title()} in {location}",
            f"Why {location} Residents Choose Our {industry.title()} Services"
        ]

        return content_ideas

# Usage: tool = GeoSearchTool("key"); keywords = tool.get_local_keywords(); competition = tool.analyze_local_competition()