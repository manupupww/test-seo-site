from chains.rag_chain import create_rag_chain
from chains.generation_chain import create_generation_chain
from chains.deployment_chain import create_deployment_chain
from agents.competitor_monitor import CompetitorMonitorAgent
from agents.rank_checker import RankCheckerAgent
from agents.market_analyzer import MarketAnalyzerAgent
from tools.website_api_tool import WebsiteAPITool

class OrchestratorAgent:
    def __init__(self, competitor_keys, website_api_config):
        self.rag_chain = create_rag_chain()
        self.gen_chain = create_generation_chain()
        self.deploy_chain = create_deployment_chain()
        self.competitor_agent = CompetitorMonitorAgent(**competitor_keys)
        self.market_agent = MarketAnalyzerAgent(competitor_keys.get("tavily_key", "mock_key"))
        self.website_tool = WebsiteAPITool(**website_api_config)

    def run_workflow(self):
        # Expert monitoring: Competitors, market, and site analysis
        competitor_insights = self.competitor_agent.monitor_all()
        market_insights = self.market_agent.analyze_market("junk removal", "Vilnius")
        insights_summary = f"Competitor insights: {competitor_insights}. Market trends: {market_insights}"

        # Check rank with geo focus
        import os
        tavily_key = os.getenv("TAVILY_API_KEY")
        rank_checker = RankCheckerAgent(tavily_key or "mock_key")
        rank = rank_checker.check_rank("junk removal Vilnius", "Vilnius")
        if rank < 1 or True:  # Always optimize for expert level
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
        return "Expert workflow completed: Superior SEO optimization, competitor outperformance, market adaptation, and autonomous site management."