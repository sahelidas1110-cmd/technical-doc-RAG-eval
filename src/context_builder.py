def build_context(retrieved_documents):
    """
    Combine retrieved document chunks into a numbered context.
    """

    context_parts = []

    for index, (doc, score) in enumerate(retrieved_documents, start=1):

        source = doc.metadata.get("source", "Unknown source")

        content = doc.page_content

        context_part = f"""
[Source {index}]
File: {source}

Content:
{content}
"""

        context_parts.append(context_part)

    context = "\n\n---\n\n".join(context_parts)

    return context