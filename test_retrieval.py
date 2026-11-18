from src.retriever import retrieve_documents


test_questions = [
    "What is the difference between a Python list and a tuple?",
    "What is the purpose of text splitters in LangChain?",
    "How does dependency injection work in FastAPI?",
    "Who is the current president of France?",
    "What is the capital of Japan?"
]


for question in test_questions:

    print("\n" + "=" * 70)
    print("QUESTION:", question)

    results = retrieve_documents(
        query=question,
        k=5
    )

    print("\nRETRIEVED DOCUMENTS:")

    for index, (doc, score) in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Source:", doc.metadata.get("source"))
        print("Category:", doc.metadata.get("category"))
        print("Chunk index:", doc.metadata.get("chunk_index"))
        print("Distance:", round(float(score), 4))
        print("Content:", doc.page_content[:300])

    print("=" * 70)