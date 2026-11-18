# Retrievers in LangChain

## 1. What Is a Retriever?

A retriever is a component in LangChain that accepts a query and returns relevant documents.

In a Retrieval-Augmented Generation (RAG) application, retrievers are responsible for finding useful information from a knowledge base.

A retriever generally performs the following operations:

1. Accepts a user's query.
2. Searches for relevant information.
3. Returns matching documents.
4. Passes the retrieved documents to the next component in the RAG pipeline.

A retriever does not generate the final answer. Its primary responsibility is document retrieval.

## 2. Why Do We Need Retrievers?

Consider a technical knowledge base containing documentation about Python, FastAPI, and LangChain.

A user asks:

"What is used to create REST APIs in Python?"

The retriever searches the knowledge base and might return:

"FastAPI is a modern Python framework for building APIs."

The retrieved document is then passed to an LLM, which generates an answer using the available context.

Without retrieval, the LLM would have to answer using only its existing model knowledge or information explicitly provided in the prompt.

Retrievers help RAG applications ground their answers in external documents.

## 3. How Does a Retriever Work?

A typical retrieval workflow looks like this:

```text
             User Query
                 |
                 v
          Query Processing
                 |
                 v
             Retriever
                 |
                 v
         Search Knowledge Base
                 |
                 v
         Relevant Documents
                 |
                 v
          Context Builder
                 |
                 v
                LLM
                 |
                 v
           Final Answer
```

In a vector-based RAG system, the retriever commonly uses a vector store to search for semantically similar documents.

However, retrievers are not limited to vector databases. They can also use keyword search, database queries, APIs, or combinations of retrieval methods.

## 4. Retriever Interface in LangChain

LangChain retrievers implement the `BaseRetriever` interface.

A retriever accepts a string query and returns a list of LangChain `Document` objects.

The standard method for invoking a retriever is:

```python
documents = retriever.invoke("What is FastAPI?")
```

The returned documents generally contain:

- `page_content`: Retrieved text.
- `metadata`: Information such as source filename, page number, or category.

Example:

```python
for doc in documents:
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)
```

The retriever interface provides a common way to work with different retrieval strategies.

## 5. Vector Store Retriever

A vector store can be converted into a retriever using `as_retriever()`.

This is one of the most common approaches in RAG applications.

### Example

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma(
    collection_name="technical_documentation",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

documents = retriever.invoke(
    "What is FastAPI used for?"
)

for doc in documents:
    print(doc.page_content)
```

Explanation:

- `as_retriever()` converts the vector store into a retriever.
- `k=3` requests three documents.
- `invoke()` executes the retrieval operation.

The retriever uses the vector store's configured similarity-search behavior by default.

## 6. Types of Retrieval Strategies

Different retrieval strategies can improve the relevance and diversity of retrieved documents.

### 6.1 Similarity Search Retriever

Similarity search retrieves documents whose embeddings are closest to the query embedding.

Example:

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

documents = retriever.invoke(
    "Explain Python functions."
)
```

Here, the retriever returns the three nearest matching documents.

**Advantages:**

- Simple to implement.
- Effective for semantic search.
- Suitable as a starting point for RAG applications.

**Limitations:**

- May return repetitive documents.
- May retrieve weakly relevant results when the query is ambiguous.
- Depends on embedding and chunk quality.

### 6.2 Similarity Score Threshold Retriever

Sometimes, retrieving a fixed number of documents is not ideal.

For example, a query may have only one relevant document, but similarity search still returns five results.

A similarity-score-threshold retriever can filter results based on a minimum relevance score.

Example:

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.7
    }
)
```

Explanation:

- `k=5` sets the maximum number of results.
- `score_threshold=0.7` specifies the minimum relevance score.

**Important:** This threshold applies to the relevance-score interpretation used by the vector-store integration. It is not necessarily the same as the raw distance returned by `similarity_search_with_score()`.

Thresholds should be calibrated using actual retrieval experiments.

### 6.3 Maximum Marginal Relevance (MMR) Retriever

Maximum Marginal Relevance (MMR) attempts to retrieve documents that are both relevant to the query and diverse from one another.

Consider a query:

"Explain the important features of Python."

A similarity search may return several chunks that all discuss Python's syntax.

MMR attempts to balance relevance with diversity so that the final results can cover different aspects of the topic.

Example:

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10,
        "lambda_mult": 0.5
    }
)
```

