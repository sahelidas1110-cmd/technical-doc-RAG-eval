
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
You are a query optimization assistant for a
technical documentation retrieval system.

Your task is to reformulate the user's question
into an effective search query for retrieving
relevant technical documentation.

Instructions:
1. Preserve the original intent of the question.
2. Preserve ALL distinct concepts, requirements,
   and sub-questions in the original question.
3. Do not allow one dominant concept to overshadow
   other important concepts in a multi-part question.
4. Identify important technical terminology,
   synonyms, components, and related concepts.
5. Expand each distinct concept where useful,
   using relevant technical terms.
6. For questions involving multiple components,
   ensure the rewritten query gives balanced
   coverage to all components.
7. Do not answer the original question.
8. Do not introduce unrelated concepts or invent
   facts or requirements.
9. Keep the rewritten query concise but sufficiently
   detailed to represent all important concepts.
10. Return ONLY the rewritten search query.
    Do not include explanations, headings or quotes.

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
