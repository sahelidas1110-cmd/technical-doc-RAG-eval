import hashlib

from langchain_chroma import Chroma

from src.config import (
    CHROMA_DB_DIR,
    CHROMA_COLLECTION_NAME
)

from src.embeddings import get_embedding_model


def generate_chunk_ids(chunks):

    ids = []

    for index, chunk in enumerate(chunks):

        source = chunk.metadata.get("source", "")

        content_hash = hashlib.sha256(
            chunk.page_content.encode("utf-8")
        ).hexdigest()

        unique_string = (
            f"{source}_{index}_{content_hash}"
        )

        chunk_id = hashlib.sha256(
            unique_string.encode("utf-8")
        ).hexdigest()

        ids.append(chunk_id)

    return ids


def create_vector_store(chunks):

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )

    ids = generate_chunk_ids(chunks)

    vector_store.add_documents(
        documents=chunks,
        ids=ids
    )

    return vector_store