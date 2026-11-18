from src.rag_pipeline import generate_answer


questions = [
    "What is FastAPI used for?",
    "Who is the president of France?"
]


for question in questions:

    result = generate_answer(question)

    print("\n" + "=" * 60)
    print("Question:", result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    if result["sources"]:
        for source in result["sources"]:
            print(
                f"[Source {source['source_id']}] "
                f"{source['file']}"
            )
    else:
        print("No relevant sources found.")

    print("=" * 60)