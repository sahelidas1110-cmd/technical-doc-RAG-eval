from src.retriever import retrieve_documents

queries = [
    (
        "Design an evaluation approach for a multi-step agent "
        "that searches a knowledge base and then uses a calculator. "
        "Which agent-specific behaviors should be measured, and "
        "what execution evidence could tracing provide when a task fails?"
    ),
    (
        "Agent evaluation metrics tool selection accuracy "
        "tool argument accuracy tool execution success "
        "task completion final answer quality safety. "
        "LangSmith tracing execution trace retrieved documents "
        "prompts LLM requests responses duration errors metadata."
    ),
    (
        "LangSmith tracing for agent evaluation and debugging. "
        "Inspect execution traces, intermediate tool calls, "
        "retriever activity, retrieved documents, prompts, "
        "LLM responses, execution duration and errors."
    ),
]

for query_number, query in enumerate(queries, start=1):

    results = retrieve_documents(query=query, k=5)

    print("\n" + "=" * 80)
    print(f"QUERY VARIANT {query_number}")
    print("=" * 80)
    print(query)

    for rank, (doc, score) in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print(f"Distance: {score:.4f}")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Chunk index: {doc.metadata.get('chunk_index')}")
        print("-" * 80)
        print(doc.page_content[:500])