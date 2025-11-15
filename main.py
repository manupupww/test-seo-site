import os
from dotenv import load_dotenv
from agents.orchestrator import OrchestratorAgent
from agents.rank_checker import RankCheckerAgent
from agents.content_generator import ContentGeneratorAgent
from agents.competitor_monitor import CompetitorMonitorAgent
from tools.website_api_tool import WebsiteAPITool

def main():
    # Load .env file
    load_dotenv()

    # Load keys from env
    google_key = os.getenv("GOOGLE_GENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    if not all([google_key, tavily_key, firecrawl_key, github_token]):
        print("Missing API keys. Fill in .env file with your keys.")
        return

    # Initialize agents
    rank_checker = RankCheckerAgent(tavily_key)
    content_gen = ContentGeneratorAgent()
    competitor_monitor = CompetitorMonitorAgent(firecrawl_key, tavily_key, ["https://example-competitor.com"])
    github_token = os.getenv("GITHUB_TOKEN")  # Set this env var
    website_tool = WebsiteAPITool("https://api.github.com/repos/manupupww/test-seo-site/contents", github_token)

    # Orchestrator
    orchestrator = OrchestratorAgent(
        competitor_keys={"firecrawl_key": firecrawl_key, "tavily_key": tavily_key, "competitors": ["https://example-competitor.com"]},
        website_api_config={"api_url": "https://api.github.com/repos/manupupww/test-seo-site/contents", "api_key": "your_github_token"}
    )

    # Run workflow
    result = orchestrator.run_workflow()
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    main()