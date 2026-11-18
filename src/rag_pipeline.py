from src.retriever import retrieve_documents
from src.context_builder import build_context
from src.prompt_template import get_rag_prompt
from src.llm import get_chat_model
from src.config import MAX_RETRIEVAL_DISTANCE


def generate_answer(question: str):
    """
    Generate an answer using retrieved documentation
    and the OpenAI chat model.
    """

    # Step 1: Retrieve relevant documents
    retrieved_documents = retrieve_documents(
        query=question,
        k=3
    )

    # Step 2: Filter documents using distance threshold
    relevant_documents = [
        (doc, score)
        for doc, score in retrieved_documents
        if score <= MAX_RETRIEVAL_DISTANCE
    ]

    # Step 3: Handle insufficient retrieval results
    if not relevant_documents:
        return {
            "question": question,
            "answer": (
                "I could not find sufficient information "
                "in the provided documentation."
            ),
            "sources": [],
            "retrieved_documents": retrieved_documents
        }

    # Step 4: Construct context using relevant documents only
    context = build_context(relevant_documents)

    # Step 5: Prepare source references
    sources = []

    for index, (doc, score) in enumerate(
        relevant_documents, start=1
    ):
        sources.append({
            "source_id": index,
            "file": doc.metadata.get(
                "source", "Unknown source"
            )
        })

    # Step 6: Load prompt
    prompt = get_rag_prompt()

    # Step 7: Initialize OpenAI LLM
    llm = get_chat_model()

    # Step 8: Connect prompt and LLM
    rag_chain = prompt | llm

    # Step 9: Generate answer
    response = rag_chain.invoke({
        "context": context,
        "question": question
    })

    # Step 10: Return structured response
    return {
        "question": question,
        "answer": response.content,
        "sources": sources,
        "retrieved_documents": relevant_documents
    }