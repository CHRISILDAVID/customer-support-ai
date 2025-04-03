# tools/vector_search_tool.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai.tools import tool  # ✅ Decorator for BaseTool-compatible tools


class VectorSearchTool:
    def __init__(self, persist_directory: str = "embeddings/chroma_db"):
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    @tool("VectorSearchTool")
    def retrieve(self, query: str) -> str:
        """
        Retrieves relevant documents from past tickets or knowledge base based on a query.
        """
        docs = self.retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in docs])