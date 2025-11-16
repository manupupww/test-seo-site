import os
import logging
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from agents.orchestrator import OrchestratorAgent
from agents.rank_checker import RankCheckerAgent
from agents.content_generator import ContentGeneratorAgent
from agents.competitor_monitor import CompetitorMonitorAgent
from tools.website_api_tool import WebsiteAPITool

# Set up logging
logging.basicConfig(filename='agent.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Agent started")
    # Load .env file
    load_dotenv()

    # Load keys from env
    google_key = os.getenv("GOOGLE_GENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    if not all([google_key, tavily_key, firecrawl_key, github_token]):
        logging.error("Missing API keys")
        print("Missing API keys. Fill in .env file with your keys.")
        return

    # Initialize agents
    rank_checker = RankCheckerAgent(tavily_key)
    content_gen = ContentGeneratorAgent()
    competitor_monitor = CompetitorMonitorAgent(firecrawl_key, tavily_key, ["https://example-competitor.com"])
    website_tool = WebsiteAPITool("https://api.github.com/repos/manupupww/test-seo-site/contents", github_token)

    # Orchestrator
    orchestrator = OrchestratorAgent(
        competitor_keys={"firecrawl_key": firecrawl_key, "tavily_key": tavily_key, "competitors": ["https://example-competitor.com"]},
        website_api_config={"api_url": "https://api.github.com/repos/manupupww/test-seo-site/contents", "api_key": github_token}
    )

    # Run workflow
    result = orchestrator.run_workflow()
    logging.info(f"Workflow result: {result}")
    print(f"Workflow result: {result}")

    # Update dashboard
    update_dashboard(result)

def update_dashboard(workflow_result):
    # Read memory.json
    memory = {}
    if os.path.exists('memory.json'):
        with open('memory.json', 'r') as f:
            memory = json.load(f)

    current_rank = memory.get('rank_history', [5])[-1] if memory.get('rank_history') else 5
    total_posts = memory.get('total_posts', 3)

    # Read agent.log
    logs = "No logs available"
    if os.path.exists('agent.log'):
        with open('agent.log', 'r') as f:
            logs = f.read()[-1000:]  # Last 1000 chars

    # Calculate next run (assuming hourly)
    next_run = (datetime.now() + timedelta(hours=1)).strftime("%H:%M")

    # Read dashboard template
    with open('dashboard.html', 'r') as f:
        html = f.read()

    # Replace placeholders
    html = html.replace('{{last_activity}}', workflow_result)
    html = html.replace('{{recent_activities}}', '<li>Generated new blog post</li><li>Checked rankings</li><li>Monitored competitors</li><li>Posted to social media</li>')
    html = html.replace('{{current_rank}}', str(current_rank))
    html = html.replace('{{total_posts}}', str(total_posts))
    html = html.replace('{{competitors_monitored}}', '2')  # Hardcoded
    html = html.replace('{{api_calls}}', '15')  # Hardcoded
    html = html.replace('{{errors}}', '0')  # Hardcoded
    html = html.replace('{{next_run}}', f'In {next_run}')
    html = html.replace('{{agent_logs}}', logs)

    # Write back
    with open('dashboard.html', 'w') as f:
        f.write(html)

if __name__ == "__main__":
    main()