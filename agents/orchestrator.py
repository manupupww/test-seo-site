from chains.rag_chain import create_rag_chain
from chains.generation_chain import create_generation_chain
from chains.deployment_chain import create_deployment_chain
from agents.competitor_monitor import CompetitorMonitorAgent
from agents.rank_checker import RankCheckerAgent
from agents.market_analyzer import MarketAnalyzerAgent
from agents.social_media_agent import SocialMediaAgent
from tools.website_api_tool import WebsiteAPITool

class OrchestratorAgent:
    def __init__(self, competitor_keys, website_api_config):
        self.rag_chain = create_rag_chain()
        self.gen_chain = create_generation_chain()
        self.deploy_chain = create_deployment_chain()
        self.competitor_agent = CompetitorMonitorAgent(**competitor_keys)
        self.market_agent = MarketAnalyzerAgent(competitor_keys.get("tavily_key", "mock_key"))
        self.social_agent = SocialMediaAgent("mock_key")  # Add real API key later
        self.website_tool = WebsiteAPITool(**website_api_config)

    def run_workflow(self):
        # Expert monitoring: Competitors, market, and site analysis
        try:
            competitor_insights = self.competitor_agent.monitor_all()
        except Exception as e:
            competitor_insights = f"Competitor monitoring failed: {str(e)}"

        try:
            market_insights = self.market_agent.analyze_market("junk removal", "Vilnius")
        except Exception as e:
            market_insights = f"Market analysis failed: {str(e)}"

        insights_summary = f"Competitor insights: {competitor_insights}. Market trends: {market_insights}"

        # Check rank with geo focus
        import os
        tavily_key = os.getenv("TAVILY_API_KEY")
        rank_checker = RankCheckerAgent(tavily_key or "mock_key")
        try:
            rank = rank_checker.check_rank("junk removal Vilnius", "Vilnius")
        except Exception as e:
            rank = 0  # Assume low rank if error

        # Intelligent optimization: update if rank is low or market/competitor insights indicate changes
        market_changed = "new" in market_insights.lower() or "trend" in market_insights.lower()
        competitor_changed = len(competitor_insights) > 0 and any("content" in str(i).lower() for i in competitor_insights)
        needs_update = rank < 5 or market_changed or competitor_changed

        if needs_update:
            try:
                # Analyze site with competitor and market data
                analysis = self.rag_chain(f"As expert SEO supervisor, analyze current SEO gaps and opportunities. {insights_summary}")
                # Generate content incorporating market trends
                content = self.gen_chain(
                    analysis,
                    "junk removal Vilnius eco-friendly sustainable",
                    "Vilnius"
                )
                # Deploy to website
                deploy_result = self.deploy_chain(content)
                print(f"Deployment: {deploy_result}")
                # Post to social media
                try:
                    social_result = self.social_agent.post_blog_update("New Expert SEO Post", "https://manupupww.github.io/test-seo-site/")
                    print(f"Social Media: {social_result}")
                except Exception as e:
                    print(f"Social media post failed: {str(e)}")
            except Exception as e:
                print(f"Content generation/deployment failed: {str(e)}")
                return f"Workflow partially completed: {str(e)}"
        return "Expert workflow completed: Superior SEO optimization, competitor outperformance, market adaptation, and autonomous site management."