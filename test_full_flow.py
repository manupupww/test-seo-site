from agents.content_generator import ContentGeneratorAgent
from tools.website_api_tool import WebsiteAPITool

print("Testing full content generation and website update flow...")

# Generate content
generator = ContentGeneratorAgent()
result = generator.generate_content(
    keywords=["junk removal", "Vilnius"],
    geo="Vilnius",
    content_type="blog_post",
    target_audience="local_businesses"
)

print("Content generation completed")
print(f"Result keys: {list(result.keys())}")

if "primary_content" in result:
    print("Primary content found, creating blog post...")

    # Create website update
    website_tool = WebsiteAPITool()
    blog_result = website_tool.create_blog_post(
        title="Expert SEO Guide: junk removal Vilnius",
        content=result["primary_content"],
        keywords=["junk removal", "Vilnius", "atliekų išvežimas"],
        category="seo"
    )

    print(f"Blog post creation status: {blog_result.get('status', 'unknown')}")

    # Check if file was created
    import os
    if blog_result.get("filepath") and os.path.exists(blog_result["filepath"]):
        print(f"SUCCESS: Blog post file created at {blog_result['filepath']}")
        with open(blog_result["filepath"], 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"File content length: {len(content)} characters")
            print("File content preview (first 100 ASCII chars):")
            safe_content = content.encode('ascii', 'ignore').decode('ascii')
            print(safe_content[:100] + "..." if len(safe_content) > 100 else safe_content)
    else:
        print("ERROR: Blog post file was not created")
        print(f"Blog result details: status={blog_result.get('status')}, filepath={blog_result.get('filepath')}")

else:
    print("ERROR: No primary_content in result")

print("Test completed.")