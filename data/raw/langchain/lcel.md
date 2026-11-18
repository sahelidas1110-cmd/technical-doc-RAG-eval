# LangChain Expression Language (LCEL)

## 1. What Is LangChain Expression Language (LCEL)?

LangChain Expression Language (LCEL) is a declarative way of composing LangChain components into executable chains.

It allows developers to connect different components such as:

- Prompt templates.
- Language models.
- Output parsers.
- Retrievers.
- Custom Python functions.
- Other Runnable components.

LCEL uses the pipe operator (`|`) to connect components.

The output of one component becomes the input of the next component.

LCEL makes it easier to build, execute, and maintain LLM applications.

## 2. Why Do We Need LCEL?

Consider a basic LLM application.

It requires the following steps:

1. Receive a user's question.
2. Insert the question into a prompt template.
3. Pass the prompt to an LLM.
4. Convert the model response into a readable string.
5. Return the answer.

Without a composition framework, developers may need to write separate functions to manage every step.

LCEL allows these operations to be connected into a single chain.

Example:

```python
chain = prompt | llm | output_parser
```

This makes the workflow easier to understand and maintain.

### Benefits of LCEL

1. Simple composition of components.
2. Reusable chains.
3. Support for synchronous and asynchronous execution.
4. Built-in batch processing interfaces.
5. Streaming support when the components support it.
6. Parallel execution.
7. Integration with LangSmith tracing.
8. Consistent execution interface.

## 3. Understanding the Pipe Operator (`|`)

The pipe operator is the central feature of LCEL.

It connects Runnable components sequentially.

Example:

```python
chain = prompt | llm | output_parser
```

The execution flow is:

```text
Prompt Template
       |
       v
      LLM
       |
       v
 Output Parser
       |
       v
 Final Output
```

The output from the prompt template is passed to the LLM.

The LLM response is passed to the output parser.

The final result is returned to the application.

The pipe operator creates a RunnableSequence when connecting Runnable components.

## 4. What Is a Runnable?

A Runnable is a standard interface used by LangChain components that can be executed or composed with other components.

A Runnable represents a unit of work.

Examples include:

- Chat models.
- Prompt templates.
- Retrievers.
- Output parsers.
- RunnableLambda.
- RunnableParallel.
- RunnableSequence.

Runnables provide a common set of execution methods.

| Method | Purpose |
|---|---|
| `invoke()` | Execute one input |
| `ainvoke()` | Execute one input asynchronously |
| `batch()` | Execute multiple inputs |
| `abatch()` | Execute multiple inputs asynchronously |
| `stream()` | Stream output incrementally |
| `astream()` | Stream output asynchronously |

These methods make it possible to execute different LangChain components using a consistent interface.

## 5. Basic LCEL Example

Let's create a simple chain using a prompt template, an LLM, and an output parser.

### Step 1: Import Libraries

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
```

### Step 2: Create a Prompt Template

```python
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms."
)
```

The prompt contains a variable named `topic`.

### Step 3: Initialize the LLM

```python
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)
```

### Step 4: Create an Output Parser

```python
output_parser = StrOutputParser()
```

`StrOutputParser` converts the model's response into a string.

### Step 5: Connect Components Using LCEL

```python
chain = prompt | llm | output_parser
```

### Step 6: Invoke the Chain

```python
response = chain.invoke({
    "topic": "Machine Learning"
})

print(response)
```

The chain executes all three components in sequence.

## 6. RunnableSequence

RunnableSequence represents a sequence of operations where the output of one Runnable becomes the input of the next.

It is commonly created using the pipe operator.

Example:

```python
from langchain_core.runnables import RunnableLambda

def add_one(x):
    return x + 1

def multiply_by_two(x):
    return x * 2

chain = (
    RunnableLambda(add_one)
    | RunnableLambda(multiply_by_two)
)

result = chain.invoke(5)

