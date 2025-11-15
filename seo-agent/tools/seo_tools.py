from langchain.tools import tool
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

@tool
def fetch_html(url: str) -> str:
    """Fetch raw HTML content of a URL."""
    headers = {"User-Agent": "SEO-AgentBot/1.0"}
    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

@tool
def extract_title(html: str) -> str:
    """Extract the page <title> from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else ""
    return title or "No title found"

@tool
def extract_meta_description(html: str) -> str:
    """Extract the meta description from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        return desc["content"]
    return "No meta description found"

@tool
def extract_h1_tags(html: str) -> str:
    """Extract all H1 tags from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    h1s = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
    return "\n".join(h1s) or "No H1 tags found"