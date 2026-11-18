from src.document_loader import (
    load_documents,
    clean_documents
)

from src.text_splitter import split_documents

from src.vector_store import create_vector_store


def run_ingestion():

    print("Step 1: Loading documents...")

    documents = load_documents()

    print(f"Loaded documents: {len(documents)}")

    if not documents:
        raise ValueError("No supported documents found.")

    print("Step 2: Cleaning documents...")

    cleaned_docs = clean_documents(documents)

    print(f"Cleaned documents: {len(cleaned_docs)}")

    print("Step 3: Splitting documents into chunks...")

    chunks = split_documents(cleaned_docs)

    print(f"Total chunks generated: {len(chunks)}")

    print("Step 4: Creating embeddings and storing in ChromaDB...")

    vector_store = create_vector_store(chunks)

    print("Step 5: Ingestion completed successfully!")

    print(f"Vector database: {vector_store}")

    return vector_store


if __name__ == "__main__":
    run_ingestion()