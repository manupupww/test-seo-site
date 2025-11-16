from agents.content_generator import ContentGeneratorAgent

print("Testing content generator...")

generator = ContentGeneratorAgent()
result = generator.generate_content(
    keywords=["junk removal", "Vilnius"],
    geo="Vilnius",
    content_type="blog_post",
    target_audience="local_businesses"
)

print("Content generation result:")
print(f"Type: {type(result)}")
if isinstance(result, dict):
    print(f"Keys: {list(result.keys())}")
    if "primary_content" in result:
        print(f"Content length: {len(result['primary_content'])}")
        print("Content preview:")
        print(result['primary_content'][:200] + "...")
else:
    print(f"Result: {result[:200] if isinstance(result, str) else result}")

print("Test completed.")