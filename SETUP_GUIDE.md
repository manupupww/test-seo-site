# Junk Removal SEO Agent Setup Guide

## Overview
This agent automates SEO for your junk removal business: creates blog posts, monitors competitors, checks rankings, and updates your website every 6 hours.

## Security First
- Never share API keys
- Use environment variables for secrets
- Don't commit .env file to GitHub

## Step-by-Step Setup

### 1. Get API Keys
- **Google AI**: https://makersuite.google.com/app/apikey (free)
- **Tavily Search**: https://tavily.com (free tier available)
- **Firecrawl**: https://firecrawl.dev (free tier)
- **GitHub Token**: https://github.com/settings/tokens
  - Create "Classic" token
  - Select scopes: `repo` (full control of private repos)
  - Copy token (save securely)

### 2. Update .env File
Fill in your real API keys in `.env` file (never commit this file).

### 3. Test Locally
Run `python main.py` to test if everything works.

### 4. Deploy to GitHub (24/7 net kai kompiuteris išjungtas)
1. Push kodą į savo GitHub repo
2. Eikite į repo Settings > Secrets and variables > Actions
3. Pridėkite secrets iš .env failo:
   - GOOGLE_GENAI_API_KEY
   - TAVILY_API_KEY
   - FIRECRAWL_API_KEY
   - GITHUB_TOKEN
4. Sukurkite .github/workflows/main.yml failą automatiniam veikimui
5. Deploy - agentas veiks 24/7 per GitHub Actions

### 5. Verify
- Check GitHub Actions logs for agent activity
- Visit your website to see new posts
- Agent runs automatically pagal nustatytą schedule

## What the Agent Does
- Generates SEO-optimized blog posts
- Monitors competitor websites
- Checks search rankings
- Updates website content automatically
- Adapts to market trends

## Troubleshooting
- If deployment fails: Check Render logs
- Token issues: Verify GitHub token scopes
- API limits: Monitor usage on provider dashboards