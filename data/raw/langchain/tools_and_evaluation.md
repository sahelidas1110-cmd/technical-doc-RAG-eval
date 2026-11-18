# Tools and Evaluation in LangChain

## 1. Introduction

Tools and evaluation are two important parts of building reliable LLM applications and AI agents.

**Tools** allow an LLM or agent to interact with external systems and perform operations beyond text generation.

**Evaluation** helps developers measure whether an application performs correctly, consistently, and safely.

For example, an enterprise AI assistant may need to:

1. Search internal technical documentation.
2. Retrieve information from a database.
3. Calculate values using Python functions.
4. Call external APIs.
5. Generate a final response.
6. Record the execution trace.
7. Evaluate whether the response and tool usage were correct.

LangChain provides interfaces for defining tools and composing them into applications. LangSmith provides tracing and evaluation capabilities for testing and monitoring those applications.

## 2. What Are Tools?

A tool is a function that an LLM application or agent can invoke to perform a specific operation.

Examples include:

- Calculator.
- Web search.
- Database query.
- File search.
- API request.
- Document retrieval.
- Data analysis.
- Email operations.

A tool allows an LLM application to interact with external systems.

The LLM generally decides when a tool should be used, while the application or agent runtime executes the actual operation.

## 3. Anatomy of a LangChain Tool

A well-designed tool generally has the following components:

| Component | Purpose |
|---|---|
| Name | Identifies the tool |
| Description | Explains what the tool does |
| Input schema | Defines accepted arguments |
| Implementation | Contains the actual Python logic |
| Output | Returns the result of the operation |

For example, consider a multiplication tool.

```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b
```

In this example:

- `multiply` is the tool name.
- `a` and `b` are input parameters.
- The type hints define the expected input types.
- The docstring explains the tool's purpose.
- The function implementation performs multiplication.

The tool schema helps the model understand how to invoke the function.

## 4. Creating Tools Using the @tool Decorator

LangChain provides the `@tool` decorator to convert Python functions into tools.

Example:

```python
from langchain.tools import tool

@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width
```

Invoke the tool directly:

```python
result = calculate_area.invoke({
    "length": 10,
    "width": 5
})

print(result)
```

Output:

```text
50.0
```

Tools can be tested independently before they are integrated into an agent.

This is useful because it separates tool implementation problems from agent reasoning problems.

## 5. Defining Structured Tool Inputs Using Pydantic

Type hints are useful, but complex tools often require more detailed input validation.

Pydantic allows developers to define structured input schemas.

Example:

```python
from pydantic import BaseModel, Field
from langchain.tools import tool


class ProductInput(BaseModel):
    product_name: str = Field(
        description="Name of the product"
    )

    quantity: int = Field(
        gt=0,
        description="Number of products required"
    )


@tool(args_schema=ProductInput)
def calculate_order_quantity(
    product_name: str,
    quantity: int
) -> str:
    """Prepare an order quantity summary."""

    return (
        f"Product: {product_name}, "
        f"Quantity: {quantity}"
    )
```

The Pydantic schema defines:

- Required fields.
- Data types.
- Validation constraints.
- Field descriptions.

For example, `gt=0` ensures that the quantity must be greater than zero.

Structured schemas are especially useful when tools interact with databases, APIs, or business systems.

## 6. Tool Descriptions and Naming

Tool descriptions have an important role in agent behavior.

The model uses tool names and descriptions to decide which tool is appropriate for a request.

Consider two descriptions.

**Poor description:**

```python
@tool
def search_data(query: str) -> str:
    """Search data."""
    return "Results"
```

**Better description:**

```python
@tool
def search_fastapi_docs(query: str) -> str:
    """
    Search the FastAPI technical documentation
    for information about routing, request validation,
    dependencies, and API development.
    """
    return "Results"
```

A good tool description should explain:

1. What the tool does.
2. When it should be used.
3. What information it requires.
4. What it returns.
5. Any important limitations.

Avoid creating several tools with overlapping descriptions unless their responsibilities are clearly different.

