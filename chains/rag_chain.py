import requests
import os

def create_rag_chain(site_url="https://manupupww.github.io/test-seo-site/"):
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        def mock_run(query):
            return f"Expert RAG analysis for: {query}. Site needs better keywords and competitor insights."
        return mock_run

    def rag_run(query):
        # Direct Gemini API call for RAG-like analysis
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        prompt = f"As an expert SEO supervisor, analyze the site at {site_url} for SEO gaps based on query: {query}. Provide detailed insights."
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"API Error: {response.status_code}. Expert fallback: Optimize keywords and monitor competitors."

    return rag_run

# Usage: chain = create_rag_chain(); result = chain("Analyze SEO gaps")