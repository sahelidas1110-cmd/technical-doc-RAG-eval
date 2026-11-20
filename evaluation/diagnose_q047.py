
from src.retriever import get_vector_store


EXPECTED_SOURCE = "data/raw/langchain/tools_and_evaluation.md"

QUERY = (
    "A retrieval system returns several relevant documents, "
    "but the first relevant document appears at rank four. "
    "How does Mean Reciprocal Rank (MRR) reflect this result?"
)


def diagnose():

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query=QUERY,
        k=5,
        filter={"source": EXPECTED_SOURCE}
    )

    print("\nMRR SOURCE CHUNK DIAGNOSTIC")
    print("=" * 70)

    if not results:
        print("No chunks found for the expected source.")
        return

    for index, (document, score) in enumerate(results, start=1):

        print(f"\nChunk {index}")
        print(f"Distance: {score:.4f}")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Chunk index: {document.metadata.get('chunk_index')}")

        print("\nChunk content:")
        print("-" * 70)
        print(document.page_content)
        print("-" * 70)


if __name__ == "__main__":
    diagnose()
