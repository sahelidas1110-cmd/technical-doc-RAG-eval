from src.query_rewriter import rewrite_query


question = (
    "Design an evaluation approach for a multi-step agent "
    "that searches a knowledge base and then uses a calculator. "
    "Which agent-specific behaviors should be measured, and "
    "what execution evidence could tracing provide when a task fails?"
)


print("=" * 80)
print("ORIGINAL QUESTION")
print("=" * 80)

print(question)


rewritten_query = rewrite_query(question)


print("\n" + "=" * 80)
print("REWRITTEN QUERY")
print("=" * 80)

print(rewritten_query)