print(result)
```

Output:

```text
12
```

Execution:

1. Input = 5.
2. `add_one(5)` returns 6.
3. `multiply_by_two(6)` returns 12.

RunnableSequence is useful when operations must execute in a particular order.

## 7. RunnableLambda

RunnableLambda converts a normal Python function into a Runnable.

This allows custom Python functions to participate in LCEL chains.

Example:

```python
from langchain_core.runnables import RunnableLambda

def uppercase_text(text):
    return text.upper()

uppercase_runnable = RunnableLambda(uppercase_text)

result = uppercase_runnable.invoke("hello langchain")

print(result)
```

Output:

```text
HELLO LANGCHAIN
```

RunnableLambda is useful when custom processing is required between LangChain components.

Examples:

- Formatting retrieved documents.
- Cleaning text.
- Transforming data.
- Extracting values.
- Applying custom business logic.

## 8. RunnableParallel

RunnableParallel executes multiple Runnable components concurrently using the same input.

It is useful when multiple independent operations need to be performed at the same time.

Example:

```python
from langchain_core.runnables import RunnableLambda, RunnableParallel

def uppercase_text(text):
    return text.upper()

def lowercase_text(text):
    return text.lower()

parallel_chain = RunnableParallel(
    uppercase=RunnableLambda(uppercase_text),
    lowercase=RunnableLambda(lowercase_text)
)

result = parallel_chain.invoke("LangChain")

print(result)
```

Conceptual output:

```python
{
    "uppercase": "LANGCHAIN",
    "lowercase": "langchain"
}
```

Both functions receive the same input.

Their results are returned in a dictionary.

### RunnableSequence vs RunnableParallel

| RunnableSequence | RunnableParallel |
|---|---|
| Executes components sequentially | Executes components concurrently |
| Output of one component goes to the next | Same input is provided to each component |
| Used for dependent operations | Used for independent operations |
| Created using the pipe operator | Created using a dictionary or RunnableParallel |

### Practical Example

Suppose an application needs to:

- Generate a short explanation of a topic.
- Generate a list of related keywords.

Both operations can run independently using RunnableParallel.

This can reduce execution time compared with running independent operations sequentially.

## 9. RunnablePassthrough

RunnablePassthrough passes its input forward without changing it.

It is particularly useful in RAG applications where the original question must be preserved while additional information is retrieved.

Example:

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough()

result = chain.invoke({
    "question": "What is FastAPI?"
})

print(result)
```

The output is the same dictionary supplied as input.

### RunnablePassthrough.assign()

The `assign()` method adds new fields to an existing dictionary while preserving its existing values.

Example:

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough.assign(
    topic=lambda x: x["question"].upper()
)

result = chain.invoke({
    "question": "What is FastAPI?"
})

print(result)
```

Conceptual output:

```python
{
    "question": "What is FastAPI?",
    "topic": "WHAT IS FASTAPI?"
}
```

This is useful when a RAG pipeline needs to preserve the original query and add retrieved context.

## 10. LCEL in a RAG Application

LCEL is particularly useful for connecting the major components of a RAG pipeline.

A basic RAG chain contains:

1. A retriever.
2. A context formatter.
3. A prompt template.
4. An LLM.
5. An output parser.

### Example RAG Chain

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.documents import Document


# 1. Initialize embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 2. Initialize vector store
vector_store = Chroma(
    collection_name="technical_documentation",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# 3. Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# 4. Format retrieved documents
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

# 5. Create prompt
prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context.

If the answer is not available in the context,
say that you do not have enough information.

Context:
{context}

Question:
{question}
""")

# 6. Initialize LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

# 7. Create RAG chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 8. Invoke the chain
response = rag_chain.invoke(
    "What is FastAPI?"
)

print(response)
```

### Understanding the RAG Chain

The first dictionary creates a parallel mapping:

```python
{
    "context": retriever | format_docs,
    "question": RunnablePassthrough()
}
```

Two operations happen using the original question:

- The retriever searches the vector database and the formatter converts retrieved documents into context.
- RunnablePassthrough preserves the original question.

The resulting dictionary contains:

```python
{
    "context": "Retrieved document content...",
    "question": "What is FastAPI?"
}
```

