from agents.seo_agent import get_agent

def run():
    agent = get_agent()
    url = "https://manupupww.github.io/test-seo-site/"
    user_prompt = (
        f"Analyze the following website for SEO and suggest the most important improvements:\nURL: {url}\n"
    )
    messages = [{"role": "user", "content": user_prompt}]
    result = agent.invoke({"messages": messages})
    print("\nSEO Analysis Report:\n")
    print(result["content"])

if __name__ == "__main__":
    run()