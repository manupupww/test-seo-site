import requests
import base64
import os
from firecrawl import FirecrawlApp

class SEOOptimizerTool:
    def __init__(self, firecrawl_key, github_token, repo_owner="manupupww", repo_name="test-seo-site"):
        self.firecrawl = FirecrawlApp(api_key=firecrawl_key) if firecrawl_key else None
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}

    def analyze_site_seo(self, site_url="https://manupupww.github.io/test-seo-site/"):
        """Analyze current site SEO status"""
        if not self.firecrawl:
            return {"error": "Firecrawl key missing"}

        try:
            # Scrape homepage
            result = self.firecrawl.scrape_url(site_url, params={'formats': ['markdown', 'html']})
            html = result.get('data', {}).get('html', '')
            markdown = result.get('data', {}).get('markdown', '')

            # Basic SEO analysis
            analysis = {
                "title": self._extract_title(html),
                "meta_description": self._extract_meta_description(html),
                "h1_tags": self._extract_h1s(html),
                "word_count": len(markdown.split()),
                "has_schema": "schema.org" in html,
                "mobile_friendly": "viewport" in html,
                "load_speed": "estimated",  # Would need more tools
                "seo_score": self._calculate_seo_score(html)
            }
            return analysis
        except Exception as e:
            return {"error": str(e)}

    def optimize_site_seo(self, analysis, keywords=["junk removal", "Vilnius", "eco-friendly"]):
        """Generate SEO optimizations"""
        optimizations = {
            "title_suggestions": [f"{kw} Services - Quick Junk Removal Vilnius" for kw in keywords],
            "meta_description": f"Professional {keywords[0]} services in {keywords[1]}. Eco-friendly disposal, fast service, 5-star rated. Call now!",
            "h1_optimization": f"Expert {keywords[0]} in {keywords[1]}",
            "schema_markup": self._generate_schema_markup(keywords),
            "internal_links": ["#services", "#contact", "#testimonials"],
            "alt_tags": f"Add alt tags for images: '{keywords[0]} service in {keywords[1]}'",
            "url_structure": f"Optimize URLs to include: {keywords[0].replace(' ', '-')}-{keywords[1].lower()}"
        }
        return optimizations

    def rewrite_content(self, original_content, keywords=["junk removal", "Vilnius"], target_audience="local customers"):
        """Rewrite content for better SEO using Gemini API"""
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not api_key or api_key.startswith("YOUR"):
            return f"Expert rewritten content: {original_content[:100]}... (optimized for {keywords})"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        prompt = f"""As an expert SEO content rewriter, rewrite the following content to be more SEO-optimized and engaging:

Original content: {original_content}

Requirements:
- Target keywords: {', '.join(keywords)}
- Target audience: {target_audience}
- Improve readability and engagement
- Add relevant headings (H2, H3)
- Include calls-to-action
- Maintain factual accuracy
- Optimize for search engines while keeping natural language
- Add internal/external link suggestions
- Improve meta description potential

Return the rewritten content in Jekyll blog post format with front matter."""

        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Rewrite failed: {response.status_code}. Expert fallback: {original_content}"

    def rewrite_existing_posts(self, keywords=["junk removal", "Vilnius"]):
        """Rewrite existing blog posts for better SEO"""
        rewrites = []

        # Get list of existing posts
        posts_url = f"{self.api_base}/contents/_posts"
        response = requests.get(posts_url, headers=self.headers)
        if response.status_code == 200:
            posts = response.json()
            for post in posts[:3]:  # Limit to first 3 posts
                if post['name'].endswith('.md'):
                    # Get post content
                    post_response = requests.get(post['url'], headers=self.headers)
                    if post_response.status_code == 200:
                        content_b64 = post_response.json()['content']
                        original_content = base64.b64decode(content_b64).decode()

                        # Rewrite content
                        rewritten = self.rewrite_content(original_content, keywords)
                        if rewritten and not rewritten.startswith("Rewrite failed"):
                            # Update post
                            rewritten_b64 = base64.b64encode(rewritten.encode()).decode()
                            update_data = {
                                "message": "SEO content rewrite by AI agent",
                                "content": rewritten_b64,
                                "sha": post_response.json()['sha']
                            }
                            update_response = requests.put(post['url'], json=update_data, headers=self.headers)
                            if update_response.status_code in [200, 201]:
                                rewrites.append(f"Rewrote {post['name']}")
                            else:
                                rewrites.append(f"Failed to rewrite {post['name']}: {update_response.status_code}")
                        else:
                            rewrites.append(f"Rewrite skipped for {post['name']}")

        return rewrites

    def update_site_files(self, optimizations):
        """Update site files via GitHub API"""
        updates = []

        # Update _config.yml with better SEO settings
        config_content = """title: Quick Junk Removal Vilnius
description: Elite junk removal services with eco-friendly disposal, fast service, and 5-star customer satisfaction in Vilnius
url: https://manupupww.github.io
baseurl: /test-seo-site

markdown: kramdown
highlighter: rouge

plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag

author: Quick Junk Removal Team
social:
  name: Quick Junk Removal
  links:
    - https://facebook.com/quickjunkremoval
    - https://instagram.com/quickjunkremoval

seo:
  type: Business
  name: Quick Junk Removal Vilnius
  telephone: +370-XXX-XXXX
  address:
    streetAddress: Example Street 123
    addressLocality: Vilnius
    addressRegion: Vilnius
    postalCode: 01111
    addressCountry: LT
"""

        updates.append(self._update_file("_config.yml", config_content, "Update site config with SEO enhancements"))

        # Update _layouts/default.html with better meta tags and schema
        layout_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if page.title %}{{ page.title }}{% else %}{{ site.title }}{% endif %}</title>
    <meta name="description" content="{% if page.description %}{{ page.description }}{% else %}{{ site.description }}{% endif %}">
    <meta name="keywords" content="junk removal, Vilnius, eco-friendly, disposal, waste management, Lithuania">
    <meta name="author" content="{{ site.author }}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{% if page.title %}{{ page.title }}{% else %}{{ site.title }}{% endif %}">
    <meta property="og:description" content="{% if page.description %}{{ page.description }}{% else %}{{ site.description }}{% endif %}">
    <meta property="og:url" content="{{ site.url }}{{ page.url }}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{% if page.title %}{{ page.title }}{% else %}{{ site.title }}{% endif %}">
    <meta name="twitter:description" content="{% if page.description %}{{ page.description }}{% else %}{{ site.description }}{% endif %}">

    <!-- Schema.org markup -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Quick Junk Removal Vilnius",
      "description": "Professional junk removal services in Vilnius with eco-friendly disposal",
      "url": "https://manupupww.github.io/test-seo-site/",
      "telephone": "+370-XXX-XXXX",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Example Street 123",
        "addressLocality": "Vilnius",
        "addressRegion": "Vilnius",
        "postalCode": "01111",
        "addressCountry": "LT"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 54.6872,
        "longitude": 25.2797
      },
      "openingHours": "Mo-Fr 08:00-18:00",
      "priceRange": "$$"
    }
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body>
    {{ content }}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

        updates.append(self._update_file("_layouts/default.html", layout_content, "Update layout with comprehensive SEO meta tags and schema markup"))

        # Rewrite existing posts
        rewrites = self.rewrite_existing_posts(keywords=["junk removal", "Vilnius", "eco-friendly"])
        updates.extend(rewrites)

        return updates

    def _update_file(self, path, content, message):
        """Update a file on GitHub"""
        url = f"{self.api_base}/contents/{path}"

        # Get current file info
        response = requests.get(url, headers=self.headers)
        sha = None
        if response.status_code == 200:
            sha = response.json().get("sha")

        # Encode content
        content_b64 = base64.b64encode(content.encode()).decode()

        data = {
            "message": message,
            "content": content_b64
        }
        if sha:
            data["sha"] = sha

        response = requests.put(url, json=data, headers=self.headers)
        if response.status_code in [200, 201]:
            return f"Successfully updated {path}"
        else:
            return f"Failed to update {path}: {response.status_code} - {response.text}"

    def _extract_title(self, html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else ""
        return title.strip()

    def _extract_meta_description(self, html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        meta = soup.find("meta", attrs={"name": "description"})
        return meta.get("content", "") if meta else ""

    def _extract_h1s(self, html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        h1s = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
        return h1s

    def _calculate_seo_score(self, html):
        score = 0
        if "<title>" in html: score += 20
        if 'name="description"' in html: score += 20
        if "<h1>" in html: score += 15
        if "viewport" in html: score += 10
        if "og:" in html: score += 15
        if "schema.org" in html: score += 20
        return min(score, 100)

    def _generate_schema_markup(self, keywords):
        return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{keywords[0]} Services",
  "description": "Professional {keywords[0]} in {keywords[1]}",
  "provider": {{
    "@type": "LocalBusiness",
    "name": "Quick Junk Removal Vilnius"
  }},
  "areaServed": {{
    "@type": "City",
    "name": "{keywords[1]}"
  }}
}}
</script>"""

    def generate_faq_content(self, industry="junk removal", location="Vilnius"):
        """Generate FAQ content for better SEO and user engagement"""
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not api_key or api_key.startswith("YOUR"):
            return self._generate_mock_faq(industry, location)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        prompt = f"""Generate 10 comprehensive FAQ questions and answers for a {industry} business in {location}.

Requirements:
- Questions should be what customers actually ask
- Answers should be helpful, detailed, and include local {location} information
- Include pricing, services, process, eco-friendly aspects
- Format as structured FAQ with schema markup ready
- Make it SEO-optimized with natural keyword usage
- Include calls-to-action where appropriate

Return in Jekyll markdown format with FAQ schema."""

        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return self._generate_mock_faq(industry, location)

    def _generate_mock_faq(self, industry, location):
        """Mock FAQ generation"""
        return f"""---
layout: page
title: "FAQ - {industry.title()} Services in {location}"
description: "Frequently asked questions about professional {industry} services in {location}"
---

# Frequently Asked Questions

## How much does {industry} cost in {location}?

Prices vary based on volume and type of items. Basic residential cleanouts start at €50-€100, while full house cleanouts range from €200-€500. We provide free estimates and transparent pricing with no hidden fees.

## Do you offer eco-friendly {industry} services?

Yes! We prioritize environmental responsibility. We recycle up to 80% of materials and donate usable items to local charities in {location}. Our eco-friendly disposal methods minimize landfill impact.

## What areas in {location} do you serve?

We serve all areas of {location} including the city center, suburbs, and surrounding regions. Same-day service available for most locations within city limits.

## How quickly can you respond to {industry} requests?

We offer same-day service for urgent needs and can typically schedule appointments within 24 hours. Emergency situations receive priority response.

## What items do you accept for {industry}?

We handle all types of household, office, and construction waste including furniture, appliances, electronics, and construction debris. Some restrictions apply for hazardous materials.

## Do you provide {industry} for businesses?

Absolutely! We offer commercial {industry} services for offices, retail spaces, and construction sites. Volume discounts available for large projects.

## Are your {industry} services insured and licensed?

Yes, our team is fully licensed, insured, and bonded. We carry comprehensive liability insurance to protect your property during service.

## What should I do to prepare for {industry} service?

Sort items if possible, ensure clear access to the area, and let us know about any special handling requirements. We'll guide you through the preparation process.

## Do you offer donation services?

Yes, we partner with local charities in {location} to donate usable items. This helps the community and reduces waste sent to landfills.

## How do I schedule {industry} service?

Contact us at +370-XXX-XXXX or use our online booking form. We'll provide a free estimate and schedule your service at your convenience.

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "How much does {industry} cost in {location}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Prices vary based on volume and type of items..."
      }}
    }}
  ]
}}
</script>"""

    def update_faq_page(self, industry="junk removal", location="Vilnius"):
        """Generate and update FAQ page on website"""
        faq_content = self.generate_faq_content(industry, location)

        # Update/create FAQ page
        return self._update_file("faq.md", faq_content, "Add comprehensive FAQ page for SEO")

# Usage: tool = SEOOptimizerTool(firecrawl_key, github_token); analysis = tool.analyze_site_seo(); optimizations = tool.optimize_site_seo(analysis); updates = tool.update_site_files(optimizations)