The dictionary is then passed to the prompt template.

The prompt is passed to the LLM, and StrOutputParser converts the response into a string.

This example demonstrates how LCEL can connect a complete RAG workflow.

## 11. invoke() Method

`invoke()` executes a Runnable using a single input.

Example:

```python
response = chain.invoke({
    "topic": "Deep Learning"
})
```

It is useful when an application receives one request at a time.

## 12. batch() Method

`batch()` executes a Runnable with multiple inputs.

Example:

```python
questions = [
    {"topic": "Machine Learning"},
    {"topic": "Deep Learning"},
    {"topic": "Generative AI"}
]

responses = chain.batch(questions)

for response in responses:
    print(response)
```

Instead of invoking the chain separately for every question, batch processing provides multiple inputs together.

The default Runnable implementation can process inputs concurrently using a thread pool. Individual integrations may provide more efficient batching behavior.

Batch processing can improve throughput for suitable workloads.

## 13. stream() Method

`stream()` produces output incrementally rather than waiting for the complete response.

This is useful when building chat applications.

Example:

```python
for chunk in chain.stream({
    "topic": "Machine Learning"
}):
    print(chunk, end="", flush=True)
```

Instead of displaying the complete response only after generation finishes, the application can display output as it becomes available.

Streaming improves the perceived responsiveness of an application.

However, streaming depends on the streaming support of the components in the chain.

Some operations may need to finish before output can be streamed.

## 14. Asynchronous Execution

LangChain supports asynchronous execution through methods with an `a` prefix.

Important methods include:

- `ainvoke()`
- `abatch()`
- `astream()`

Asynchronous execution is useful for applications that need to handle multiple I/O-bound operations without blocking the event loop.

Example:

```python
import asyncio

async def main():
    response = await chain.ainvoke({
        "topic": "Agentic AI"
    })

    print(response)

asyncio.run(main())
```

### Synchronous vs Asynchronous Execution

| Synchronous | Asynchronous |
|---|---|
| `invoke()` | `ainvoke()` |
| `batch()` | `abatch()` |
| `stream()` | `astream()` |

Asynchronous execution does not automatically make every operation faster.

Its benefits depend on the workload, concurrency, and whether the underlying integrations support native asynchronous operations.

## 15. LCEL Configuration

Runnables can receive configuration information during execution.

Configuration can include:

- Tags.
- Metadata.
- Run names.
- Maximum concurrency.
- Other execution settings.

Example:

```python
response = chain.invoke(
    {"topic": "RAG"},
    config={
        "tags": ["rag", "learning"],
        "metadata": {
            "project": "technical-doc-RAG-eval"
        }
    }
)
```

Tags and metadata can help identify and organize executions in tracing and debugging tools such as LangSmith.

Configuration can also be passed to other Runnable methods.

## 16. Error Handling, Retries, and Fallbacks

External APIs and other services can occasionally fail.

LangChain provides Runnable methods that help manage certain execution failures.

### 16.1 with_retry()

`with_retry()` creates a Runnable that retries execution when an exception occurs.

Example:

```python
reliable_chain = chain.with_retry(
    stop_after_attempt=3
)
```

This allows up to three attempts according to the retry configuration.

Retries should be used carefully.

They can increase latency and cost, and not every error is temporary or worth retrying.

### 16.2 with_fallbacks()

Fallbacks allow another Runnable to be used if the original Runnable fails.

Example:

```python
from langchain_core.runnables import RunnableLambda

primary = RunnableLambda(
    lambda x: 1 / 0
)

fallback = RunnableLambda(
    lambda x: "Fallback response"
)

safe_chain = primary.with_fallbacks(
    [fallback]
)

result = safe_chain.invoke("test")

print(result)
```

The primary Runnable raises an exception, so the fallback is attempted.

Fallbacks are useful when an application has an alternative execution path.

They should not silently convert every failure into a misleading successful response.

## 17. LCEL and LangSmith

LangSmith provides tracing and observability for LangChain applications.

When LCEL chains are executed with supported tracing configuration, their component executions can be recorded.

