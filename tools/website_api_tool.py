import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests

class WebsiteAPITool:
    """Advanced Website API Tool for autonomous site management"""

    def __init__(self, repo_owner: str = None, repo_name: str = None, github_token: str = None):
        self.repo_owner = repo_owner or "manupupww"
        self.repo_name = repo_name or "test-seo-site"
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.base_path = os.getcwd()  # Local repository path
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"

        if self.github_token:
            self.headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
        else:
            self.headers = {"Accept": "application/vnd.github.v3+json"}

    def create_blog_post(self, title: str, content: str, keywords: List[str], category: str = "seo") -> Dict[str, Any]:
        """Create a new blog post in Jekyll format"""
        # Generate filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = title.lower().replace(" ", "-").replace("?", "").replace("!", "")
        filename = f"{date_str}-expert-seo-post.md"

        # Create Jekyll frontmatter
        frontmatter = f"""---
layout: post
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")}
categories: {category}
tags: {', '.join(keywords)}
description: "Expert SEO analysis and optimization guide for {', '.join(keywords[:3])}"
keywords: {', '.join(keywords)}
author: AI SEO Agent
---

"""

        # Combine frontmatter and content
        full_content = frontmatter + content

        # Write to local file
        posts_dir = os.path.join(self.base_path, "_posts")
        os.makedirs(posts_dir, exist_ok=True)

        filepath = os.path.join(posts_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
        except UnicodeEncodeError:
            # Fallback to ASCII-safe content
            safe_content = full_content.encode('ascii', 'ignore').decode('ascii')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(safe_content)

        return {
            "status": "success",
            "filename": filename,
            "filepath": filepath,
            "title": title,
            "word_count": len(content.split()),
            "keywords": keywords
        }

    def update_homepage_content(self, new_content: str, section: str = "main") -> Dict[str, Any]:
        """Update homepage content sections"""
        index_path = os.path.join(self.base_path, "index.md")

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                current_content = f.read()

            # Simple content replacement - in real implementation, use more sophisticated parsing
            if section == "main":
                # Replace main content area
                updated_content = current_content.replace(
                    "<!-- MAIN CONTENT START -->",
                    f"<!-- MAIN CONTENT START -->\n{new_content}\n"
                )
            else:
                # Append to end
                updated_content = current_content + f"\n\n## {section.title()}\n{new_content}"

            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            return {"status": "success", "section": section, "updated": True}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def generate_faq_content(self, keywords: List[str], industry: str = "junk removal") -> Dict[str, Any]:
        """Generate comprehensive FAQ content"""
        faq_items = []

        for keyword in keywords[:5]:  # Limit to 5 main keywords
            faq_items.extend([
                {
                    "question": f"Kas yra {keyword} paslaugos?",
                    "answer": f"{keyword.title()} paslaugos apima profesionalų atliekų surinkimą, rūšiavimą ir utilizavimą. Mes užtikriname ekologišką ir saugų procesą."
                },
                {
                    "question": f"Kiek kainuoja {keyword}?",
                    "answer": f"{keyword.title()} kainos priklauso nuo atliekų kiekio ir tipo. Bazinės paslaugos kainuoja nuo €50. Susisiekite dėl asmeninio įkainojimo."
                },
                {
                    "question": f"Kaip užsakyti {keyword} paslaugas?",
                    "answer": f"Užsisakyti {keyword} paslaugas galite telefonu arba internetu. Mes dirbame 24/7 ir atvykstame per 2-4 valandas."
                }
            ])

        # Format as Markdown
        faq_content = "# Dažnai Užduodami Klausimai\n\n"
        for i, faq in enumerate(faq_items[:10], 1):  # Limit to 10 questions
            faq_content += f"## {i}. {faq['question']}\n\n{faq['answer']}\n\n"

        # Write to faq.md
        faq_path = os.path.join(self.base_path, "faq.md")
        try:
            with open(faq_path, 'w', encoding='utf-8') as f:
                f.write(faq_content)
        except UnicodeEncodeError:
            # Fallback to ASCII-safe content
            safe_content = faq_content.encode('ascii', 'ignore').decode('ascii')
            with open(faq_path, 'w', encoding='utf-8') as f:
                f.write(safe_content)

        return {
            "status": "success",
            "filename": "faq.md",
            "questions_count": len(faq_items[:10]),
            "keywords_covered": keywords[:5]
        }

    def update_site_config(self, new_keywords: List[str], new_description: str = None) -> Dict[str, Any]:
        """Update Jekyll site configuration with new SEO keywords"""
        config_path = os.path.join(self.base_path, "_config.yml")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()

            # Add new keywords to existing ones
            if 'keywords:' in config_content:
                # Find existing keywords line and append
                lines = config_content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('keywords:'):
                        current_keywords = line.split(':', 1)[1].strip()
                        if current_keywords:
                            new_keywords_str = f"{current_keywords}, {', '.join(new_keywords)}"
                        else:
                            new_keywords_str = ', '.join(new_keywords)
                        lines[i] = f"keywords: {new_keywords_str}"
                        break
            else:
                # Add keywords section
                lines = config_content.split('\n')
                lines.append(f"keywords: {', '.join(new_keywords)}")

            # Update description if provided
            if new_description:
                for i, line in enumerate(lines):
                    if line.strip().startswith('description:'):
                        lines[i] = f"description: {new_description}"
                        break

            updated_config = '\n'.join(lines)

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(updated_config)

            return {"status": "success", "config_updated": True, "keywords_added": new_keywords}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def add_schema_markup(self, page_type: str = "local_business") -> Dict[str, Any]:
        """Add structured data markup to pages"""
        schema_templates = {
            "local_business": {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": "Expert Junk Removal Services",
                "description": "Professional junk removal and disposal services in Vilnius",
                "url": "https://your-domain.com",
                "telephone": "+370-600-12345",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Gedimino pr. 1",
                    "addressLocality": "Vilnius",
                    "postalCode": "01103",
                    "addressCountry": "LT"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 54.6872,
                    "longitude": 25.2797
                },
                "openingHours": "Mo-Su 08:00-18:00",
                "priceRange": "€€"
            }
        }

        if page_type in schema_templates:
            schema_json = json.dumps(schema_templates[page_type], indent=2, ensure_ascii=False)

            # Add to layout or specific page
            layout_path = os.path.join(self.base_path, "_layouts", "default.html")

            try:
                with open(layout_path, 'r', encoding='utf-8') as f:
                    layout_content = f.read()

                # Add schema markup in head section
                if '<head>' in layout_content and '</head>' in layout_content:
                    schema_script = f'\n<script type="application/ld+json">\n{schema_json}\n</script>\n'
                    layout_content = layout_content.replace('</head>', f'{schema_script}</head>')

                    with open(layout_path, 'w', encoding='utf-8') as f:
                        f.write(layout_content)

                    return {"status": "success", "schema_added": page_type}

            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "error", "message": f"Unknown page type: {page_type}"}

    def get_website_metrics(self) -> Dict[str, Any]:
        """Get current website statistics"""
        try:
            posts_count = len([f for f in os.listdir(os.path.join(self.base_path, "_posts")) if f.endswith('.md')])
            pages_count = len([f for f in os.listdir(self.base_path) if f.endswith('.md')])

            return {
                "status": "success",
                "blog_posts": posts_count,
                "pages": pages_count,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def commit_changes(self, message: str = None) -> Dict[str, Any]:
        """Commit all changes to Git"""
        if not message:
            message = f"AI Agent SEO Optimization - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        try:
            import subprocess

            # Add all changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True)

            # Commit
            result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)

            if result.returncode == 0:
                # Push to GitHub
                push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)

                return {
                    "status": "success",
                    "commit_message": message,
                    "push_success": push_result.returncode == 0,
                    "push_output": push_result.stdout if push_result.returncode == 0 else push_result.stderr
                }
            else:
                return {"status": "error", "message": "Nothing to commit"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

# Usage examples:
# tool = WebsiteAPITool()
# tool.create_blog_post("SEO Title", "Content here", ["keyword1", "keyword2"])
# tool.generate_faq_content(["junk removal", "disposal"])
# tool.update_site_config(["new", "keywords"])
# tool.commit_changes("AI optimization update")