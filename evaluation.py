from google.adk.evaluation import Criteria
from langchain.callbacks import StdOutCallbackHandler

# ADK Evaluation Criteria
rank_improvement = Criteria(
    name="rank_improvement",
    description="Measure if rank improved after content update",
    evaluator=lambda result: result.get("new_rank", 0) > result.get("old_rank", 0)
)

content_quality = Criteria(
    name="content_quality",
    description="Assess SEO quality of generated content",
    evaluator=lambda result: len(result.get("content", "")) > 500  # Simple check
)

competitor_gap = Criteria(
    name="competitor_gap",
    description="Check if we closed the gap with competitors",
    evaluator=lambda result: result.get("our_rank", 10) <= result.get("competitor_rank", 10)
)

update_success = Criteria(
    name="update_success",
    description="Verify website/blog updates were successful",
    evaluator=lambda result: result.get("update_status") == "success"
)

# LangChain Callbacks for Safety
safety_callback = StdOutCallbackHandler()

# Usage in agents
# agent.callbacks = [safety_callback]
# runtime.evaluate(criteria=[rank_improvement, content_quality, competitor_gap, update_success])