This helps developers inspect:

- Input values.
- Output values.
- Execution time.
- Errors.
- Intermediate chain steps.
- Token usage, when provided by the integration.

Tracing is useful when debugging complex RAG pipelines.

For example, if a RAG application generates an incorrect answer, tracing can help determine whether:

1. The retriever returned irrelevant documents.
2. The context formatter produced incomplete context.
3. The prompt was constructed incorrectly.
4. The LLM generated an unsupported answer.

LangSmith can therefore help diagnose problems at individual stages of a chain.

## 18. LCEL vs Traditional Chains

| Feature | LCEL | Traditional chain implementations |
|---|---|---|
| Composition | Pipe operator and Runnable composition | Often requires more explicit class or function wiring |
| Reusability | Runnable components can be reused | Depends on implementation |
| Execution methods | Common Runnable interface | Varies by chain |
| Streaming | Supported when components permit it | Depends on implementation |
| Parallel execution | RunnableParallel | Often requires custom logic |
| Async execution | Common async interface | Depends on implementation |

LCEL is a modern composition approach in LangChain.

Older chain classes such as `LLMChain` are still encountered in older tutorials and codebases. For new LCEL-based examples, composing prompts, models, and parsers with the Runnable interface is generally the more consistent approach.

## 19. Common Problems When Working with LCEL

### Problem 1: Input Key Mismatch

**Problem:** A prompt expects a variable named `question`, but the chain receives a dictionary with a different key.

**Solution:** Make sure the input keys match the prompt template variables.

### Problem 2: Incorrect Output Type

**Problem:** A downstream component expects a string but receives an AIMessage object.

**Solution:** Use an appropriate output parser, such as StrOutputParser.

### Problem 3: Incorrect Runnable Composition

**Problem:** A normal Python function is used in a place where a Runnable is expected.

**Solution:** Use RunnableLambda or a supported callable coercion.

### Problem 4: Streaming Does Not Produce Incremental Output

**Possible causes:**

- A component does not support streaming.
- A custom function buffers the entire input.
- A processing step must finish before output can be generated.

**Solution:** Inspect the streaming behavior of individual components in the chain.

### Problem 5: Parallel Execution Does Not Improve Performance

**Possible causes:**

- Operations are not independent.
- The workload is CPU-bound.
- External API limits restrict concurrency.
- The overhead of parallel execution exceeds its benefits.

**Solution:** Benchmark the chain with realistic workloads.

## 20. Best Practices

1. Use LCEL to connect reusable Runnable components.
2. Keep chains small and understandable.
3. Use RunnableSequence for dependent operations.
4. Use RunnableParallel for independent operations.
5. Use RunnableLambda for custom Python logic.
6. Use RunnablePassthrough when original inputs must be preserved.
7. Use output parsers to standardize downstream output.
8. Use batch processing for suitable multi-input workloads.
9. Use streaming for responsive user interfaces.
10. Use asynchronous execution for appropriate I/O-bound workloads.
11. Add retries only for errors that may be temporary.
12. Use fallbacks when a meaningful alternative exists.
13. Use LangSmith tracing to inspect complex chains.
14. Test each component independently before combining the complete pipeline.

## 21. Summary

LangChain Expression Language provides a consistent way to compose and execute LangChain components.

Important concepts include:

- Pipe operator (`|`).
- Runnable interface.
- RunnableSequence.
- RunnableParallel.
- RunnableLambda.
- RunnablePassthrough.
- invoke and batch.
- stream and asynchronous execution.
- Configuration, retries, and fallbacks.

LCEL is particularly useful in RAG applications because it allows retrievers, context formatting functions, prompts, LLMs, and output parsers to be connected into a single executable workflow.

## References

- LangChain Runnable Reference: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable
- LangChain RunnableSequence: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence
- LangChain RunnableParallel: https://reference.langchain.com/python/langchain-core/runnables/passthrough
- LangChain Core Reference: https://reference.langchain.com/python/langchain-core/runnables
- LangChain Documentation: https://docs.langchain.com/oss/python/langchain/overview