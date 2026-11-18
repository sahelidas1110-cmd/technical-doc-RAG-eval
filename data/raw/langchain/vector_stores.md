# Vector Stores in LangChain

## 1. What Is a Vector Store?

A vector store is a specialized storage system designed to store and search vector embeddings.

In a RAG application, documents are converted into embeddings before being stored in a vector store.

When a user submits a query, the application converts that query into an embedding and searches for similar vectors.

The vector store returns the corresponding document chunks and metadata.

A vector store typically manages:

- Document IDs.
- Document text.
- Embedding vectors.
- Metadata.
- Similarity search.
- Document updates and deletion.

Examples of popular vector stores include:

- Chroma
- FAISS
- Pinecone
- Qdrant
- Weaviate
- Milvus

## 2. Why Do We Need a Vector Store?

Consider a knowledge base containing 10,000 technical documents.

If a user asks:

"What framework can I use to develop Python APIs?"

A traditional keyword search may look for exact terms such as "Python", "framework", or "API".

However, a semantic search system can retrieve relevant documents even if they use different wording.

For example:

"FastAPI is a modern Python framework for building APIs."

A vector store makes this possible by comparing the embedding of the user's query with the embeddings stored in the database.

### Benefits

1. Semantic search based on vector similarity.
2. Efficient retrieval from large document collections.
3. Metadata-based filtering.
4. Support for document insertion, updates, and deletion.
5. Integration with RAG pipelines.
6. Persistent storage, depending on the selected vector store.

## 3. How Does a Vector Store Work?

A typical vector-store workflow has two main stages.

### Stage 1: Indexing Documents

1. Load documents.
2. Split documents into chunks.
3. Generate embeddings for each chunk.
4. Assign an ID to each chunk.
5. Store the text, embedding, and metadata.

Example:

```text
Document
   |
   v
Text Splitter
   |
   v
Document Chunks
   |
   v
Embedding Model
   |
   v
Vector Embeddings
   |
   v
Vector Store
```

### Stage 2: Retrieving Documents

1. Receive the user's query.
2. Generate a query embedding.
3. Compare the query vector with stored vectors.
4. Rank matching results.
5. Return the most relevant document chunks.

```text
User Query
    |
    v
Embedding Model
    |
    v
Query Vector
    |
    v
Vector Store Search
    |
    v
Ranked Documents
    |
    v
Retrieved Context
```

The retrieved context is subsequently passed to the LLM in a RAG pipeline.

## 4. LangChain Vector Store Interface

LangChain provides a common VectorStore interface that allows applications to work with different vector databases using similar methods.

Some important methods include:

| Method | Purpose |
|---|---|
| `add_documents()` | Add LangChain Document objects |
| `add_texts()` | Add raw text |
| `similarity_search()` | Retrieve similar documents |
| `similarity_search_with_score()` | Retrieve documents with scores |
| `delete()` | Delete documents using IDs |
| `update_documents()` | Update existing documents |
| `as_retriever()` | Convert a vector store into a retriever |

The exact capabilities and behavior can vary across vector-store integrations.

## 5. Chroma Vector Database

<badge color="success">Used in this project</badge>

Chroma is an open-source vector database that supports embedding storage and similarity search.

It can be used for:

- Semantic search.
- RAG applications.
- Document retrieval.
- Metadata filtering.
- Persistent vector storage.

LangChain provides the Chroma integration through the `langchain-chroma` package.

### 5.1 Installation

```powershell
uv add langchain-chroma
uv add chromadb
```

