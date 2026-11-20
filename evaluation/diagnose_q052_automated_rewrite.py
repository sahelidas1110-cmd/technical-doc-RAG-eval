from src.retriever import retrieve_documents
from src.query_rewriter import rewrite_query


question = (
    "Design an evaluation approach for a multi-step agent "
    "that searches a knowledge base and then uses a calculator. "
    "Which agent-specific behaviors should be measured, and "
    "what execution evidence could tracing provide when a task fails?"
)


rewritten_query = rewrite_query(question)


print("=" * 80)
print("ORIGINAL QUESTION")
print("=" * 80)

print(question)


print("\n" + "=" * 80)
print("AUTOMATICALLY REWRITTEN QUERY")
print("=" * 80)

print(rewritten_query)


results = retrieve_documents(
    query=rewritten_query,
    k=10
)


print("\n" + "=" * 80)
print("TOP 10 RETRIEVAL RESULTS")
print("=" * 80)


for rank, (doc, score) in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print(f"Distance: {score:.4f}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk index: {doc.metadata.get('chunk_index')}")
    print("-" * 80)

    print(doc.page_content[:500])