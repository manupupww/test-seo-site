from tools.social_media_tool import SocialMediaTool

class SocialMediaAgent:
    def __init__(self, api_key):
        self.tool = SocialMediaTool(api_key)

    def post_blog_update(self, blog_title, blog_url):
        content = f"New blog post: {blog_title} - Check it out at {blog_url} #SEO #Vilnius"
        result = self.tool.post_update(content)
        return result

# Usage: agent = SocialMediaAgent("key"); agent.post_blog_update("Title", "url")