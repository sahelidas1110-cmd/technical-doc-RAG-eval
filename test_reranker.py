
from src.reranker import retrieve_reranked_documents

query = "What is FastAPI used for?"

results = retrieve_reranked_documents(
    query=query,
    k=3,
    candidate_k=20
)

for rank, (doc, score) in enumerate(results, start=1):
    print(f"\nRank: {rank}")
    print(f"Reranking Score: {score:.6f}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk: {doc.metadata.get('chunk_index')}")
    print(f"Content: {doc.page_content[:300]}")
