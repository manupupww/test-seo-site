import requests
import os

def create_generation_chain():
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key or api_key.startswith("YOUR"):
        def mock_run(documents=None, keywords="", geo="", content_type="", target_audience=""):
            keywords_str = ', '.join(keywords) if isinstance(keywords, list) else str(keywords)
            return f"""---
layout: post
title: "Expert SEO Post: {keywords_str} in {geo}"
date: 2025-11-15
categories: seo
tags: [{keywords_str}, {geo}]
---

# Expert Generated Content

This is mock content for testing. Real content would be generated using AI for keywords: {keywords_str} in {geo}.

Content type: {content_type}
Target audience: {target_audience}

Superior SEO-optimized content would appear here.
"""
        return mock_run

    def gen_run(documents=None, keywords="", geo="", content_type="", target_audience=""):
        # Direct Gemini API call for content generation
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        context = str(documents) if documents else "No analysis provided"
        prompt = f"""As an expert SEO supervisor better than any human, generate a high-quality, SEO-optimized blog post based on analysis: {context}
        Target keywords: {keywords}
        Geo location: {geo}
        Content type: {content_type}
        Target audience: {target_audience}
        Make it engaging, rank-boosting, superior to human content. Include meta descriptions, headings, calls to action. Format as Jekyll blog post."""
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        try:
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                content = result['candidates'][0]['content']['parts'][0]['text']
                # Format as Jekyll post
                keywords_str = ', '.join(keywords) if isinstance(keywords, list) else str(keywords).replace(' ', ', ')
                return f"""---
layout: post
title: "Expert SEO Post: {keywords_str} in {geo}"
date: 2025-11-15
categories: seo
tags: [{keywords_str}, {geo}]
---

{content}
"""
            else:
                # Fallback to mock on API error
                return mock_run(documents, keywords, geo, content_type, target_audience)
        except Exception as e:
            # Fallback to mock on any error
            return mock_run(documents, keywords, geo, content_type, target_audience)

    return gen_run

# Usage: chain = create_generation_chain(); result = chain("analysis", "keywords", "geo")