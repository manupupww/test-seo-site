# SEO Automation Agent System

This project implements an expert-level AI agent that surpasses human SEO supervisors in website optimization, blog content generation, rank monitoring, competitor analysis, and autonomous site management using Google's ADK and LangChain.

## Features
- **Multi-Agent Architecture**: Orchestrator coordinates specialized agents via A2A protocol.
- **Geo-Focused SEO**: Location-based search and content optimization for local businesses like junk removal.
- **Competitor Monitoring**: Scrape and analyze competitor sites/strategies in the junk removal niche.
- **Market Monitoring**: Track industry trends, keywords, and news for proactive SEO.
- **Website Integration**: Direct API connections for autonomous updates and blog uploads to GitHub Pages.
- **Hybrid Framework**: ADK for orchestration + LangChain for chains and memory.
- **Tools Integration**: Tavily (search), Firecrawl (scraping), GitHub (deployment), Website API.
- **Evaluation & Safety**: Built-in criteria and callbacks for ethical operation.

## Setup
1. Install dependencies: `pip install langchain langchain-google-genai langchain-community tavily-python firecrawl-py python-dotenv requests`
2. Set API keys in `.env` file.
3. For local testing: `python main.py`
4. For 24/7 operation: Run `run_24h.bat` (Windows) or schedule with Task Scheduler.

## 24/7 Local Deployment
- Run `run_24h.bat` to start the agent in a loop (runs every 6 hours).
- Alternatively, use Windows Task Scheduler: Create a task to run `python main.py` every 6 hours.

## Docker Deployment (Alternative)
1. Ensure Docker Desktop is running.
2. Build: `docker build -t seo-agent .`
3. Run: `docker-compose up -d`
4. The agent runs every 6 hours via cron.
5. Logs: `docker-compose logs`
6. Stop: `docker-compose down`

## Cloud Deployment (24/7 kai kompiuteris išjungtas)
Rekomenduojama naudoti Render.com:
1. Push kodą į GitHub
2. Sukurkite Render Web Service
3. Prijunkite GitHub repo
4. Runtime: Docker
5. Start Command: `sh -c "cron && tail -f /dev/null"`
6. Pridėkite API keys į Environment
7. Deploy - agentas veiks 24/7 debesyje

## Local Docker (testavimui)
```bash
docker-compose up -d
```
Logs: `docker-compose logs -f`

## Architecture
- **Agents**: orchestrator.py, rank_checker.py, content_generator.py, competitor_monitor.py
- **Chains**: rag_chain.py, generation_chain.py, deployment_chain.py
- **Tools**: geo_search.py, firecrawl_tool.py, competitor_tool.py, website_api_tool.py
- **Config**: agent_config.yaml

## New Enhancements
- **Competitor Monitoring**: Daily analysis of competitor SEO and content.
- **Website API Integration**: Automatic blog uploads and site updates.
- **Advanced Evaluation**: Competitor gap and update success metrics.

This is a cutting-edge, autonomous system for full SEO dominance!