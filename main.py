import os
import logging
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from agents.level3_ai_orchestrator import Level3AIOrchestrator
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

    # Check deployment mode
    deployment_mode = os.getenv("DEPLOYMENT_MODE", "local")
    update_frequency = os.getenv("UPDATE_FREQUENCY", "hourly")

    logging.info(f"Deployment mode: {deployment_mode}, Update frequency: {update_frequency}")

    # Load keys from env
    google_key = os.getenv("GOOGLE_GENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    # For Railway deployment, allow missing keys initially (will use mock data)
    if deployment_mode == "local" and not all([google_key, tavily_key, firecrawl_key, github_token]):
        logging.error("Missing API keys in local mode")
        print("Missing API keys. Fill in .env file with your keys.")
        return

    # Log available keys (without exposing them)
    logging.info(f"API Keys status - Google: {'YES' if google_key else 'NO'}, Tavily: {'YES' if tavily_key else 'NO'}, Firecrawl: {'YES' if firecrawl_key else 'NO'}, GitHub: {'YES' if github_token else 'NO'}")

    # Level 3 AI Orchestrator - Maximum Capabilities
    print("🚀 Initializing Level 3 AI Orchestrator with maximum capabilities...")
    orchestrator = Level3AIOrchestrator()

    # Run maximum AI workflow
    result = orchestrator.run_maximum_ai_workflow()
    logging.info(f"Level 3 AI Workflow result: {result}")
    print(f"🎯 Level 3 AI Workflow completed: {result.get('status', 'Unknown')}")

    # Performance summary
    metrics = result.get('performance_metrics', {})
    print(f"📊 AI Utilization: {metrics.get('ai_utilization_achieved', '0%')}")
    print(f"⚡ Optimizations Applied: {metrics.get('optimizations_applied', 0)}")
    print(f"🧠 Learning Insights: {metrics.get('learning_insights_generated', 0)}")

    # For Railway deployment, commit changes back to GitHub if we have a token
    if deployment_mode == "railway" and github_token and github_token != "mock_token":
        try:
            import subprocess
            # Add all changes
            subprocess.run(["git", "add", "."], check=True)
            # Commit with timestamp
            commit_msg = f"AI Agent SEO Optimization - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            # Push to GitHub
            subprocess.run(["git", "push", "origin", "main"], check=True)
            logging.info("Successfully committed and pushed changes to GitHub")
            print("Changes committed and pushed to GitHub")
        except Exception as e:
            logging.error(f"Failed to commit/push changes: {e}")
            print(f"Failed to commit/push changes: {e}")

    # Update dashboard (only in local mode)
    if deployment_mode == "local":
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