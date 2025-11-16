#!/usr/bin/env python3
"""Test script to verify Level 3 AI orchestrator parallel execution"""

import time
import threading
from agents.level3_ai_orchestrator import Level3AIOrchestrator

def test_parallel_execution():
    """Test the parallel optimization execution"""
    print("Testing Level 3 AI Orchestrator parallel execution...")

    orchestrator = Level3AIOrchestrator()

    # Test just the parallel optimization part
    print("Running parallel optimizations...")

    # Create mock intelligence data
    intelligence = {
        "seo_monitoring": {"rows": [{"position": 15, "keyword": "junk removal Vilnius"}]},
        "competitor_analysis": {"content_gaps": ["eco-friendly disposal tips"]},
        "market_intelligence": {"trends": ["sustainability", "local SEO"]}
    }

    # Create mock strategy
    strategy = {
        "primary_objectives": ["Improve rankings", "Generate content"],
        "tactical_approaches": ["Content creation", "SEO optimization"]
    }

    start_time = time.time()
    try:
        optimizations = orchestrator._execute_parallel_optimizations(strategy)
        execution_time = time.time() - start_time

        print(f"Parallel execution completed in {execution_time:.2f} seconds")
        print(f"Optimizations keys: {list(optimizations.keys())}")

        # Check if website updates were applied
        if "website_updates" in optimizations:
            print(f"Website updates: {len(optimizations['website_updates'])} items")
            for key, value in optimizations["website_updates"].items():
                print(f"  {key}: {value}")
        else:
            print("No website updates found!")

        return True

    except Exception as e:
        print(f"Parallel execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_parallel_execution()