Parameters:

- `k`: Number of final documents.
- `fetch_k`: Number of candidate documents considered before selecting the final results.
- `lambda_mult`: Controls the balance between relevance and diversity.

A higher lambda value places more emphasis on relevance.

A lower lambda value places more emphasis on diversity.

**Advantages:**

- Reduces repetitive retrieval results.
- Can provide broader context.
- Useful when several chunks contain overlapping information.

**Limitations:**

- May retrieve less directly relevant documents to increase diversity.
- Requires tuning.
- Does not guarantee that every returned document is useful.

## 7. Metadata Filtering in Retrieval

Metadata filtering restricts retrieval to documents that satisfy specified conditions.

For example, suppose the vector database contains documentation about Python, FastAPI, and LangChain.

We want to retrieve only FastAPI documentation.

Example:

```python
retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3,
        "filter": {"topic": "FastAPI"}
    }
)

documents = retriever.invoke(
    "How do I create an API?"
)
```

The filter restricts the search to records whose metadata contains the specified topic.

Metadata filtering is useful for:

- Department-specific document retrieval.
- Product-specific knowledge bases.
- Version-specific documentation.
- Access-controlled document collections.
- Filtering by document category.

The supported filter syntax depends on the vector-store integration.

## 8. Advanced Retrieval Techniques

Basic similarity search works well for many applications, but complex knowledge bases may require more sophisticated retrieval techniques.

### 8.1 Multi-Query Retrieval

A user may ask a question using ambiguous or limited wording.

For example:

"How does FastAPI validate data?"

An LLM can generate alternative queries such as:

- How does FastAPI use Pydantic for request validation?
- How are request bodies validated in FastAPI?
- How do Python type annotations support validation in FastAPI?

A retriever searches using these alternative queries.

The resulting documents are combined, often with duplicate results removed.

**Benefits:**

- Expands the search space.
- Handles different ways of expressing the same question.
- Can improve recall.

**Limitations:**

- Requires additional LLM calls.
- May increase latency and cost.
- Generated queries can introduce irrelevant search terms.

### 8.2 Ensemble Retrieval

Ensemble retrieval combines results from multiple retrieval systems.

For example:

- BM25 keyword retrieval.
- Dense vector similarity retrieval.

BM25 is a keyword-based ranking algorithm.

Dense retrieval uses embeddings to identify semantically related content.

Consider this query:

"What is the HTTP 404 status code?"

Keyword retrieval may identify documents containing the exact term "404".

Vector retrieval may find related explanations even if the exact phrase is not present.

Combining both approaches can improve retrieval coverage.

Ensemble retrieval commonly uses Reciprocal Rank Fusion (RRF) to combine rankings.

#### Reciprocal Rank Fusion (RRF)

RRF combines rankings from multiple retrieval systems.

A commonly used formula is:

\[
RRF(d)=\sum_{r \in R}\frac{1}{k+rank_r(d)}
\]

Where:

- \(d\) is a document.
- \(R\) is the set of ranking systems.
- \(rank_r(d)\) is the rank of the document in a ranking system.
- \(k\) is a constant used to reduce the influence of high rankings.

A document ranked highly by multiple retrieval systems can receive a stronger combined score.

### 8.3 Contextual Compression Retrieval

Sometimes, a retrieved document contains relevant information mixed with unrelated text.

Contextual compression attempts to reduce the retrieved content to the parts that are relevant to the query.

For example:

A 1,000-word document may contain only two paragraphs relevant to the user's question.

A compression step can extract those paragraphs before passing the context to the LLM.

**Benefits:**

- Reduces unnecessary context.
- Can improve the relevance of information passed to the LLM.
- May help control token usage.

**Limitations:**

