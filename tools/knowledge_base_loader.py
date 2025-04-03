# tools/knowledge_base_loader.py

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_vector_db(
    persist_directory: str = "embeddings/chroma_db",
    conversations_dir: str = "data/conversations",
    historical_csv: str = "data/historical/historical_tickets.csv",
    kb_file: str = "data/knowledge_base/knowledge_base.txt"
):
    documents = []

    # Load and split KB file (if exists)
    if os.path.exists(kb_file):
        print(f"🔍 Loading KB: {kb_file}")
        documents += TextLoader(kb_file).load()

    # Load and split all sample conversations
    for filename in os.listdir(conversations_dir):
        if filename.endswith(".txt"):
            path = os.path.join(conversations_dir, filename)
            print(f"📄 Indexing: {filename}")
            documents += TextLoader(path).load()

    # Load historical ticket CSV (if exists)
    if os.path.exists(historical_csv):
        print(f"📊 Loading historical tickets: {historical_csv}")
        documents += CSVLoader(historical_csv).load()

    # Split for embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create vector DB
    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    ).persist()

    print(f"✅ Vector DB created at: {persist_directory}")

if __name__ == "__main__":
    os.makedirs("embeddings/chroma_db", exist_ok=True)
    build_vector_db()
