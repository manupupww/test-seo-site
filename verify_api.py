#!/usr/bin/env python3
"""
API Key Verification Script
Tests if your Google AI API key is working correctly
"""

import requests
import os
from dotenv import load_dotenv

def test_api_key():
    """Test the Google AI API key"""
    print("Testing Google AI API Key...")
    print("=" * 50)

    # Load environment variables
    load_dotenv()

    api_key = os.getenv('GOOGLE_GENAI_API_KEY')

    # Check if key exists
    if not api_key:
        print("ERROR: GOOGLE_GENAI_API_KEY not found in .env file")
        return False

    if api_key == "YOUR_NEW_API_KEY_HERE":
        print("ERROR: API key is still placeholder. Please update .env file with your real API key!")
        return False

    print(f"API key found (length: {len(api_key)})")

    # Test 1: Models list API
    print("\n1. Testing Models List API...")
    models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    try:
        response = requests.get(models_url, timeout=10)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            models = response.json()
            gemini_models = [m['name'] for m in models.get('models', []) if 'gemini' in m['name']]
            print(f"   Available Gemini models: {len(gemini_models)}")
            for model in gemini_models[:3]:  # Show first 3
                print(f"      - {model}")
        else:
            print(f"   Models API failed: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"   Models API error: {e}")
        return False

    # Test 2: Content generation API
    print("\n2. Testing Content Generation API...")
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    data = {
        "contents": [{
            "parts": [{"text": "Generate a short SEO title for junk removal services in Vilnius."}]
        }]
    }

    try:
        response = requests.post(gen_url, json=data, timeout=15)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            print("   Content generation successful!")
            print(f"   Generated: {content[:100]}...")
            return True
        else:
            print(f"   Generation API failed: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"   Generation API error: {e}")
        return False

def main():
    print("Google AI API Key Verification")
    print("This script tests if your API key is working correctly")
    print()

    success = test_api_key()

    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: Your API key is working perfectly!")
        print("The agent will now use real Google AI instead of mock data.")
        print("\nNext steps:")
        print("1. Run: python working_agent.py")
        print("2. The agent will generate real AI content")
    else:
        print("FAILURE: API key is not working")
        print("\nTroubleshooting:")
        print("1. Check your .env file has the real API key")
        print("2. Verify API key has no restrictions in Google Cloud Console")
        print("3. Ensure Generative AI API is enabled")
        print("4. Try regenerating the API key")

if __name__ == "__main__":
    main()