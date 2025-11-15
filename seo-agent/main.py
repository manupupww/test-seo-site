from agents.seo_agent import get_agent

def run():
    agent = get_agent()
    url = "https://manupupww.github.io/test-seo-site/"
    user_prompt = (
        f"Analyze the following website for SEO and suggest the most important improvements:\nURL: {url}\n"
    )

    # For synchronous (non-streaming) agent use:
    result = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
    print("\nSEO Analysis Report:\n")
    print(result["messages"][-1]["content"])

if __name__ == "__main__":
    run()