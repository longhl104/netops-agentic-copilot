from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class RetrievalAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)

    def retrieve_info(self, query: str) -> list:
        """
        Queries the Vector DB to find relevant troubleshooting steps for a specific error.
        """
        print(f"Retrieval Agent querying for: {query}")
        docs = self.vector_db.similarity_search(query, k=2)
        return [doc.page_content for doc in docs]
