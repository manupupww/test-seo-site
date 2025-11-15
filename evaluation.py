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

# Additional criteria to avoid penalties
content_uniqueness = Criteria(
    name="content_uniqueness",
    description="Ensure content is unique and not duplicated",
    evaluator=lambda result: len(set(result.get("content", "").split())) / len(result.get("content", "").split()) > 0.7  # Rough uniqueness check
)

keyword_density = Criteria(
    name="keyword_density",
    description="Check keyword density is not too high (avoid stuffing)",
    evaluator=lambda result: result.get("keyword_density", 0) < 0.05  # Less than 5%
)

natural_language = Criteria(
    name="natural_language",
    description="Assess if content reads naturally (basic check)",
    evaluator=lambda result: " " in result.get("content", "") and len(result.get("content", "").split(".")) > 3  # Has spaces and sentences
)

update_frequency = Criteria(
    name="update_frequency",
    description="Ensure updates are not too frequent",
    evaluator=lambda result: result.get("hours_since_last_update", 24) >= 6  # At least 6 hours
)

# LangChain Callbacks for Safety
safety_callback = StdOutCallbackHandler()

# Usage in agents
# agent.callbacks = [safety_callback]
# runtime.evaluate(criteria=[rank_improvement, content_quality, competitor_gap, update_success, content_uniqueness, keyword_density, natural_language, update_frequency])