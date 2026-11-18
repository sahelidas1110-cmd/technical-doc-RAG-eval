import hashlib
import logging

from collections import defaultdict
from pathlib import PurePosixPath

from langchain_chroma import Chroma

from src.config import (
    CHROMA_DB_DIR,
    CHROMA_COLLECTION_NAME
)

from src.embeddings import get_embedding_model


logger = logging.getLogger(__name__)


# --------------------------------------------------
# NORMALIZE SOURCE PATHS
# --------------------------------------------------

def normalize_source_path(source):

    if not source:
        return ""

    return PurePosixPath(
        str(source).replace("\\", "/")
    ).as_posix()


# --------------------------------------------------
# GENERATE DETERMINISTIC CHUNK IDS
# --------------------------------------------------

def generate_chunk_ids(chunks):

    ids = []

    for index, chunk in enumerate(chunks):

        source = normalize_source_path(
            chunk.metadata.get("source")
        )

        if not source:
            raise ValueError(
                "Every chunk must contain source metadata."
            )

        chunk_index = chunk.metadata.get(
            "chunk_index",
            index
        )

        content_hash = hashlib.sha256(
            chunk.page_content.encode("utf-8")
        ).hexdigest()

        unique_string = (
            f"{source}_{chunk_index}_{content_hash}"
        )

        chunk_id = hashlib.sha256(
            unique_string.encode("utf-8")
        ).hexdigest()

        ids.append(chunk_id)

    return ids


# --------------------------------------------------
# CREATE OR LOAD VECTOR STORE
# --------------------------------------------------

def get_vector_store():

    embeddings = get_embedding_model()

    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )


# --------------------------------------------------
# SYNCHRONIZE VECTOR STORE
# --------------------------------------------------

def create_vector_store(chunks, source_files=None):

    vector_store = get_vector_store()

    if source_files is not None:

        active_sources = {
            normalize_source_path(source)
            for source in source_files
        }

    else:
        active_sources = None

    if not chunks and active_sources is None:
        logger.warning(
            "No ingestion data supplied. "
            "Existing collection was not modified."
        )
        return vector_store

    # Group chunks by source

    chunks_by_source = defaultdict(list)

    for chunk in chunks:

        source = normalize_source_path(
            chunk.metadata.get("source")
        )

        if not source:
            raise ValueError(
                "Every chunk must contain source metadata."
            )

        chunks_by_source[source].append(chunk)

    if active_sources is None:

        active_sources = set(chunks_by_source.keys())

    elif set(chunks_by_source.keys()) - active_sources:

        raise ValueError(
            "Chunk sources do not match source_files."
        )

    # Generate deterministic IDs

    all_chunks = []
    all_ids = []

    for source_chunks in chunks_by_source.values():

        ids = generate_chunk_ids(source_chunks)

        all_chunks.extend(source_chunks)
        all_ids.extend(ids)

    if len(all_ids) != len(set(all_ids)):
        raise ValueError(
            "Duplicate chunk IDs detected."
        )

    # Retrieve existing ChromaDB records

    existing_records = vector_store.get(
        include=["metadatas"]
    )

    existing_ids = existing_records.get("ids", [])

    existing_metadatas = existing_records.get(
        "metadatas", []
    )

    existing_by_source = defaultdict(set)

    for record_id, metadata in zip(
        existing_ids,
        existing_metadatas
    ):

        if metadata and metadata.get("source"):

            source = normalize_source_path(
                metadata["source"]
            )

            existing_by_source[source].add(record_id)

    existing_id_set = set(existing_ids)

    # Identify current chunk IDs by source

    new_ids_by_source = defaultdict(set)

    for chunk, chunk_id in zip(all_chunks, all_ids):

        source = normalize_source_path(
            chunk.metadata["source"]
        )

        new_ids_by_source[source].add(chunk_id)

    # Identify stale chunks

    stale_ids = []

    for source in active_sources:

        old_ids = existing_by_source.get(
            source, set()
        )

        current_ids = new_ids_by_source.get(
            source, set()
        )

        stale_ids.extend(
            old_ids - current_ids
        )

    # Delete stale chunks

    if stale_ids:

        vector_store.delete(ids=stale_ids)

        logger.info(
            "Deleted stale chunks: %d",
            len(stale_ids)
        )

    # Identify new chunks

    documents_to_add = []
    ids_to_add = []

    unchanged_count = 0

    for chunk, chunk_id in zip(all_chunks, all_ids):

        if chunk_id in existing_id_set:

            unchanged_count += 1

        else:

            documents_to_add.append(chunk)
            ids_to_add.append(chunk_id)

    # Add new chunks only

    if documents_to_add:

        vector_store.add_documents(
            documents=documents_to_add,
            ids=ids_to_add
        )

    # Synchronization summary

    logger.info(
        "New chunks added: %d",
        len(documents_to_add)
    )

    logger.info(
        "Unchanged chunks skipped: %d",
        unchanged_count
    )

    logger.info(
        "Stale chunks deleted: %d",
        len(stale_ids)
    )

    logger.info(
        "Vector store synchronization completed."
    )

    return vector_store