## 7. Tool Calling vs Tool Execution

These two concepts are related but not identical.

### Tool Calling

Tool calling occurs when an LLM produces a structured request to invoke a tool.

For example:

```python
{
    "name": "multiply",
    "args": {
        "a": 10,
        "b": 5
    }
}
```

The model has requested the multiplication operation.

### Tool Execution

Tool execution occurs when the application or agent runtime actually runs the function.

```python
result = multiply.invoke({
    "a": 10,
    "b": 5
})
```

The function executes and returns:

```text
50
```

### Comparison

| Tool Calling | Tool Execution |
|---|---|
| Model requests an action | Application performs the action |
| Produces structured arguments | Runs the implementation |
| Does not necessarily execute code | Executes the actual function |
| Depends on model tool-calling support | Depends on application/runtime permissions |

This distinction is important when debugging agent applications.

A model can request an incorrect tool call even when the tool implementation itself is correct.

## 8. Tool Execution and Error Handling

Tools interact with external systems, so failures are possible.

Examples include:

- API timeouts.
- Database connection failures.
- Invalid inputs.
- Authentication failures.
- Missing records.
- Rate limits.

A robust tool should handle expected failures and return useful error information.

Example:

```python
import requests
from langchain.tools import tool


@tool
def get_product_details(product_id: int) -> str:
    """Retrieve product details using a product ID."""

    try:
        response = requests.get(
            f"https://example.com/api/products/{product_id}",
            timeout=10
        )

        response.raise_for_status()

        return response.text

    except requests.Timeout:
        return "The product service timed out."

    except requests.HTTPError:
        return "The product service returned an HTTP error."

    except requests.RequestException:
        return "Unable to retrieve product information."
```

This example uses a placeholder API endpoint. A real implementation must use an authorized service and validate its response.

Error handling should distinguish expected business errors from unexpected system failures.

Do not expose sensitive exception details, API credentials, or internal infrastructure information in tool outputs.

## 9. Tool Permissions and Security

Tools can perform operations that have external consequences.

For example:

- Updating customer records.
- Sending emails.
- Deleting files.
- Executing database queries.
- Making purchases.

Therefore, tools should follow the principle of least privilege.

Important security practices:

### 9.1 Least Privilege

Give each tool only the permissions required for its task.

A search tool should not automatically have permission to delete records.

### 9.2 Input Validation

Validate all inputs before executing an operation.

Never assume that LLM-generated arguments are trustworthy.

### 9.3 Authentication

Use secure authentication for external APIs and databases.

### 9.4 Secret Management

Store API keys and passwords in environment variables or a secrets manager.

Never hardcode credentials in source files.

### 9.5 Human Approval

Require human approval before sensitive or irreversible operations.

### 9.6 Logging

Record useful execution information without exposing sensitive data.

## 10. Testing Individual Tools

Before integrating tools into an agent, test them independently.

For example, consider a multiplication function.

Create a file:

```text
tests/test_tools.py
```

Add:

```python
from langchain.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


def test_multiply():
    result = multiply.invoke({
        "a": 10,
        "b": 5
    })

    assert result == 50


def test_multiply_with_zero():
    result = multiply.invoke({
        "a": 10,
        "b": 0
    })

    assert result == 0
```

Run the tests:

```powershell
uv add --dev pytest
uv run pytest tests/test_tools.py -v
```

Testing individual tools helps identify problems before agent execution is introduced.

For more complex tools, test:

- Valid inputs.
- Invalid inputs.
- Missing parameters.
- Boundary values.
- External API failures.
- Permission restrictions.
- Unexpected responses.

## 11. What Is Evaluation in LLM Applications?

Evaluation is the process of measuring the quality and performance of an LLM application.

A working application is not necessarily a reliable application.

For example, a RAG system may generate an answer that sounds correct but is not supported by the retrieved documents.

Evaluation helps identify such problems.

It can measure:

