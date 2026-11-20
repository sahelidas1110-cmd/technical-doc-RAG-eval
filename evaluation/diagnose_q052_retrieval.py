from src.retriever import retrieve_documents

question = (
    "Design an evaluation approach for a multi-step agent "
    "that searches a knowledge base and then uses a calculator. "
    "Which agent-specific behaviors should be measured, and "
    "what execution evidence could tracing provide when a task fails?"
)

results = retrieve_documents(query=question, k=10)

print("\nQ052 TOP-10 RETRIEVAL DIAGNOSTIC")
print("=" * 80)

for rank, (doc, score) in enumerate(results, start=1):
    print(f"\nRank: {rank}")
    print(f"Distance: {score:.4f}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk index: {doc.metadata.get('chunk_index')}")
    print("-" * 80)
    print(doc.page_content[:800])