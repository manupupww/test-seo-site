import os
import re
from typing import List, Dict, Set
import requests

class VoiceSearchOptimizer:
    """Voice search optimization for local SEO"""

    def __init__(self):
        self.question_starters = [
            "kas", "kaip", "kur", "kada", "kodėl", "kiek", "ar",
            "what", "how", "where", "when", "why", "how much", "is",
            "who", "which", "can", "do", "does", "are", "will"
        ]

        self.location_modifiers = [
            "Vilniuje", "Vilnius", "šalia", "arti", "netoli",
            "in Vilnius", "near", "close to", "around"
        ]

        self.intent_keywords = {
            "informational": ["kaip", "kodėl", "kas yra", "how", "why", "what is"],
            "commercial": ["geriausias", "rekomenduoju", "best", "recommend"],
            "transactional": ["užsakyti", "pirkti", "skambinti", "book", "buy", "call"],
            "local": ["arti", "šalia", "netoli", "near", "close", "around"]
        }

    def generate_voice_search_keywords(self, base_keywords: List[str], location: str = "Vilnius") -> List[str]:
        """Generate voice search optimized keywords"""
        voice_keywords = []

        for keyword in base_keywords:
            # Add question-based keywords
            for starter in self.question_starters:
                voice_keywords.extend([
                    f"{starter} {keyword}",
                    f"{starter} {keyword} {location}",
                    f"{starter} rasti {keyword}",
                    f"{starter} geriausias {keyword}"
                ])

            # Add location-based voice queries
            for modifier in self.location_modifiers:
                voice_keywords.extend([
                    f"{keyword} {modifier}",
                    f"kur {keyword} {modifier}",
                    f"geriausias {keyword} {modifier}"
                ])

            # Add conversational phrases
            voice_keywords.extend([
                f"aš ieškau {keyword}",
                f"man reikia {keyword}",
                f"kur galima rasti {keyword}",
                f"rekomenduokite {keyword}",
                f"koks yra geriausias {keyword}"
            ])

        # Remove duplicates and filter
        unique_keywords = list(set(voice_keywords))
        return [kw for kw in unique_keywords if self._is_voice_search_friendly(kw)]

    def _is_voice_search_friendly(self, keyword: str) -> bool:
        """Check if keyword is suitable for voice search"""
        # Voice queries are typically longer (3+ words)
        word_count = len(keyword.split())
        if word_count < 3:
            return False

        # Should contain question words or conversational phrases
        has_question = any(starter in keyword.lower() for starter in self.question_starters)
        has_conversational = any(phrase in keyword.lower() for phrase in [
            "ieškau", "reikia", "norėčiau", "galite", "padėti"
        ])

        return has_question or has_conversational or word_count >= 4

    def optimize_content_for_voice(self, content: str, keywords: List[str]) -> str:
        """Optimize existing content for voice search"""
        optimized_content = content

        # Add FAQ sections
        faq_section = self._generate_faq_section(keywords)
        if faq_section:
            optimized_content += "\n\n" + faq_section

        # Add conversational elements
        conversational_section = self._generate_conversational_section(keywords)
        if conversational_section:
            optimized_content += "\n\n" + conversational_section

        # Add local intent content
        local_section = self._generate_local_intent_section(keywords)
        if local_section:
            optimized_content += "\n\n" + local_section

        return optimized_content

    def _generate_faq_section(self, keywords: List[str]) -> str:
        """Generate FAQ section for voice search"""
        faq_items = []

        for keyword in keywords[:3]:  # Limit to top 3 keywords
            faq_items.extend([
                f"**Kas yra {keyword}?**\n{keyword.title()} - tai profesionalios atliekų tvarkymo paslaugos Vilniuje.",
                f"**Kaip rasti {keyword} Vilniuje?**\nMūsų komanda teikia {keyword} paslaugas visame Vilniuje.",
                f"**Kodėl pasirinkti {keyword}?**\nMes siūlome ekologišką ir patikimą {keyword} sprendimą."
            ])

        if faq_items:
            return "## Dažnai Užduodami Klausimai\n\n" + "\n\n".join(faq_items[:6])
        return ""

    def _generate_conversational_section(self, keywords: List[str]) -> str:
        """Generate conversational content"""
        return f"""## Mūsų Pokalbiai su Klientais

**"Aš ieškau patikimo sprendimo atliekų išvežimui"**
Mūsų komanda padės rasti geriausią sprendimą jūsų poreikiams.

**"Man reikia greitos pagalbos su junk removal"**
Siūlome same-day paslaugas kritiniais atvejais.

**"Kur galima rasti ekologišką atliekų tvarkymą Vilniuje?"**
Mes esame jūsų vietiniai ekspertai ekologiško atliekų šalinimo srityje."""

    def _generate_local_intent_section(self, keywords: List[str]) -> str:
        """Generate local intent content"""
        return """## Vietinės Paslaugos Vilniuje

### Aptarnavimo Teritorija
- **Vilniaus miestas** - viso miesto teritorija
- **Priemiesčiai** - Trakai, Elektrėnai, Šalčininkai
- **Verslo rajonai** - biurų kompleksai, prekybos centrai

### Vietiniai Privalumai
- **Greitas atvykimas** - dažnai tą pačią dieną
- **Vietiniai specialistai** - pažįstantys miesto specifiką
- **Lokalus požiūris** - suprantame Vilniaus gyventojų poreikius

### Susisiekite Su Mumis
📞 **+370-600-12345**
📍 **Gedimino pr. 1, Vilnius**
🕒 **I-V 8:00-18:00, VI 9:00-16:00**"""

    def analyze_voice_search_opportunity(self, current_keywords: List[str]) -> Dict:
        """Analyze voice search optimization opportunities"""
        voice_keywords = self.generate_voice_search_keywords(current_keywords)

        return {
            "current_keywords": current_keywords,
            "voice_optimized_keywords": voice_keywords[:20],  # Top 20
            "opportunity_score": len(voice_keywords) / max(len(current_keywords), 1),
            "recommendations": [
                "Add FAQ sections to improve voice search visibility",
                "Use conversational language in content",
                "Optimize for question-based queries",
                "Add local intent modifiers",
                "Create voice-search friendly content structure"
            ],
            "implementation_priority": "high" if len(voice_keywords) > len(current_keywords) * 2 else "medium"
        }

    def get_featured_snippet_opportunities(self, content: str) -> List[str]:
        """Identify content that could appear in featured snippets"""
        opportunities = []

        # Look for question patterns
        questions = re.findall(r'[A-Z][^.!?]*\?', content)
        if questions:
            opportunities.append(f"Found {len(questions)} questions that could become featured snippets")

        # Look for list patterns
        lists = re.findall(r'\d+\.\s+[A-Z][^.!?]*', content)
        if lists:
            opportunities.append(f"Found {len(lists)} list items suitable for featured snippets")

        # Look for table data
        if '|' in content and '---' in content:
            opportunities.append("Content contains table data - good for featured snippets")

        return opportunities

# Usage example:
# voice_optimizer = VoiceSearchOptimizer()
# voice_keywords = voice_optimizer.generate_voice_search_keywords(["junk removal", "atliekų išvežimas"])
# optimized_content = voice_optimizer.optimize_content_for_voice("Original content", voice_keywords)
# analysis = voice_optimizer.analyze_voice_search_opportunity(["junk removal Vilnius"])