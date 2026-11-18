import logging

from src.document_loader import (
    load_documents,
    clean_documents
)

from src.text_splitter import split_documents

from src.vector_store import create_vector_store


# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# INGESTION PIPELINE
# --------------------------------------------------

def run_ingestion():

    logger.info("Starting RAG ingestion pipeline.")

    # STEP 1: Load documents

    logger.info("Step 1: Loading documents.")

    documents = load_documents()

    logger.info(
        "Total documents loaded: %d",
        len(documents)
    )

    if not documents:
        raise ValueError(
            "No supported documents were loaded."
        )

    # STEP 2: Clean documents

    logger.info("Step 2: Cleaning documents.")

    cleaned_docs = clean_documents(documents)

    logger.info(
        "Documents remaining after cleaning: %d",
        len(cleaned_docs)
    )

    if not cleaned_docs:
        raise ValueError(
            "No valid documents remaining after cleaning."
        )

    # Track successfully loaded source files.
    # This avoids treating a file that failed to load
    # as an empty document during synchronization.

    source_files = sorted({
        doc.metadata["source"]
        for doc in cleaned_docs
        if doc.metadata.get("source")
    })

    if not source_files:
        raise ValueError(
            "No source metadata found in loaded documents."
        )

    # STEP 3: Split documents

    logger.info("Step 3: Splitting documents into chunks.")

    chunks = split_documents(cleaned_docs)

    logger.info(
        "Total chunks generated: %d",
        len(chunks)
    )

    if not chunks:
        raise ValueError(
            "No chunks were generated from the documents."
        )

    # STEP 4: Create embeddings and synchronize ChromaDB

    logger.info(
        "Step 4: Creating embeddings and synchronizing ChromaDB."
    )

    vector_store = create_vector_store(
        chunks=chunks,
        source_files=source_files
    )

    # STEP 5: Completion summary

    logger.info("Ingestion pipeline completed successfully.")

    logger.info(
        "Summary | Loaded documents: %d | "
        "Chunks generated: %d | Source files: %d",
        len(cleaned_docs),
        len(chunks),
        len(source_files)
    )

    return vector_store


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    run_ingestion()