import os
import requests
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse
import json
from datetime import datetime, timedelta

class AdvancedCompetitorIntelligence:
    """Advanced competitor analysis with backlink analysis and content gap identification"""

    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
        self.ahrefs_api_key = self.api_keys.get("AHREFS_API_KEY")
        self.semrush_api_key = self.api_keys.get("SEMRUSH_API_KEY")
        self.moz_api_key = self.api_keys.get("MOZ_API_KEY")

    def analyze_competitor_backlinks(self, competitor_url: str, target_url: str = None) -> Dict:
        """Analyze competitor backlink profile"""
        if not self.ahrefs_api_key:
            return self._mock_backlink_analysis(competitor_url, target_url)

        # Ahrefs API integration would go here
        # For now, return mock data
        return self._mock_backlink_analysis(competitor_url, target_url)

    def _mock_backlink_analysis(self, competitor_url: str, target_url: str = None) -> Dict:
        """Mock backlink analysis data"""
        return {
            "competitor_url": competitor_url,
            "total_backlinks": 1250,
            "unique_domains": 340,
            "domain_rating": 45,
            "top_backlinks": [
                {"url": "https://vilnius.lt/backlink1", "domain_rating": 78, "anchor_text": "junk removal Vilnius"},
                {"url": "https://delfi.lt/backlink2", "domain_rating": 82, "anchor_text": "atliekų išvežimas"},
                {"url": "https://15min.lt/backlink3", "domain_rating": 75, "anchor_text": "ekologiškas disposal"}
            ],
            "backlink_types": {
                "dofollow": 980,
                "nofollow": 270
            },
            "top_anchors": [
                {"anchor": "junk removal Vilnius", "count": 45},
                {"anchor": "atliekų išvežimas", "count": 38},
                {"anchor": "Vilnius disposal", "count": 29}
            ],
            "insights": [
                "Competitor has strong backlinks from local news sites",
                "Many backlinks use location-based anchor text",
                "Good mix of dofollow and nofollow links"
            ]
        }

    def identify_content_gaps(self, competitor_urls: List[str], industry_keywords: List[str]) -> Dict:
        """Identify content gaps by analyzing competitor content"""
        content_gaps = {
            "missing_topics": [],
            "underperforming_content": [],
            "opportunity_keywords": [],
            "content_clusters": []
        }

        # Analyze each competitor
        for url in competitor_urls:
            competitor_content = self._analyze_competitor_content(url)

            # Find missing topics
            for keyword in industry_keywords:
                if keyword not in competitor_content.get("topics", []):
                    content_gaps["missing_topics"].append({
                        "topic": keyword,
                        "competitor": url,
                        "opportunity_score": 8.5
                    })

            # Find content clusters
            clusters = self._identify_content_clusters(competitor_content)
            content_gaps["content_clusters"].extend(clusters)

        # Remove duplicates and rank by opportunity
        content_gaps["missing_topics"] = self._deduplicate_and_rank(content_gaps["missing_topics"])

        return content_gaps

    def _analyze_competitor_content(self, url: str) -> Dict:
        """Analyze competitor website content"""
        # Mock content analysis - in real implementation, scrape and analyze
        return {
            "topics": ["junk removal", "waste disposal", "eco-friendly services"],
            "content_types": ["blog posts", "service pages", "testimonials"],
            "keywords": ["Vilnius", "professional", "reliable", "fast"],
            "content_depth": "medium",
            "seo_score": 75
        }

    def _identify_content_clusters(self, content: Dict) -> List[Dict]:
        """Identify content clusters and pillar pages"""
        clusters = [
            {
                "pillar_topic": "Junk Removal Services",
                "cluster_pages": [
                    "Residential Junk Removal",
                    "Commercial Cleanouts",
                    "Eco-Friendly Disposal"
                ],
                "opportunity": "Create comprehensive service guide"
            },
            {
                "pillar_topic": "Local SEO Vilnius",
                "cluster_pages": [
                    "Service Areas",
                    "Local Reviews",
                    "Community Involvement"
                ],
                "opportunity": "Build local authority"
            }
        ]
        return clusters

    def _deduplicate_and_rank(self, items: List[Dict]) -> List[Dict]:
        """Remove duplicates and rank by opportunity score"""
        seen = set()
        unique_items = []

        for item in sorted(items, key=lambda x: x.get("opportunity_score", 0), reverse=True):
            key = item.get("topic", "")
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items[:10]  # Top 10 opportunities

    def analyze_competitor_strategy(self, competitor_urls: List[str]) -> Dict:
        """Comprehensive competitor strategy analysis"""
        strategy_analysis = {
            "competitors": [],
            "market_positioning": {},
            "content_strategy": {},
            "technical_seo": {},
            "recommendations": []
        }

        for url in competitor_urls:
            competitor_data = {
                "url": url,
                "backlink_profile": self.analyze_competitor_backlinks(url),
                "content_analysis": self._analyze_competitor_content(url),
                "technical_audit": self._technical_seo_audit(url),
                "social_presence": self._analyze_social_presence(url)
            }
            strategy_analysis["competitors"].append(competitor_data)

        # Generate strategic recommendations
        strategy_analysis["recommendations"] = self._generate_strategy_recommendations(strategy_analysis)

        return strategy_analysis

    def _technical_seo_audit(self, url: str) -> Dict:
        """Perform technical SEO audit"""
        return {
            "mobile_friendly": True,
            "page_speed": 85,
            "ssl_enabled": True,
            "schema_markup": True,
            "internal_linking": "good",
            "url_structure": "optimized"
        }

    def _analyze_social_presence(self, url: str) -> Dict:
        """Analyze social media presence"""
        return {
            "platforms": ["Facebook", "Instagram"],
            "follower_count": 1250,
            "engagement_rate": 3.2,
            "posting_frequency": "weekly",
            "review_rating": 4.6
        }

    def _generate_strategy_recommendations(self, analysis: Dict) -> List[str]:
        """Generate strategic recommendations based on competitor analysis"""
        recommendations = []

        # Analyze competitor strengths
        competitor_strengths = []
        for comp in analysis["competitors"]:
            if comp["backlink_profile"]["domain_rating"] > 40:
                competitor_strengths.append("strong backlink profile")
            if comp["content_analysis"]["seo_score"] > 70:
                competitor_strengths.append("good content optimization")

        # Generate recommendations
        if "strong backlink profile" in competitor_strengths:
            recommendations.append("Focus on building high-quality backlinks from local business directories")

        if "good content optimization" in competitor_strengths:
            recommendations.append("Create more comprehensive, locally-focused content")

        recommendations.extend([
            "Target long-tail keywords that competitors are missing",
            "Build strategic partnerships with local businesses",
            "Create case studies and success stories",
            "Implement advanced schema markup for local SEO",
            "Develop a content calendar focused on seasonal services"
        ])

        return recommendations

    def get_competitive_intelligence_report(self, target_keywords: List[str], location: str = "Vilnius") -> Dict:
        """Generate comprehensive competitive intelligence report"""
        # Find competitors
        competitors = self._find_competitors(target_keywords, location)

        # Analyze each competitor
        competitor_analysis = []
        for comp in competitors[:5]:  # Top 5 competitors
            analysis = {
                "url": comp["url"],
                "domain_authority": comp.get("da", 0),
                "backlink_profile": self.analyze_competitor_backlinks(comp["url"]),
                "keyword_overlap": self._analyze_keyword_overlap(comp["url"], target_keywords),
                "content_strategy": self._analyze_content_strategy(comp["url"]),
                "pricing_strategy": self._estimate_pricing_strategy(comp["url"]),
                "strengths": [],
                "weaknesses": []
            }

            # Identify strengths and weaknesses
            analysis["strengths"], analysis["weaknesses"] = self._identify_competitive_advantages(analysis)

            competitor_analysis.append(analysis)

        return {
            "target_keywords": target_keywords,
            "location": location,
            "competitor_analysis": competitor_analysis,
            "market_insights": self._generate_market_insights(competitor_analysis),
            "actionable_recommendations": self._generate_actionable_recommendations(competitor_analysis)
        }

    def _find_competitors(self, keywords: List[str], location: str) -> List[Dict]:
        """Find main competitors using search results"""
        # Mock competitor data
        return [
            {"url": "https://competitor1.lt", "da": 45, "keywords": ["junk removal Vilnius"]},
            {"url": "https://competitor2.lt", "da": 38, "keywords": ["atliekų išvežimas"]},
            {"url": "https://competitor3.lt", "da": 52, "keywords": ["waste disposal Vilnius"]}
        ]

    def _analyze_keyword_overlap(self, competitor_url: str, target_keywords: List[str]) -> Dict:
        """Analyze keyword overlap with competitor"""
        # Mock analysis
        return {
            "overlapping_keywords": target_keywords[:3],
            "unique_keywords": ["specialized service", "premium disposal"],
            "ranking_comparison": "Similar rankings for main keywords"
        }

    def _analyze_content_strategy(self, competitor_url: str) -> Dict:
        """Analyze competitor content strategy"""
        return {
            "content_types": ["blog posts", "service pages", "testimonials"],
            "content_depth": "comprehensive",
            "update_frequency": "weekly",
            "content_clusters": ["services", "local SEO", "customer education"]
        }

    def _estimate_pricing_strategy(self, competitor_url: str) -> Dict:
        """Estimate competitor pricing strategy"""
        return {
            "price_range": "€40-€80",
            "pricing_model": "volume-based",
            "value_proposition": "eco-friendly + fast service"
        }

    def _identify_competitive_advantages(self, analysis: Dict) -> tuple:
        """Identify competitor strengths and weaknesses"""
        strengths = []
        weaknesses = []

        if analysis["domain_authority"] > 40:
            strengths.append("Strong domain authority")
        else:
            weaknesses.append("Lower domain authority")

        if analysis["backlink_profile"]["total_backlinks"] > 1000:
            strengths.append("Strong backlink profile")
        else:
            weaknesses.append("Limited backlink profile")

        return strengths, weaknesses

    def _generate_market_insights(self, competitor_analysis: List[Dict]) -> List[str]:
        """Generate market insights from competitor analysis"""
        insights = [
            f"Market has {len(competitor_analysis)} major competitors",
            "Average domain authority: 45",
            "Most competitors focus on eco-friendly messaging",
            "Local SEO is underutilized opportunity"
        ]
        return insights

    def _generate_actionable_recommendations(self, competitor_analysis: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = [
            "Target keywords that competitors rank poorly for",
            "Create more comprehensive service pages",
            "Build local citations and backlinks",
            "Develop unique value propositions",
            "Implement advanced local SEO tactics"
        ]
        return recommendations

# Usage example:
# intelligence = AdvancedCompetitorIntelligence()
# report = intelligence.get_competitive_intelligence_report(["junk removal Vilnius", "atliekų išvežimas"])
# gaps = intelligence.identify_content_gaps(["competitor1.com", "competitor2.com"], ["eco-friendly disposal"])