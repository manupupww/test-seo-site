from tools.seo_optimizer_tool import SEOOptimizerTool

class SEOOptimizerAgent:
    def __init__(self, firecrawl_key, github_token):
        self.tool = SEOOptimizerTool(firecrawl_key, github_token)

    def optimize_website_seo(self, keywords=["junk removal", "Vilnius", "eco-friendly"]):
        """Complete website SEO optimization workflow"""
        try:
            # Analyze current SEO status
            analysis = self.tool.analyze_site_seo()
            print(f"SEO Analysis: {analysis}")

            # Generate optimizations
            optimizations = self.tool.optimize_site_seo(analysis, keywords)
            print(f"Generated Optimizations: {optimizations}")

            # Apply updates to site files (includes content rewriting)
            updates = self.tool.update_site_files(optimizations)
            print(f"Site Updates: {updates}")

            # Generate and update FAQ page
            faq_update = self.tool.update_faq_page("junk removal", "Vilnius")
            print(f"FAQ Update: {faq_update}")
            updates.append(faq_update)

            return {
                "analysis": analysis,
                "optimizations": optimizations,
                "updates": updates,
                "status": "SEO optimization, content rewriting, and FAQ generation completed successfully"
            }
        except Exception as e:
            print(f"SEO optimization failed: {str(e)}")
            return {"error": str(e)}

# Usage: agent = SEOOptimizerAgent(firecrawl_key, github_token); result = agent.optimize_website_seo()