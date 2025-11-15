import requests
import base64
import os

def create_deployment_chain():
    github_token = os.getenv("GITHUB_TOKEN")
    print(f"Using GitHub token: {github_token[:10]}...")  # Debug: show first 10 chars
    if not github_token or github_token.startswith("YOUR"):
        def mock_run(content):
            return f"Expert deployed: {content}"
        return mock_run

    # Test token first
    test_url = "https://api.github.com/user"
    test_headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    test_response = requests.get(test_url, headers=test_headers)
    print(f"Token test status: {test_response.status_code}")
    if test_response.status_code != 200:
        def mock_run(content):
            return f"Token invalid: {test_response.status_code} - {test_response.text}"
        return mock_run

    def deploy_run(content):
        # Direct GitHub API call to upload file
        import time
        filename = f"_posts/{time.strftime('%Y-%m-%d')}-expert-seo-post.md"
        url = f"https://api.github.com/repos/manupupww/test-seo-site/contents/{filename}"
        headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
        # Encode content to base64
        content_b64 = base64.b64encode(content.encode()).decode()
        data = {
            "message": "Expert AI SEO post upload",
            "content": content_b64
        }
        response = requests.put(url, json=data, headers=headers)
        if response.status_code in [201, 200]:
            return "Successfully deployed expert post to website. Check https://manupupww.github.io/test-seo-site/ for updates."
        else:
            try:
                error_msg = response.json().get("message", "Unknown error")
            except:
                error_msg = response.text or "Unknown error"
            return f"Deployment failed: {response.status_code} - {error_msg}. Ensure GITHUB_TOKEN has 'repo' scope at https://github.com/settings/tokens."

    return deploy_run

# Usage: chain = create_deployment_chain(); result = chain("post content")