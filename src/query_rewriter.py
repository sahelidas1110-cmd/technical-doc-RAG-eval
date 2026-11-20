
import logging

from src.llm import get_chat_model


logger = logging.getLogger(__name__)


# --------------------------------------------------
# QUERY REWRITING
# --------------------------------------------------

def rewrite_query(query: str) -> str:

    if not isinstance(query, str) or not query.strip():
        raise ValueError(
            "Query must be a non-empty string."
        )

    original_query = query.strip()

    llm = get_chat_model()

    prompt = f"""
You are a retrieval query optimization assistant for a
technical documentation search system.

Your goal is to improve retrieval of relevant documentation,
not simply paraphrase the user's question.

Instructions:

1. Preserve the original intent of the question.
2. Identify all distinct technical concepts in the question.
3. Expand important concepts using specific technical terms,
   terminology, metrics, components and synonyms commonly
   used in technical documentation.
4. For questions about evaluation, explicitly include
   relevant evaluation metrics or criteria.
5. For questions about debugging or tracing, explicitly
   include relevant execution evidence, artifacts and
   diagnostic information.
6. Preserve multiple requirements when the question
   contains more than one sub-question.
7. Include relevant terminology without introducing
   unrelated concepts.
8. Do not answer the original question.
9. Do not invent facts.
10. Return a concise but concept-rich search query.
11. Return ONLY the rewritten search query.

Original question:
{original_query}
"""

    response = llm.invoke(prompt)

    rewritten_query = response.content

    if not isinstance(rewritten_query, str):
        raise TypeError(
            "LLM returned an unexpected response format."
        )

    rewritten_query = rewritten_query.strip()

    if not rewritten_query:
        raise ValueError(
            "Query rewriting returned an empty result."
        )

    logger.info(
        "Query rewriting completed successfully."
    )

    return rewritten_query
