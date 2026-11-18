import logging


logger = logging.getLogger(__name__)


# --------------------------------------------------
# CONTEXT BUILDER
# --------------------------------------------------

def build_context(retrieved_documents):

    if not retrieved_documents:
        logger.warning(
            "No retrieved documents provided for context building."
        )
        return ""

    context_parts = []

    for index, (doc, score) in enumerate(
        retrieved_documents,
        start=1
    ):

        metadata = doc.metadata

        source = metadata.get(
            "source",
            "Unknown source"
        )

        category = metadata.get(
            "category",
            "Unknown category"
        )

        chunk_index = metadata.get(
            "chunk_index",
            "Unknown"
        )

        content = doc.page_content.strip()

        if not content:
            continue

        context_part = f"""
[Source {index}]
File: {source}
Category: {category}
Chunk Index: {chunk_index}
Retrieval Distance: {float(score):.4f}

Content:
{content}
"""

        context_parts.append(context_part.strip())

    context = "\n\n---\n\n".join(context_parts)

    logger.info(
        "Context built using %d document chunks.",
        len(context_parts)
    )

    return context