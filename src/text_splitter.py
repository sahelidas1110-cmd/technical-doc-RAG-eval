import logging

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from src.config import CHUNK_SIZE, CHUNK_OVERLAP


logger = logging.getLogger(__name__)


# --------------------------------------------------
# TEXT SPLITTING
# --------------------------------------------------

def split_documents(documents):

    if not documents:
        logger.warning("No documents received for splitting.")
        return []

    # Validate chunk configuration

    if CHUNK_SIZE <= 0:
        raise ValueError("CHUNK_SIZE must be greater than zero.")

    if CHUNK_OVERLAP < 0:
        raise ValueError("CHUNK_OVERLAP cannot be negative.")

    if CHUNK_OVERLAP >= CHUNK_SIZE:
        raise ValueError(
            "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
        )

    # Initialize recursive text splitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            " ",
            ""
        ],
        add_start_index=True,
        strip_whitespace=True
    )

    # Split documents while preserving metadata

    chunks = splitter.split_documents(documents)

    # Add a sequential chunk index for each source document

    source_chunk_counts = {}

    for chunk in chunks:

        source = chunk.metadata.get(
            "source",
            "unknown"
        )

        chunk_index = source_chunk_counts.get(source, 0)

        chunk.metadata["chunk_index"] = chunk_index

        source_chunk_counts[source] = chunk_index + 1

    logger.info(
        "Document splitting completed. "
        "Input documents: %d | Generated chunks: %d",
        len(documents),
        len(chunks)
    )

    return chunks