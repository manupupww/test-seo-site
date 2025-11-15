import requests
import os

def create_generation_chain():
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key or api_key.startswith("YOUR"):
        def mock_run(docs, keywords, geo):
            return f"Expert generated blog post with keywords: {keywords}, geo: {geo}. Superior content: {docs}"
        return mock_run

    def gen_run(docs, keywords, geo):
        # Direct Gemini API call for content generation
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        context = str(docs) if docs else "No analysis provided"
        prompt = f"""As an expert SEO supervisor better than any human, generate a high-quality, SEO-optimized blog post based on analysis: {context}
        Target keywords: {keywords}
        Geo location: {geo}
        Make it engaging, rank-boosting, superior to human content. Include meta descriptions, headings, calls to action. Format as Jekyll blog post."""
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            # Format as Jekyll post
            return f"""---
layout: post
title: "Expert SEO Post: {keywords} in {geo}"
date: 2025-11-15
categories: seo
tags: [{keywords.replace(' ', ', ')}, {geo}]
---

{content}
"""
        else:
            return f"API Error: {response.status_code}. Expert fallback post."

    return gen_run

# Usage: chain = create_generation_chain(); result = chain("analysis", "keywords", "geo")