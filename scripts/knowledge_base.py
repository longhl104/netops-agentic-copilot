import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_knowledge_base(docs_path="data/troubleshooting_guides"):
    """
    Builds a FAISS knowledge base from troubleshooting guides.
    """
    documents = []
    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_path, filename)
            with open(filepath, "r") as f:
                documents.append(f.read())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.create_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = FAISS.from_documents(chunked_documents, embeddings)
    vector_db.save_local("faiss_index")
    print("Knowledge base built and saved to faiss_index/")

if __name__ == "__main__":
    # Placeholder for generating mock troubleshooting guides
    # In a real scenario, these would be actual documentation files
    os.makedirs("data/troubleshooting_guides", exist_ok=True)
    with open("data/troubleshooting_guides/bgp_flapping.txt", "w") as f:
        f.write("BGP Route Flapping Troubleshooting Guide: Steps to diagnose and resolve BGP route instability.")
    with open("data/troubleshooting_guides/high_latency.txt", "w") as f:
        f.write("High Latency Diagnosis on Switch X: Identifying and mitigating network latency issues on Cisco Switch X.")

    build_knowledge_base()