- Answer correctness.
- Relevance.
- Faithfulness.
- Retrieval quality.
- Tool selection.
- Tool execution.
- Latency.
- Cost.
- Reliability.
- Safety.

Evaluation should be performed at both component and application levels.

## 12. Types of Evaluation

LLM applications commonly use three broad evaluation approaches.

### 12.1 Rule-Based Evaluation

Rule-based evaluation uses deterministic conditions to verify outputs.

Examples:

- Does the response contain a required field?
- Is the JSON valid?
- Does the answer contain a source citation?
- Did the function return the expected value?
- Did the agent call the required tool?

Example:

```python
def test_answer_contains_source():
    answer = (
        "FastAPI is a Python framework. [Source 1]"
    )

    assert "[Source 1]" in answer
```

Advantages:

- Fast.
- Repeatable.
- Relatively inexpensive.
- Suitable for automated tests.

Limitations:

- Cannot reliably judge every semantic or contextual requirement.
- Exact string matching may reject correct alternative wording.

### 12.2 LLM-as-a-Judge Evaluation

LLM-as-a-Judge uses an LLM to evaluate another LLM's output.

For example, an evaluator can compare:

- User question.
- Retrieved context.
- Generated answer.
- Reference answer.

It can then assess whether the generated answer is correct, relevant, and supported by the context.

Advantages:

- Can evaluate semantic similarity.
- Can assess nuanced responses.
- Useful when exact string matching is insufficient.

Limitations:

- Evaluator judgments can be inconsistent.
- Evaluation requires additional model calls and cost.
- Results can be affected by evaluator bias and prompt design.

LLM-based evaluation should be calibrated against human judgments.

### 12.3 Human Evaluation

Human evaluation involves people reviewing application outputs.

It is useful for:

- Complex answers.
- Domain-specific correctness.
- Safety assessment.
- Ambiguous cases.
- Validating automated evaluator performance.

Human evaluation can be more expensive and time-consuming, but it is valuable for high-impact applications.

## 13. Offline and Online Evaluation

Evaluation can be performed before deployment and after deployment.

### 13.1 Offline Evaluation

Offline evaluation tests an application using a curated dataset before releasing changes.

For example, a RAG application may be tested using 100 predefined questions and their expected answers.

It helps compare different versions of the application.

Typical uses:

- Benchmarking.
- Unit tests.
- Regression tests.
- Comparing embedding models.
- Comparing retrieval strategies.

### 13.2 Online Evaluation

Online evaluation monitors application behavior using production traces or user interactions.

It can help detect:

- Increasing error rates.
- Poor answer quality.
- Unexpected tool usage.
- Latency problems.
- New failure patterns.

### Comparison

| Offline Evaluation | Online Evaluation |
|---|---|
| Uses curated datasets | Uses production interactions or traces |
| Usually performed before deployment | Usually performed during production |
| Supports benchmarking | Supports continuous monitoring |
| Helps detect regressions | Helps identify real-world issues |

Both approaches are important for maintaining reliable LLM applications.

## 14. Golden Evaluation Dataset

A golden dataset is a curated collection of representative test examples used to evaluate an application.

For a RAG application, an example may contain:

- Question.
- Expected answer.
- Reference context.
- Expected source.
- Category.
- Whether the system should answer.

Example:

```json
{
    "id": "Q001",
    "question": "What is FastAPI?",
    "expected_answer": "FastAPI is a Python framework for building APIs.",
    "reference_context": "FastAPI is a modern Python framework for building APIs.",
    "expected_sources": [
        "fastapi_basics.md"
    ],
    "category": "factual",
    "should_answer": true
}
```

A good golden dataset should include different types of questions.

Examples:

- Factual questions.
- Conceptual questions.
- Comparison questions.
- Multi-hop questions.
- Complex questions.
- Unanswerable questions.

The dataset should represent the actual application use cases rather than containing only simple questions.

### Why Is a Golden Dataset Important?

It helps developers:

1. Compare different application versions.
2. Identify retrieval failures.
3. Measure answer quality.
4. Detect regressions.
5. Compare embedding models.
6. Compare chunking strategies.
7. Evaluate prompt changes.
8. Track improvements over time.

