from src.retriever import retrieve_documents

question = (
    "A retrieval system returns several relevant documents, "
    "but the first relevant document appears at rank four. "
    "How does Mean Reciprocal Rank (MRR) reflect this result?"
)

results = retrieve_documents(query=question, k=3)

print("\nQ047 RETRIEVAL RESULTS")
print("=" * 70)

for rank, (doc, score) in enumerate(results, start=1):
    print(f"\nRank: {rank}")
    print(f"Distance: {score:.4f}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk index: {doc.metadata.get('chunk_index')}")
    print("-" * 70)
    print(doc.page_content[:1000])