- Can add model calls and latency.
- May accidentally remove useful context.
- Requires evaluation of the compression process.

### 8.4 Parent Document Retrieval

Small chunks are often better for precise semantic retrieval.

However, very small chunks may lose important surrounding context.

Parent Document Retrieval addresses this problem.

The general process is:

1. Split large documents into parent sections.
2. Split parent sections into smaller child chunks.
3. Index the child chunks.
4. Retrieve the most relevant child chunks.
5. Return their associated parent documents or sections.

Example:

A child chunk contains a definition of dependency injection.

Its parent section contains the complete explanation, code examples, and related concepts.

Returning the parent section provides additional context to the LLM.

### 8.5 Self-Query Retrieval

Self-query retrieval uses an LLM to interpret a natural-language query and identify both:

- The semantic search query.
- Structured metadata filters.

Example:

"Find FastAPI documentation published in version 2.0."

The system may extract:

- Search text: FastAPI documentation.
- Metadata filter: version equals 2.0.

This can help when the knowledge base contains structured metadata.

Self-query retrieval requires an appropriate metadata schema and compatible vector-store integration.

## 9. Keyword Search vs Semantic Search vs Hybrid Search

These are three important retrieval approaches.

| Approach | How it works | Strength |
|---|---|---|
| Keyword search | Matches terms using lexical ranking | Exact terms and identifiers |
| Semantic search | Compares embedding vectors | Meaning and related wording |
| Hybrid search | Combines keyword and semantic retrieval | Balances exact matching and semantic relevance |

### Keyword Search

Keyword search is useful when exact terms matter.

Examples:

- Error codes.
- API endpoint names.
- Product IDs.
- Function names.
- Technical identifiers.

BM25 is a commonly used keyword-ranking algorithm.

### Semantic Search

Semantic search uses embeddings to identify conceptually related content.

It is useful when users express an idea differently from the wording in the source documents.

### Hybrid Search

Hybrid search combines lexical and semantic retrieval.

It can be particularly useful in technical documentation because users often search using both natural-language questions and exact technical terms.

## 10. Retriever Evaluation

A retriever should be evaluated independently from the LLM's answer-generation ability.

A correct answer depends partly on whether the retriever supplies the appropriate evidence.

Important retrieval metrics include:

### 10.1 Precision@K

Precision@K measures how many of the top K retrieved documents are relevant.

\[
Precision@K =
\frac{\text{Relevant documents in top K}}{K}
\]

A higher value indicates that a larger proportion of retrieved documents are relevant.

### 10.2 Recall@K

Recall@K measures how many of the relevant documents are found within the top K results.

\[
Recall@K =
\frac{\text{Relevant documents in top K}}
{\text{Total relevant documents}}
\]

A higher value indicates that the retriever finds more of the relevant evidence.

### 10.3 Mean Reciprocal Rank (MRR)

MRR evaluates how highly the first relevant document appears in the result ranking.

\[
MRR = \frac{1}{N}\sum_{i=1}^{N}\frac{1}{rank_i}
\]

Here, \(rank_i\) is the position of the first relevant result for query \(i\).

A higher MRR means relevant results tend to appear closer to the top.

### 10.4 Normalized Discounted Cumulative Gain (NDCG)

NDCG evaluates the quality of a ranked list while considering the relevance of each result and its position.

It is useful when documents can have different levels of relevance rather than simply being relevant or irrelevant.

## 11. Choosing the Right Retriever

Different retrieval strategies suit different requirements.

| Requirement | Possible approach |
|---|---|
| Basic semantic search | Similarity search |
| Reduce repetitive results | MMR |
| Avoid weak matches | Score threshold |
| Exact technical terms | BM25 |
| Semantic and keyword coverage | Hybrid retrieval |
| Ambiguous user questions | Multi-query retrieval |
| Multiple retrieval sources | Ensemble retrieval |
| Long documents with small indexed chunks | Parent document retrieval |
| Metadata-based natural-language queries | Self-query retrieval |
| Reduce irrelevant retrieved text | Contextual compression |

There is no universally best retriever.

