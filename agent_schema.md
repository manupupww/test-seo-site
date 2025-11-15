# Agent Architecture Schema (ADK + LangChain Integration)

## Mermaid Diagram Code
```mermaid
graph TD
    A[Orchestrator Agent<br/>ADK LLM + LangChain Chain] --> B[Rank Checker Agent<br/>ADK Loop + LangChain Tool]
    A --> C[SEO Generator Agent<br/>ADK LLM + LangChain RAG]
    A --> D[Blog Uploader Agent<br/>ADK Tool + LangChain API]
    A --> E[Safety Agent<br/>ADK + LangChain Callbacks]
    
    B --> F[Geo Search Tool<br/>ADK + LangChain Retrieval]
    C --> G[Firecrawl Tool<br/>LangChain Loader]
    D --> H[GitHub Tool<br/>LangChain Integration]
    
    F --> I[Global SERP Check<br/>LangChain Web Search]
    F --> J[Local/Geo SERP Check<br/>LangChain Geo Params]
    
    C --> K[Gemini Model<br/>LangChain Integration]
    E --> L[Logging & Evaluation<br/>ADK + LangChain Tracing]
    
    M[LangChain Memory<br/>State Persistence] --> A
    M --> C
```

## ASCII Diagram
```
Orchestrator Agent (ADK LLM + LangChain Chain)
    |--- LangChain Memory (State)
    |
    +-- Rank Checker Agent (ADK Loop + LangChain Tool)
    |   +-- Geo Search Tool (ADK + LangChain Retrieval)
    |       +-- Global SERP Check (LangChain Web Search)
    |       +-- Local/Geo SERP Check (LangChain Geo Params)
    |
    +-- SEO Generator Agent (ADK LLM + LangChain RAG)
    |   +-- Firecrawl (LangChain Loader)
    |   +-- Gemini (LangChain Integration)
    |
    +-- Blog Uploader Agent (ADK Tool + LangChain API)
    |   +-- GitHub (LangChain Integration)
    |
    +-- Safety Agent (ADK + LangChain Callbacks)
        +-- Logging/Eval (ADK + LangChain Tracing)
```

This schema visualizes the hybrid ADK + LangChain agent2agent flow for automated SEO and blog management.</content>
<parameter name="filePath">C:\Users\Mr. Perfect\coffeeproject\agent_schema.md