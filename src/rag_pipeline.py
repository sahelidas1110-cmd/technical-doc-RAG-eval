import logging

from langsmith import traceable

from src.retriever import retrieve_documents
from src.context_builder import build_context
from src.prompt_template import get_rag_prompt
from src.llm import get_chat_model
from src.config import MAX_RETRIEVAL_DISTANCE


logger = logging.getLogger(__name__)


# --------------------------------------------------
# RAG ANSWER GENERATION
# --------------------------------------------------

@traceable(
    name="generate_answer",
    tags=["rag", "retrieval", "answer-generation"],
    metadata={
        "pipeline": "technical-doc-RAG-eval",
        "embedding_model": "text-embedding-3-large",
        "chunk_size": 400,
        "chunk_overlap": 80,
        "top_k": 3,
        "retrieval_threshold": 1.05
    }
)
def generate_answer(question: str):

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    question = question.strip()

    logger.info("Starting RAG answer generation.")

    # STEP 1: Retrieve relevant documents

    retrieved_documents = retrieve_documents(
        query=question,
        k=3
    )

    print("=== GENERATE_ANSWER EXECUTED ===")
    print("ACTIVE THRESHOLD:", MAX_RETRIEVAL_DISTANCE)

    for doc, score in retrieved_documents:
        print(
            "RETRIEVAL SCORE:",
            score,
            "| SOURCE:",
            doc.metadata.get("source")
        )

    logger.info(
        "Retrieved %d document chunks.",
        len(retrieved_documents)
    )

    # STEP 2: Filter using retrieval distance threshold

    relevant_documents = [
        (doc, score)
        for doc, score in retrieved_documents
        if score <= MAX_RETRIEVAL_DISTANCE
    ]

    logger.info(
        "Relevant documents after filtering: %d",
        len(relevant_documents)
    )

    # STEP 3: Handle insufficient retrieval results

    if not relevant_documents:

        logger.warning(
            "No relevant documents found for the question."
        )

        return {
            "question": question,
            "answer": (
                "I could not find sufficient information "
                "in the provided documentation."
            ),
            "sources": [],
            "retrieved_documents": retrieved_documents
        }

    # STEP 4: Construct context

    context = build_context(relevant_documents)

    # STEP 5: Prepare source references

    sources = []

    for index, (doc, score) in enumerate(
        relevant_documents,
        start=1
    ):

        sources.append({
            "source_id": index,
            "file": doc.metadata.get(
                "source",
                "Unknown source"
            ),
            "category": doc.metadata.get(
                "category",
                "Unknown category"
            ),
            "chunk_index": doc.metadata.get(
                "chunk_index"
            ),
            "score": float(score)
        })

    # STEP 6: Load RAG prompt

    prompt = get_rag_prompt()

    # STEP 7: Initialize chat model

    llm = get_chat_model()

    # STEP 8: Create RAG chain

    rag_chain = prompt | llm

    # STEP 9: Generate answer

    response = rag_chain.invoke({
        "context": context,
        "question": question
    })

    # STEP 10: Return structured response

    logger.info("RAG answer generated successfully.")

    return {
        "question": question,
        "answer": response.content,
        "sources": sources,
        "retrieved_documents": relevant_documents
    }