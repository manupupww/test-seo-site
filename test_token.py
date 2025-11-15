import os
import requests
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    print("No GITHUB_TOKEN in .env")
    exit()

# Test basic access
test_url = "https://api.github.com/user"
headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
response = requests.get(test_url, headers=headers)
print(f"Basic access: {response.status_code}")
if response.status_code != 200:
    print("Token invalid")
    exit()

# Test repo access
repo_url = "https://api.github.com/repos/manupupww/test-seo-site"
response = requests.get(repo_url, headers=headers)
print(f"Repo access: {response.status_code}")

# Test write permission (try to get contents)
contents_url = "https://api.github.com/repos/manupupww/test-seo-site/contents/README.md"
response = requests.get(contents_url, headers=headers)
print(f"Contents read: {response.status_code}")

# Test write (simulate PUT)
# Note: This will fail if no permission, but shows the issue
put_url = "https://api.github.com/repos/manupupww/test-seo-site/contents/test.txt"
data = {"message": "Test", "content": "dGVzdA=="}  # base64 "test"
response = requests.put(put_url, json=data, headers=headers)
print(f"Write test: {response.status_code} - {response.json().get('message', 'OK')}")

print("If write test is 403, fix token permissions.")