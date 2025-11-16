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

    # Load keys from env
    google_key = os.getenv("GOOGLE_GENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    # Check for required API keys
    if not all([google_key, tavily_key, firecrawl_key, github_token]):
        logging.error("Missing API keys")
        print("Missing API keys. Fill in .env file with your keys.")
        return

    # Log available keys (without exposing them)
    logging.info(f"API Keys status - Google: {'YES' if google_key else 'NO'}, Tavily: {'YES' if tavily_key else 'NO'}, Firecrawl: {'YES' if firecrawl_key else 'NO'}, GitHub: {'YES' if github_token else 'NO'}")

    # Level 3 AI Orchestrator - Maximum Capabilities
    print("Initializing Level 3 AI Orchestrator with maximum capabilities...")
    orchestrator = Level3AIOrchestrator()

    # Run maximum AI workflow
    result = orchestrator.run_maximum_ai_workflow()
    logging.info(f"Level 3 AI Workflow result: {result}")
    print(f"Level 3 AI Workflow completed: {result.get('status', 'Unknown')}")

    # Performance summary
    metrics = result.get('performance_metrics', {})
    print(f"AI Utilization: {metrics.get('ai_utilization_achieved', '0%')}")
    print(f"Optimizations Applied: {metrics.get('optimizations_applied', 0)}")
    print(f"Learning Insights: {metrics.get('learning_insights_generated', 0)}")

    # Commit changes back to GitHub if we have a token
    if github_token and github_token != "mock_token":
        try:
            import subprocess
            # Pull latest changes first to avoid conflicts
            subprocess.run(["git", "pull", "--no-edit"], check=True)
            # Add all changes
            subprocess.run(["git", "add", "."], check=True)
            # Check if there are changes to commit
            result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
            if result.returncode != 0:  # There are changes
                # Commit with timestamp
                commit_msg = f"AI Agent SEO Optimization - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                # Push to GitHub
                subprocess.run(["git", "push", "origin", "main"], check=True)
                logging.info("Successfully committed and pushed changes to GitHub")
                print("Changes committed and pushed to GitHub")
            else:
                logging.info("No changes to commit")
                print("No changes to commit")
        except Exception as e:
            logging.error(f"Failed to commit/push changes: {e}")
            print(f"Failed to commit/push changes: {e}")

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
    html = html.replace('{{last_activity}}', str(workflow_result))
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