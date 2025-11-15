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

### 4. Deploy to Render (24/7)
1. Go to https://dashboard.render.com
2. Create new "Web Service"
3. Connect GitHub repo: `manupupww/test-seo-site` (your website repo)
4. Runtime: Docker
5. Branch: main
6. Build Command: (leave empty)
7. Start Command: `sh -c "cron && tail -f /dev/null"`
8. Environment: Add variables from .env
9. Deploy

### 5. Verify
- Check Render logs for agent activity
- Visit your website to see new posts
- Agent runs every 6 hours automatically

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