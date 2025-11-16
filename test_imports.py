print("Starting test...")

try:
    from agents.content_generator import ContentGeneratorAgent
    print("ContentGeneratorAgent imported")
except Exception as e:
    print(f"ContentGeneratorAgent import failed: {e}")

try:
    from tools.website_api_tool import WebsiteAPITool
    print("WebsiteAPITool imported")
except Exception as e:
    print(f"WebsiteAPITool import failed: {e}")

print("Basic imports completed")

try:
    website_tool = WebsiteAPITool()
    print("WebsiteAPITool initialized")
except Exception as e:
    print(f"WebsiteAPITool init failed: {e}")

print("Test completed")