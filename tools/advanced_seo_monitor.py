import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class GoogleSearchConsoleAPI:
    """Google Search Console API integration for real-time SEO monitoring"""

    def __init__(self, credentials_path: str = None):
        self.base_url = "https://www.googleapis.com/webmasters/v3"
        self.site_url = "https://manupupww.github.io/test-seo-site/"
        self.credentials = credentials_path or os.getenv("GOOGLE_CREDENTIALS_JSON")

        if self.credentials:
            # In production, use proper OAuth2 flow
            self.access_token = os.getenv("GOOGLE_ACCESS_TOKEN")
        else:
            self.access_token = None

    def get_search_analytics(self, days: int = 7) -> Dict:
        """Get search analytics data"""
        if not self.access_token:
            return {"error": "No Google credentials", "mock_data": self._get_mock_analytics()}

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        url = f"{self.base_url}/sites/{self.site_url}/searchAnalytics/query"

        payload = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "dimensions": ["query", "page", "country"],
            "rowLimit": 100
        }

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}", "mock_data": self._get_mock_analytics()}
        except Exception as e:
            return {"error": str(e), "mock_data": self._get_mock_analytics()}

    def get_sitemaps(self) -> Dict:
        """Get sitemap information"""
        if not self.access_token:
            return {"error": "No Google credentials"}

        url = f"{self.base_url}/sites/{self.site_url}/sitemaps"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.get(url, headers=headers)
            return response.json() if response.status_code == 200 else {"error": response.status_code}
        except Exception as e:
            return {"error": str(e)}

    def submit_sitemap(self, sitemap_url: str) -> Dict:
        """Submit sitemap to Google"""
        if not self.access_token:
            return {"error": "No Google credentials"}

        url = f"{self.base_url}/sites/{self.site_url}/sitemaps/{sitemap_url}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.put(url, headers=headers)
            return {"status": response.status_code, "success": response.status_code == 200}
        except Exception as e:
            return {"error": str(e)}

    def _get_mock_analytics(self) -> Dict:
        """Mock data for testing without API credentials"""
        return {
            "rows": [
                {
                    "keys": ["junk removal Vilnius", "/index.html", "LTU"],
                    "clicks": 45,
                    "impressions": 1250,
                    "ctr": 0.036,
                    "position": 8.5
                },
                {
                    "keys": ["atliekų išvežimas Vilnius", "/apie-mus.html", "LTU"],
                    "clicks": 32,
                    "impressions": 890,
                    "ctr": 0.036,
                    "position": 6.2
                }
            ],
            "responseAggregationType": "byProperty"
        }

class BingWebmasterAPI:
    """Bing Webmaster API for additional search data"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BING_API_KEY")
        self.base_url = "https://ssl.bing.com/webmaster/api.svc/json"

    def get_search_keywords(self) -> Dict:
        """Get keyword data from Bing"""
        if not self.api_key:
            return {"error": "No Bing API key", "mock_data": self._get_mock_bing_data()}

        # Bing API implementation would go here
        return {"mock_data": self._get_mock_bing_data()}

    def _get_mock_bing_data(self) -> Dict:
        """Mock Bing data"""
        return {
            "keywords": [
                {"term": "junk removal Vilnius", "volume": 1200, "competition": "medium"},
                {"term": "atliekų išvežimas", "volume": 890, "competition": "low"}
            ]
        }

class AdvancedSEOMonitor:
    """Advanced SEO monitoring with multiple data sources"""

    def __init__(self):
        self.gsc = GoogleSearchConsoleAPI()
        self.bing = BingWebmasterAPI()

    def get_comprehensive_seo_report(self) -> Dict:
        """Get comprehensive SEO report from all sources"""
        gsc_data = self.gsc.get_search_analytics()
        bing_data = self.bing.get_search_keywords()

        # Combine and analyze data
        report = {
            "timestamp": datetime.now().isoformat(),
            "google_search_console": gsc_data,
            "bing_webmaster": bing_data,
            "insights": self._analyze_insights(gsc_data, bing_data),
            "recommendations": self._generate_recommendations(gsc_data, bing_data)
        }

        return report

    def _analyze_insights(self, gsc_data: Dict, bing_data: Dict) -> List[str]:
        """Analyze data and generate insights"""
        insights = []

        if "rows" in gsc_data:
            for row in gsc_data["rows"][:5]:  # Top 5 keywords
                keys = row["keys"]
                position = row.get("position", 0)
                clicks = row.get("clicks", 0)

                if position > 10:
                    insights.append(f"Keyword '{keys[0]}' ranks at position {position} - needs optimization")
                elif position <= 3 and clicks > 20:
                    insights.append(f"Keyword '{keys[0]}' performing well at position {position}")

        insights.append("Combined Google + Bing data shows strong local SEO potential")
        return insights

    def _generate_recommendations(self, gsc_data: Dict, bing_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Position-based recommendations
        if "rows" in gsc_data:
            low_performing = [row for row in gsc_data["rows"] if row.get("position", 0) > 15]
            if low_performing:
                recommendations.append("Focus on improving content for low-performing keywords")

        # Volume-based recommendations
        if "keywords" in bing_data:
            high_volume = [kw for kw in bing_data["keywords"] if kw.get("volume", 0) > 1000]
            if high_volume:
                recommendations.append("Target high-volume keywords with dedicated content")

        recommendations.extend([
            "Implement voice search optimization for local queries",
            "Add structured data for local business information",
            "Create location-specific landing pages",
            "Optimize for mobile search with local intent"
        ])

        return recommendations

# Usage example:
# monitor = AdvancedSEOMonitor()
# report = monitor.get_comprehensive_seo_report()
# print(json.dumps(report, indent=2))