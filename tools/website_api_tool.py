import requests

class WebsiteAPITool:
    def __init__(self, api_url, api_key):
        self.api_url = api_url  # GitHub API URL
        self.api_key = api_key
        self.headers = {"Authorization": f"token {api_key}", "Accept": "application/vnd.github.v3+json"}

    def _run(self, action: str, data: dict):
        if action == "upload_blog":
            # GitHub API to create file
            import base64
            content_b64 = base64.b64encode(data['content'].encode()).decode()
            payload = {
                "message": "Add new blog post",
                "content": content_b64
            }
            response = requests.put(f"{self.api_url}/contents/_posts/{data['filename']}", json=payload, headers=self.headers)
            return response.json()
        else:
            return "Invalid action"

# Usage: tool = WebsiteAPITool(api_url="https://api.github.com/repos/owner/repo", api_key="token")