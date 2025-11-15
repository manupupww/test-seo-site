from langchain.chains import SimpleSequentialChain

def seo_analysis_chain(agent_tools):
    # Define a chain of steps for SEO: fetch_html → extract_title/meta/h1 → LLM
    return SimpleSequentialChain(chains=agent_tools)