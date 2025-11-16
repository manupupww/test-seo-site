from agents.content_generator import ContentGeneratorAgent

print("Testing just content generation...")

try:
    generator = ContentGeneratorAgent()
    print("ContentGeneratorAgent initialized")

    result = generator.generate_content(
        keywords=["test"],
        geo="test",
        content_type="blog_post",
        target_audience="test"
    )

    print("Content generation completed successfully")
    print(f"Result type: {type(result)}")
    print(f"Has primary_content: {'primary_content' in result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Test finished")