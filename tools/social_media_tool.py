class SocialMediaTool:
    def __init__(self, api_key):
        self.api_key = api_key  # Mock, use real API like Twitter or Facebook

    def post_update(self, content):
        # Mock posting
        print(f"Posted to social media: {content[:100]}...")
        return "Posted successfully"

# Usage: tool = SocialMediaTool("key"); tool.post_update("New blog post!")