The same evaluation dataset should be used when comparing experiments, unless the experiment specifically evaluates a different test set.

## 15. Important RAG Evaluation Metrics

RAG evaluation should examine both retrieval and generation.

### 15.1 Retrieval Metrics

**Precision@K**

Measures the proportion of retrieved documents that are relevant.

\[
Precision@K =
\frac{\text{Relevant documents in top K}}
{K}
\]

**Recall@K**

Measures the proportion of all relevant documents that are found within the top K results.

\[
Recall@K =
\frac{\text{Relevant documents in top K}}
{\text{Total relevant documents}}
\]

**Mean Reciprocal Rank (MRR)**

Measures the ranking position of the first relevant result.

\[
MRR =
\frac{1}{N}
\sum_{i=1}^{N}
\frac{1}{rank_i}
\]

**Normalized Discounted Cumulative Gain (NDCG)**

Evaluates the quality of ranked retrieval results while considering their relevance and position.

### 15.2 Generation Metrics

**Faithfulness**

Measures whether the answer is supported by the retrieved context.

**Answer Relevance**

Measures whether the answer addresses the user's question.

**Context Relevance**

Measures whether the retrieved context is relevant to the question.

**Answer Correctness**

Measures whether the generated answer agrees with a reference answer or expected facts.

These metrics measure different aspects of a RAG application. A system can retrieve relevant documents but still generate an incorrect answer.

## 16. Evaluating Tool-Using Agents

Agent evaluation should examine the actions taken by the agent as well as the final response.

Important dimensions include:

### Tool Selection Accuracy

Did the agent choose the appropriate tool?

### Tool Argument Accuracy

Did it supply valid arguments?

### Tool Execution Success

Did the tool execute successfully?

### Task Completion

Did the agent complete the requested task?

### Final Answer Quality

Was the response correct and relevant?

### Safety

Did the agent follow permission and approval requirements?

For example, if an agent is asked to calculate a discounted product price, evaluation should check:

1. Whether it selected the correct calculation tool.
2. Whether it passed the correct price and discount.
3. Whether the calculation was correct.
4. Whether the final answer was accurate.

This is more informative than checking only the final response.

## 17. LangSmith for Tracing and Evaluation

LangSmith is an observability and evaluation platform for LLM applications.

It can help developers understand how an application behaves during execution.

### 17.1 Tracing

Tracing records the execution of an application and its components.

For a RAG application, a trace may contain:

- User input.
- Retriever execution.
- Retrieved documents.
- Prompt construction.
- LLM request.
- LLM response.
- Execution duration.
- Errors and other available metadata.

Tracing helps identify where a problem occurs.

For example, if a RAG application produces an incorrect answer, tracing can help determine whether:

- The retriever returned irrelevant documents.
- The context builder omitted important information.
- The prompt was incorrectly constructed.
- The LLM generated an unsupported answer.

### 17.2 Datasets

LangSmith supports datasets containing examples that can be used for evaluation.

A dataset can contain inputs and reference outputs.

For a RAG application, it may contain:

- User questions.
- Reference answers.
- Expected retrieval information.

### 17.3 Experiments

An experiment evaluates an application against a dataset.

Different application versions can be compared using the same examples.

For example:

- Experiment 1: Similarity search with K=3.
- Experiment 2: Similarity search with K=5.
- Experiment 3: MMR retrieval with K=5.

The results help determine which configuration performs better.

### 17.4 Evaluators

Evaluators assign scores or judgments to application outputs.

Examples include:

- Correctness.
- Relevance.
- Faithfulness.
- Tool selection.
- Custom business rules.

LangSmith supports code-based and LLM-based evaluation approaches.

### 17.5 Online Monitoring

LangSmith can also support online evaluation of production traces.

This helps identify quality changes and emerging failure patterns after deployment.

## 18. Setting Up LangSmith Tracing

LangSmith tracing can be enabled using environment variables.

