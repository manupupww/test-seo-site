import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

class ABTestingFramework:
    """A/B Testing framework for content optimization"""

    def __init__(self, test_data_file: str = "ab_tests.json"):
        self.test_data_file = test_data_file
        self.tests = self._load_tests()

    def _load_tests(self) -> Dict:
        """Load existing A/B tests"""
        if os.path.exists(self.test_data_file):
            try:
                with open(self.test_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_tests(self):
        """Save tests to file"""
        try:
            with open(self.test_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tests, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving A/B tests: {e}")

    def create_test(self, test_id: str, page_url: str, element_type: str,
                   variant_a: Dict, variant_b: Dict, traffic_split: float = 0.5) -> Dict:
        """Create a new A/B test"""

        test = {
            "test_id": test_id,
            "page_url": page_url,
            "element_type": element_type,  # "title", "description", "content", "cta"
            "variants": {
                "A": variant_a,
                "B": variant_b
            },
            "traffic_split": traffic_split,  # 0.5 = 50/50 split
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "stats": {
                "A": {"views": 0, "conversions": 0, "ctr": 0},
                "B": {"views": 0, "conversions": 0, "ctr": 0}
            },
            "winner": None,
            "confidence_level": 0
        }

        self.tests[test_id] = test
        self._save_tests()
        return test

    def get_variant_for_user(self, test_id: str, user_id: str = None) -> Tuple[str, Dict]:
        """Get which variant to show for a user (sticky assignment)"""
        if test_id not in self.tests:
            return "A", {}  # Default fallback

        test = self.tests[test_id]
        if test["status"] != "active":
            winner = test.get("winner", "A")
            return winner, test["variants"][winner]

        # Create consistent user assignment using hash
        if not user_id:
            user_id = str(random.randint(1, 1000000))  # Random for anonymous users

        # Use hash to consistently assign users to variants
        hash_value = int(hashlib.md5(f"{test_id}_{user_id}".encode()).hexdigest()[:8], 16)
        normalized_hash = hash_value / 2**32  # Normalize to 0-1

        variant = "A" if normalized_hash < test["traffic_split"] else "B"

        # Record view
        self.record_view(test_id, variant)

        return variant, test["variants"][variant]

    def record_view(self, test_id: str, variant: str):
        """Record that a variant was viewed"""
        if test_id in self.tests:
            self.tests[test_id]["stats"][variant]["views"] += 1
            self._save_tests()

    def record_conversion(self, test_id: str, variant: str):
        """Record that a variant led to conversion"""
        if test_id in self.tests:
            self.tests[test_id]["stats"][variant]["conversions"] += 1
            self._calculate_stats(test_id)
            self._save_tests()

    def _calculate_stats(self, test_id: str):
        """Calculate CTR and confidence intervals"""
        test = self.tests[test_id]
        stats = test["stats"]

        for variant in ["A", "B"]:
            views = stats[variant]["views"]
            conversions = stats[variant]["conversions"]

            if views > 0:
                ctr = conversions / views
                stats[variant]["ctr"] = ctr

        # Simple winner determination (basic statistical significance)
        self._determine_winner(test_id)

    def _determine_winner(self, test_id: str):
        """Determine if there's a statistically significant winner"""
        test = self.tests[test_id]
        stats = test["stats"]

        a_views = stats["A"]["views"]
        b_views = stats["B"]["views"]
        a_conv = stats["A"]["conversions"]
        b_conv = stats["B"]["conversions"]

        # Need minimum sample size for statistical significance
        min_sample = 100
        if a_views < min_sample or b_views < min_sample:
            return

        # Calculate conversion rates
        a_rate = a_conv / a_views if a_views > 0 else 0
        b_rate = b_conv / b_views if b_views > 0 else 0

        # Simple significance test (z-test approximation)
        if abs(a_rate - b_rate) > 0.02:  # 2% difference threshold
            test["winner"] = "A" if a_rate > b_rate else "B"
            test["status"] = "completed"
            test["completed_at"] = datetime.now().isoformat()

    def get_test_results(self, test_id: str) -> Dict:
        """Get comprehensive test results"""
        if test_id not in self.tests:
            return {"error": "Test not found"}

        test = self.tests[test_id]
        return {
            "test_id": test_id,
            "status": test["status"],
            "winner": test.get("winner"),
            "stats": test["stats"],
            "created_at": test["created_at"],
            "completed_at": test.get("completed_at"),
            "recommendation": self._get_recommendation(test)
        }

    def _get_recommendation(self, test: Dict) -> str:
        """Generate recommendation based on test results"""
        if test["status"] != "completed":
            return "Test still running - need more data"

        winner = test["winner"]
        winner_stats = test["stats"][winner]

        return f"Variant {winner} won with {winner_stats['ctr']:.1%} CTR. Implement this variant permanently."

    def get_active_tests(self) -> List[Dict]:
        """Get all active tests"""
        return [test for test in self.tests.values() if test["status"] == "active"]

    def create_content_test(self, page_url: str, content_type: str = "title") -> Dict:
        """Create a content A/B test with AI-generated variants"""
        test_id = f"content_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Mock variants - in real implementation, use AI to generate different versions
        if content_type == "title":
            variant_a = {"title": "Expert Junk Removal Vilnius | Eco-Friendly Disposal Services"}
            variant_b = {"title": "Vilnius Junk Removal - Professional & Affordable Services"}
        elif content_type == "description":
            variant_a = {"description": "Professional junk removal and eco-friendly disposal services in Vilnius. Since 2015 - trusted by 500+ customers."}
            variant_b = {"description": "Fast, reliable junk removal in Vilnius. Eco-friendly disposal, free quotes, same-day service."}
        else:
            variant_a = {"content": "Original content version"}
            variant_b = {"content": "Optimized content version"}

        return self.create_test(test_id, page_url, content_type, variant_a, variant_b)

# Example usage:
# ab_test = ABTestingFramework()
# test = ab_test.create_content_test("/index.html", "title")
# variant, content = ab_test.get_variant_for_user(test["test_id"], "user123")
# ab_test.record_conversion(test["test_id"], variant)