### 5.2 Import Required Libraries

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
```

### 5.3 Initialize the Embedding Model

```python
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)
```

### 5.4 Initialize Chroma

```python
vector_store = Chroma(
    collection_name="technical_documentation",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

Explanation:

- `collection_name`: Name of the collection in Chroma.
- `embedding_function`: Embedding model used to generate vectors.
- `persist_directory`: Local directory where the database is stored.

A collection is a logical grouping of stored records.

The `persist_directory` allows a local Chroma database to be reopened in a later application session.

### 5.5 Add Documents

LangChain uses the `Document` class to represent text and its associated metadata.

```python
documents = [
    Document(
        page_content="FastAPI is a Python framework for building APIs.",
        metadata={"topic": "FastAPI"}
    ),
    Document(
        page_content="Python supports object-oriented programming.",
        metadata={"topic": "Python"}
    ),
    Document(
        page_content="LangChain helps developers build LLM applications.",
        metadata={"topic": "LangChain"}
    )
]

ids = ["doc_001", "doc_002", "doc_003"]

vector_store.add_documents(
    documents=documents,
    ids=ids
)
```

When documents are added, the embedding function generates their vectors and Chroma stores the records.

Providing IDs explicitly is useful because it allows the application to identify records for later updates or deletion.

### 5.6 Perform Similarity Search

```python
query = "How can I build an API using Python?"

results = vector_store.similarity_search(
    query=query,
    k=2
)

for doc in results:
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)
```

Here:

- `query` is the user's question.
- `k=2` requests the two nearest matching documents.
- `results` contains LangChain Document objects.

### 5.7 Similarity Search with Scores

```python
results = vector_store.similarity_search_with_score(
    query="How can I build an API using Python?",
    k=3
)

for doc, score in results:
    print("Content:", doc.page_content)
    print("Score:", score)
```

This method returns document-score pairs.

**Important:** In the Chroma integration, `similarity_search_with_score()` returns a distance value, not a universally normalized similarity percentage.

For distance-based metrics, a smaller distance generally means a closer match.

Do not assume that a score of 0.8 means 80% similarity.

The interpretation depends on the vector store and its configured distance metric.

### 5.8 Metadata Filtering

Metadata filtering allows retrieval to be restricted to documents matching specified conditions.

For example, suppose the database contains documents about Python, FastAPI, and LangChain.

We want to retrieve only FastAPI documents.

```python
results = vector_store.similarity_search(
    query="How do I create an API?",
    k=3,
    filter={"topic": "FastAPI"}
)

for doc in results:
    print(doc.page_content)
    print(doc.metadata)
```

Metadata filtering is useful when a knowledge base contains multiple document categories, products, departments, or versions.

### 5.9 Update Documents

A document can be updated using its existing ID.

```python
updated_document = Document(
    page_content="FastAPI is a modern Python framework for building APIs.",
    metadata={"topic": "FastAPI"}
)

vector_store.update_documents(
    ids=["doc_001"],
    documents=[updated_document]
)
```

The vector store updates the document associated with the specified ID.

### 5.10 Delete Documents

```python
vector_store.delete(
    ids=["doc_002"]
)
```

This deletes the record associated with the supplied ID.

Deletion and update behavior should be tested against the particular vector-store integration being used.

## 6. Chroma Collections

A collection is a logical container for records in Chroma.

For example, an enterprise application could maintain separate collections for:

- Python documentation.
- FastAPI documentation.
- LangChain documentation.
- Internal company policies.

Example:

```python
python_store = Chroma(
    collection_name="python_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

fastapi_store = Chroma(
    collection_name="fastapi_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

Collections can help organize documents and separate different knowledge bases.

For many applications, one collection with useful metadata fields and filters may also be sufficient.

The correct design depends on retrieval requirements and data isolation needs.

## 7. Convert a Vector Store into a Retriever

A retriever is an interface that accepts a query and returns relevant documents.

A vector store can be converted into a retriever using `as_retriever()`.

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
```

Invoke the retriever:

```python
results = retriever.invoke(
    "What is FastAPI?"
)

for doc in results:
    print(doc.page_content)
```

### Difference Between Vector Store and Retriever

| Vector Store | Retriever |
|---|---|
| Stores embeddings and documents | Retrieves relevant documents |
| Provides database operations | Provides a retrieval interface |
| Can add, update, and delete records | Primarily focuses on retrieving records |
| Supports similarity search | Can use different retrieval strategies |

A vector store can act as the underlying storage mechanism for a retriever.

A retriever does not necessarily have to use a vector database. Other retrieval strategies can also implement the retriever interface.

## 8. Retrieval Strategies

LangChain supports different retrieval approaches through vector-store retrievers.

### 8.1 Similarity Search

Similarity search retrieves the top K documents closest to the query embedding.

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
```

This is a common starting point for RAG applications.

### 8.2 Similarity Score Threshold

This approach retrieves documents only when their relevance scores satisfy a specified threshold.

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.7
    }
)
```

The threshold is based on the relevance-score interpretation provided by the integration.

It is not interchangeable with the raw distance returned by `similarity_search_with_score()`.

Calibrate the threshold using actual retrieval results rather than choosing a value arbitrarily.

### 8.3 Maximum Marginal Relevance (MMR)

MMR stands for Maximum Marginal Relevance.

It attempts to balance two objectives:

1. Retrieve documents relevant to the query.
2. Reduce unnecessary similarity among the retrieved documents.

For example, a query may return five chunks that all explain the same concept.

MMR attempts to retrieve relevant chunks that provide more varied information.

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

- `k`: Number of final documents to return.
- `fetch_k`: Number of candidate documents to retrieve before selecting the final results.
- `lambda_mult`: Controls the balance between query relevance and diversity.

A higher lambda value favors relevance, while a lower value gives more emphasis to diversity.

MMR can be useful when retrieved chunks are highly repetitive.

## 9. Other Popular Vector Stores

### 9.1 FAISS

FAISS stands for Facebook AI Similarity Search.

It is a library developed for efficient similarity search and clustering of dense vectors.

It is commonly used for local vector search and experimentation.

LangChain provides a FAISS integration.

Installation:

```powershell
uv add faiss-cpu
```

Example:

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = FAISS.from_documents(
    documents,
    embeddings
)

results = vector_store.similarity_search(
    "What is FastAPI?",
    k=3
)
```

FAISS is useful when an application needs efficient vector similarity search without operating a separate database server.

For this example, the FAISS integration is imported from `langchain-community`. Check the current integration documentation and package compatibility before adopting it in a new project.

### 9.2 Pinecone

Pinecone is a managed vector database service.

It is designed for applications that need hosted vector storage and retrieval.

Typical use cases include:

- Large-scale semantic search.
- Production RAG applications.
- Managed infrastructure.
- Scalable vector retrieval.

### 9.3 Qdrant

Qdrant is an open-source vector database.

It supports vector similarity search and payload-based filtering.

It can be deployed locally or as a managed service.

### 9.4 Weaviate

Weaviate is an open-source vector database that supports vector search and additional data-management capabilities.

It can be used for semantic search and RAG applications.

## 10. Chroma vs FAISS vs Pinecone vs Qdrant

| Feature | Chroma | FAISS | Pinecone | Qdrant |
|---|---|---|---|---|
| Main purpose | Vector database | Vector similarity-search library | Managed vector database | Vector database |
| Local usage | Yes | Yes | Through hosted service | Yes |
| Managed cloud option | Yes | Not a database service itself | Yes | Yes |
| Metadata filtering | Yes | More limited in basic FAISS workflows | Yes | Yes |
| Persistence | Yes | Supported through index saving | Managed | Yes |
| Typical use | RAG and local development | Local search and experimentation | Managed production search | Local and production search |

The best choice depends on the application's scale, infrastructure, operational requirements, and retrieval needs.

## 11. Persistence in Vector Stores

Persistence means retaining stored data beyond the lifetime of a Python process.

Without persistence, an in-memory vector store may lose its data when the application exits.

For local Chroma storage:

```python
vector_store = Chroma(
    collection_name="technical_documentation",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

To reopen the same collection later, initialize it using the same collection name and persistence directory:

```python
vector_store = Chroma(
    collection_name="technical_documentation",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

The stored collection can then be searched without rebuilding it from the original documents.

For production systems, also consider backups, access controls, storage reliability, and recovery procedures.

## 12. Important Vector Store Design Considerations

### 12.1 Unique Document IDs

Every stored chunk should have a stable, unique ID.

Stable IDs help with:

- Updating documents.
- Deleting obsolete chunks.
- Avoiding accidental duplicates.
- Tracking document versions.

### 12.2 Metadata Management

Useful metadata fields may include:

```python
metadata = {
    "source": "fastapi_basics.md",
    "topic": "FastAPI",
    "document_type": "technical_documentation",
    "version": "1.0"
}
```

Metadata can support filtering, source attribution, and debugging.

### 12.3 Embedding Model Consistency

Documents and queries should use compatible embedding models.

If the embedding model or vector dimensions change, the existing index may need to be rebuilt.

### 12.4 Avoid Duplicate Records

Repeated ingestion can create duplicate or outdated records if document IDs and update logic are not managed properly.

A reliable ingestion pipeline should:

- Generate deterministic IDs.
- Track source documents.
- Detect content changes.
- Update modified records.
- Remove obsolete chunks.

### 12.5 Retrieval Quality

A vector store does not guarantee that the retrieved documents are correct or useful.

Retrieval quality depends on:

- Embedding model.
- Chunking strategy.
- Similarity metric.
- Metadata.
- Query wording.
- Retrieval configuration.

Evaluate retrieval results using a representative question dataset.

## 13. Vector Store Performance and Scalability

As a knowledge base grows, vector retrieval needs to remain efficient.

Important considerations include:

- Number of stored vectors.
- Embedding dimensions.
- Index configuration.
- Batch insertion.
- Query concurrency.
- Metadata filtering.
- Storage and memory requirements.
- Database availability.

Some vector stores use approximate nearest-neighbor (ANN) search to improve search efficiency on large collections.

ANN methods trade some search accuracy for faster retrieval.

The appropriate configuration should be evaluated against the application's latency and retrieval-quality requirements.

## 14. Common Problems and Troubleshooting

### Problem 1: Dimension Mismatch

**Cause:** The query embedding and stored document embeddings have incompatible dimensions.

**Solution:** Use a compatible embedding model and rebuild the collection when necessary.

### Problem 2: Duplicate Documents

**Cause:** Documents are repeatedly inserted without stable IDs or update logic.

**Solution:** Use deterministic IDs and implement idempotent ingestion.

### Problem 3: Irrelevant Search Results

**Possible causes:**

- Poor chunking.
- Incorrect embedding model.
- Inappropriate distance metric.
- Missing metadata filters.
- Poorly worded queries.

**Solution:** Evaluate different retrieval settings and inspect retrieved chunks.

### Problem 4: Data Not Available After Restart

**Cause:** The vector store was created in memory or reopened using a different persistence directory or collection name.

**Solution:** Configure persistence and use the same collection name and directory.

### Problem 5: Incorrect Score Interpretation

**Cause:** Treating a raw distance as a similarity percentage.

**Solution:** Verify whether the method returns distance or normalized relevance scores before applying thresholds.

## 15. Best Practices

1. Choose a vector store based on application requirements.
2. Use stable IDs for every document chunk.
3. Store useful metadata with each document.
4. Use consistent embedding models.
5. Avoid unnecessary re-embedding.
6. Implement document update and deletion logic.
7. Use metadata filtering when appropriate.
8. Compare similarity search and MMR.
9. Configure persistence for local applications.
10. Evaluate retrieval quality using a golden dataset.
11. Monitor retrieval latency and database performance.
12. Maintain backups and recovery procedures for important data.

## 16. Summary

Vector stores are an important component of RAG applications.

They store document embeddings and support semantic retrieval.

LangChain provides a common interface for integrating vector databases such as Chroma, FAISS, Pinecone, and Qdrant.

In this project, Chroma is used to store technical documentation embeddings.

Important concepts include:

- Adding documents.
- Similarity search.
- Metadata filtering.
- Document updates and deletion.
- Persistence.
- Retriever integration.
- Maximum Marginal Relevance.
- Retrieval evaluation.

A well-designed vector store and ingestion process provide the foundation for reliable document retrieval.

## References

- LangChain Chroma Integration: https://reference.langchain.com/python/langchain-chroma/vectorstores/Chroma
- Chroma Documentation: https://docs.trychroma.com/
- LangChain Vector Store Concepts: https://docs.langchain.com/oss/python/integrations/vectorstores
- FAISS Documentation: https://faiss.ai/
- Pinecone Documentation: https://docs.pinecone.io/
- Qdrant Documentation: https://qdrant.tech/documentation/
- Weaviate Documentation: https://docs.weaviate.io/