Install the package:

```powershell
uv add langsmith
```

Configure the environment variables in `.env`:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=technical-doc-rag-eval
```

Load the environment variables in Python:

```python
from dotenv import load_dotenv

load_dotenv()
```

When supported LangChain components execute with tracing enabled, their runs can be sent to the configured LangSmith project.

Do not commit `.env` to GitHub.

Tracing can involve sending application inputs and outputs to an external service. Review data-handling requirements and redact sensitive information before enabling it.

## 19. Automated Evaluation with pytest

pytest is a Python testing framework that can be used to automate application tests.

It is useful for:

- Testing individual functions.
- Testing document loaders.
- Testing retrieval logic.
- Testing prompt construction.
- Testing API endpoints.
- Running regression tests.

Example:

```python
def test_retrieval_returns_documents(retriever):
    documents = retriever.invoke(
        "What is FastAPI?"
    )

    assert len(documents) > 0
```

Another example:

```python
def test_retrieved_document_has_source(retriever):
    documents = retriever.invoke(
        "What is FastAPI?"
    )

    assert all(
        "source" in doc.metadata
        for doc in documents
    )
```

These examples assume that a configured retriever fixture is available.

In a production-quality test suite, use controlled test data rather than depending on an external API or a changing vector database for every unit test.

## 20. DeepEval for RAG Evaluation

DeepEval is a framework for evaluating LLM applications.

It provides evaluation metrics that can be used to assess RAG systems and other LLM applications.

Examples of RAG-related metrics include:

- Answer Relevancy.
- Faithfulness.
- Contextual Precision.
- Contextual Recall.
- Contextual Relevancy.

DeepEval can also be integrated into automated testing workflows.

### Example: Faithfulness Evaluation

A faithfulness evaluation checks whether the generated answer is supported by the supplied context.

Conceptually:

```text
Question:
What is FastAPI?

Retrieved Context:
FastAPI is a Python framework for building APIs.

Generated Answer:
FastAPI is a Python framework used to build APIs.

