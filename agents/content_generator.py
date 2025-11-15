from chains.generation_chain import create_generation_chain
from chains.rag_chain import create_rag_chain

class ContentGeneratorAgent:
    def __init__(self):
        self.gen_chain = create_generation_chain()
        self.rag_chain = create_rag_chain()

    def generate_content(self, keywords, geo):
        analysis = self.rag_chain.run("SEO analysis for junk removal")
        content = self.gen_chain.run(
            documents=[{"page_content": analysis}],
            keywords=keywords,
            geo=geo
        )
        return content