The correct approach should be selected through experiments using the actual knowledge base and evaluation questions.

## 12. Common Retrieval Problems

### Problem 1: Irrelevant Documents

**Possible causes:**

- Poor embedding model.
- Incorrect chunk size.
- Ambiguous query.
- Low-quality source documents.

**Possible improvements:**

- Evaluate different embedding models.
- Improve document preprocessing.
- Experiment with chunking.
- Compare retrieval strategies.

### Problem 2: Missing Relevant Documents

**Possible causes:**

- The top K value is too small.
- Important terms are missing from the query.
- The embedding model does not retrieve the relevant concept effectively.
- Exact keyword matching is required.

**Possible improvements:**

- Increase K.
- Try multi-query retrieval.
- Introduce BM25 or hybrid search.
- Improve query formulation.

### Problem 3: Repetitive Results

**Possible cause:**

Multiple retrieved chunks contain similar information.

**Possible improvement:**

Try MMR or another diversity-aware ranking approach.

### Problem 4: Too Much Context

**Possible cause:**

Large documents or too many chunks are passed to the LLM.

**Possible improvements:**

- Reduce the number of retrieved chunks.
- Improve chunking.
- Use contextual compression.
- Retrieve parent sections selectively.

### Problem 5: Retrieval Scores Are Misinterpreted

**Possible cause:**

Confusing raw vector distances with normalized relevance scores.

**Possible improvement:**

Understand the scoring behavior of the selected vector-store integration before setting thresholds.

## 13. Retrievers in Our RAG Evaluation Project

Our project currently uses Chroma as the vector database.

The retrieval implementation is located in:

```text
src/
    retriever.py
```

The current implementation uses:

```python
similarity_search_with_score(
    query,
    k=3
)
```

The RAG pipeline then filters results using the configured retrieval-distance threshold.

This provides a basic similarity-based retrieval baseline.

Later, we will compare this baseline with alternative retrieval configurations.

Planned experiments include:

1. Similarity search with different K values.
2. Different retrieval-distance thresholds.
3. MMR retrieval.
4. Metadata filtering.
5. Hybrid retrieval, if appropriate for the document corpus.

We will measure retrieval performance using the golden evaluation dataset.

Useful metrics include:

- Precision@K.
- Recall@K.
- MRR.
- NDCG.

We should not assume that a more complex retriever will automatically perform better. Each experiment must be evaluated against the same test questions and document collection.

## 14. Best Practices

1. Start with simple similarity retrieval.
2. Use an appropriate embedding model.
3. Tune the number of retrieved documents.
4. Evaluate retrieval quality independently from answer generation.
5. Use metadata filtering when it provides meaningful constraints.
6. Try MMR when retrieval results are repetitive.
7. Consider hybrid retrieval when exact technical terms matter.
8. Use multi-query retrieval for ambiguous questions when the extra cost is justified.
9. Inspect retrieved chunks when debugging incorrect answers.
10. Record retrieval configurations for reproducible experiments.
11. Measure latency and API cost when introducing advanced retrieval techniques.
12. Avoid adding complexity without measurable improvements.

## 15. Summary

Retrievers are responsible for finding relevant documents in a RAG application.

LangChain provides a common retriever interface that supports different retrieval strategies.

Important concepts include:

- Vector store retrievers.
- Similarity search.
- Similarity score thresholds.
- Maximum Marginal Relevance.
- Metadata filtering.
- Multi-query retrieval.
- Ensemble retrieval.
- Contextual compression.
- Parent document retrieval.
- Self-query retrieval.
- Retrieval evaluation metrics.

A reliable RAG application requires more than simply storing embeddings. It needs a retrieval strategy that consistently finds useful evidence for user queries.

## References

- LangChain Retrieval Concepts: https://docs.langchain.com/oss/python/langchain/retrieval
- LangChain Vector Store Integrations: https://docs.langchain.com/oss/python/integrations/vectorstores
- LangChain Core Retriever API: https://reference.langchain.com/python/langchain-core/retrievers/
- LangChain Learn Tutorials: https://docs.langchain.com/oss/python/learn
