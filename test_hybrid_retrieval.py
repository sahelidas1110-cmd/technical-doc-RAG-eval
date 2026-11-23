
from src.hybrid_retriever import retrieve_hybrid_documents

results = retrieve_hybrid_documents(
    "What is FastAPI used for?",
    k=3
)

for i, (doc, score) in enumerate(results, start=1):
    print(f"\nRank: {i}")
    print(f"RRF Score: {score:.6f}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk: {doc.metadata.get('chunk_index')}")
    print(f"Content: {doc.page_content[:300]}")