Evaluation:
The answer is supported by the retrieved context.
```

An answer that introduces unsupported information may receive a lower faithfulness score.

DeepEval metrics may use LLM-based evaluation, so their results should be validated and interpreted carefully.

## 21. RAG Evaluation Tools: Comparison

| Tool | Primary purpose | Typical use |
|---|---|---|
| pytest | Python testing | Unit and regression tests |
| DeepEval | LLM evaluation | RAG and agent evaluation |
| Ragas | RAG evaluation | Retrieval and generation metrics |
| LangSmith | Tracing and evaluation | Experiments and monitoring |

These tools are complementary rather than direct replacements for one another.

For example:

- pytest can verify that the retriever returns the expected data structure.
- DeepEval can assess faithfulness.
- Ragas can measure RAG quality.
- LangSmith can trace application execution and compare experiments.

## 22. Evaluation Strategy for Our Portfolio Project

Our project is an Enterprise RAG Application with an Automated Evaluation Harness.

The objective is to demonstrate that we can build, test, evaluate, and improve a RAG application systematically.

### Stage 1: Component Testing

Use pytest to test:

- Document loading.
- Text cleaning.
- Chunking.
- Embedding configuration.
- Vector-store operations.
- Retrieval behavior.
- Context construction.

### Stage 2: Golden Dataset

Maintain a curated evaluation dataset containing representative questions.

The dataset should cover:

- Factual questions.
- Conceptual questions.
- Comparison questions.
- Multi-hop questions.
- Complex questions.
- Unanswerable questions.

### Stage 3: Retrieval Evaluation

Measure:

- Precision@K.
- Recall@K.
- MRR.
- NDCG.

Compare different retrieval configurations.

### Stage 4: Generation Evaluation

Measure:

- Faithfulness.
- Answer relevance.
- Answer correctness.
- Context relevance.

Use appropriate automated evaluators and manual review.

### Stage 5: Experiment Tracking

Compare different configurations, such as:

| Experiment | Retrieval method | K |
|---|---|---:|
| Baseline | Similarity search | 3 |
| Experiment 2 | Similarity search | 5 |
| Experiment 3 | MMR | 5 |
| Experiment 4 | Similarity search with metadata filtering | 5 |

These are proposed experiments, not measured results.

### Stage 6: Regression Testing

After changing the embedding model, chunk size, retriever, prompt, or LLM:

1. Run the same evaluation dataset.
2. Compare the new results with the baseline.
3. Inspect failures.
4. Identify regressions.
5. Keep changes that demonstrate meaningful improvements.

### Stage 7: Monitoring

After deployment, monitor:

- Request volume.
- Error rates.
- Retrieval latency.
- LLM latency.
- Token usage.
- API cost.
- User feedback.
- Answer quality.

## 23. Common Evaluation Mistakes

### Mistake 1: Evaluating Only the Final Answer

A correct-looking answer does not prove that retrieval was correct.

Evaluate retrieval and generation separately.

### Mistake 2: Using Only Simple Questions

A dataset containing only factual questions does not adequately test a complex RAG application.

Include comparisons, multi-hop questions, and unanswerable questions.

### Mistake 3: Treating LLM Judgments as Perfect

LLM evaluators can make mistakes.

Validate their judgments using human review and known test examples.

### Mistake 4: Changing Multiple Variables at Once

If the embedding model, chunk size, prompt, and retriever are all changed together, it becomes difficult to determine which change caused an improvement.

Change and evaluate variables systematically.

### Mistake 5: Ignoring Latency and Cost

A configuration may improve answer quality but introduce significant latency or cost.

Measure quality alongside operational performance.

### Mistake 6: Ignoring Regression Testing

A change that improves some questions may make previously correct questions fail.

Use the same baseline dataset to detect regressions.

## 24. Best Practices

1. Define clear responsibilities for every tool.
2. Use descriptive tool names and schemas.
3. Validate tool inputs.
4. Test tools independently.
5. Apply least-privilege permissions.
6. Require approval for sensitive operations.
7. Maintain a representative golden dataset.
8. Separate retrieval evaluation from generation evaluation.
9. Use deterministic tests for predictable behavior.
10. Use LLM-as-a-Judge for suitable semantic evaluation tasks.
11. Validate automated evaluation with human judgments.
12. Use tracing to inspect intermediate execution steps.
13. Record experiment configurations.
14. Measure latency and cost alongside quality.
15. Run regression tests after significant changes.
16. Monitor production behavior and incorporate new failure cases into future evaluation datasets.

## 25. Summary

Tools allow LLM applications and agents to interact with external systems and perform operations.

LangChain supports tool creation through:

- `@tool`.
- Structured input schemas.
- Pydantic validation.
- Tool calling.
- Tool execution.

Evaluation helps measure the quality and reliability of an LLM application.

Important evaluation concepts include:

- Rule-based evaluation.
- LLM-as-a-Judge.
- Human evaluation.
- Offline evaluation.
- Online evaluation.
- Golden datasets.
- Retrieval metrics.
- Generation metrics.
- Agent evaluation.
- Regression testing.

Important tools include:

- pytest.
- DeepEval.
- Ragas.
- LangSmith.

A reliable enterprise RAG application needs both well-designed tools and a systematic evaluation strategy.

## References

- LangChain Tools: https://docs.langchain.com/oss/python/langchain/tools
- LangChain Agents: https://docs.langchain.com/oss/python/langchain/agents
- LangChain Core Tool Reference: https://reference.langchain.com/python/langchain-core/tools/
- LangSmith Evaluation Concepts: https://docs.langchain.com/langsmith/evaluation
- LangSmith Evaluation Types: https://docs.langchain.com/langsmith/evaluation-types
- LangSmith Tracing: https://docs.langchain.com/langsmith/observability
- DeepEval Documentation: https://deepeval.com/docs/getting-started
- Ragas Documentation: https://docs.ragas.io/
- pytest Documentation: https://docs.pytest.org/