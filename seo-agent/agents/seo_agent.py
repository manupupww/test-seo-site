import yaml
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.seo_tools import fetch_html, extract_title, extract_meta_description, extract_h1_tags

def load_config(path="config/settings.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_agent():
    config = load_config()
    llm_cfg = config["llm"]
    model = ChatOpenAI(
        temperature=llm_cfg.get("temperature", 0.0),
        model=llm_cfg.get("model", "gpt-3.5-turbo")
    )
    seo_tools = [fetch_html, extract_title, extract_meta_description, extract_h1_tags]
    agent = create_agent(model, tools=seo_tools)
    return agent