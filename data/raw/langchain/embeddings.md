# Embeddings in LangChain

## 1. What Are Embeddings?

Embeddings are numerical representations of text in the form of vectors.

An embedding model converts text such as a word, sentence, paragraph, or document into a list of floating-point numbers.

For example:

```python
text = "Machine learning is a branch of artificial intelligence."
```

An embedding model may convert this text into a vector that looks conceptually like:

```python
[0.021, -0.034, 0.078, 0.012, -0.056, ...]
```

The actual vector contains many dimensions. Its values represent patterns learned by the embedding model.

The purpose of embeddings is to make it possible to compare text based on semantic relationships rather than relying only on exact keyword matches.

For example, these two sentences use different words but have related meanings:

- "How can I build an API using Python?"
- "What is the process for creating a web service in Python?"

A semantic search system may identify these sentences as related because their embeddings are close in vector space.

## 2. Why Are Embeddings Important in RAG?

Retrieval-Augmented Generation (RAG) uses embeddings to retrieve relevant information from a knowledge base.

A typical RAG application follows these steps:

1. Load documents from different sources.
2. Split documents into smaller chunks.
3. Convert each chunk into an embedding vector.
4. Store the vectors in a vector database.
5. Convert the user's question into an embedding.
6. Compare the query embedding with stored document embeddings.
7. Retrieve the most relevant chunks.
8. Pass the retrieved context to an LLM to generate an answer.

For example:

**Knowledge base document:**

"FastAPI is a Python framework used to build APIs."

**User query:**

"What Python framework can I use to develop REST APIs?"

The query and document may have different wording, but their embeddings can be semantically similar.

The retrieval system uses this similarity to identify relevant document chunks.

## 3. How Do Embeddings Work?

Embedding models learn to represent text in a high-dimensional vector space.

Each input text is mapped to a vector.

Texts with related meanings may be positioned closer together in this space, depending on the model and its training.

The process can be understood in three stages:

### Stage 1: Text Encoding

The embedding model receives text as input.

### Stage 2: Vector Generation

The model converts the input text into a numerical vector.

### Stage 3: Similarity Comparison

The generated vectors can be compared using mathematical similarity or distance metrics.

Important: Embeddings do not store complete sentences or human-readable meanings. They provide numerical representations that help machine learning systems compare text.

## 4. Document Embeddings and Query Embeddings

LangChain provides a standard Embeddings interface with two important methods.

### 4.1 embed_documents()

This method generates embeddings for a list of documents.

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

documents = [
    "Python is a programming language.",
    "FastAPI is a Python framework.",
    "Machine learning is a field of AI."
]

document_vectors = embeddings.embed_documents(documents)

print(len(document_vectors))
```

The result is a list of vectors, with one vector corresponding to each input document.

This method is generally used when preparing documents for storage in a vector database.

### 4.2 embed_query()

This method generates an embedding for a single query.

```python
query = "What is FastAPI?"

query_vector = embeddings.embed_query(query)

print(len(query_vector))
```

This method is generally used when a user submits a question to a RAG application.

The query vector is compared with the vectors already stored in the vector database.

### Difference Between the Two Methods

| Method | Purpose | Input |
|---|---|---|
| `embed_documents()` | Generate embeddings for documents | List of strings |
| `embed_query()` | Generate an embedding for a query | Single string |

The two methods provide a common interface, although some embedding providers may use different internal strategies for documents and queries.

## 5. Popular Embedding Models

Several embedding models are available for semantic search and RAG applications.

### 5.1 OpenAI Embeddings

OpenAI provides embedding models that can convert text into vector representations.

Two commonly used models are:

- `text-embedding-3-small`
- `text-embedding-3-large`

The smaller model is often a practical starting point when balancing cost and retrieval quality.

The larger model may be worth evaluating when retrieval quality is especially important.

### 5.2 Hugging Face Embeddings

Hugging Face provides access to many open-source embedding models.

These models can be useful when an application requires local execution or more control over the embedding infrastructure.

Example using LangChain's Hugging Face integration:

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

This integration requires the relevant Hugging Face LangChain package and model dependencies.

### 5.3 Other Embedding Providers

Other providers and model families include:

- Cohere
- Google
- Voyage AI
- Mistral
- NVIDIA
- Ollama

The appropriate model depends on the application's accuracy, latency, cost, privacy, and infrastructure requirements.

## 6. Similarity and Distance Metrics

After generating embeddings, a retrieval system needs a method to compare vectors.

Three commonly used metrics are:

### 6.1 Cosine Similarity

Cosine similarity measures the cosine of the angle between two vectors.

It focuses on the direction of vectors rather than their magnitude.

The formula is:

```text
Cosine Similarity = (A · B) / (||A|| × ||B||)
```

Where:

- A and B are two vectors.
- A · B is their dot product.
- ||A|| and ||B|| represent their magnitudes.

For normalized vectors, cosine similarity is commonly interpreted as follows:

- A value closer to 1 indicates a more similar direction.
- A value around 0 indicates little directional similarity.
- A value closer to -1 indicates opposite directions.

The actual interpretation depends on the embedding model and data.

### 6.2 Euclidean Distance

Euclidean distance measures the straight-line distance between two vectors.

The formula is:

```text
Distance = sqrt(sum((A[i] - B[i]) ** 2))
```

A smaller distance generally indicates that the vectors are closer together.

### 6.3 Dot Product

The dot product measures the product of corresponding vector values summed across dimensions.

```text
Dot Product = sum(A[i] * B[i])
```

For normalized vectors, dot product and cosine similarity produce the same ranking.

For vectors that are not normalized, vector magnitude can also influence the dot product.

### Comparison

| Metric | What it measures | Typical interpretation |
|---|---|---|
| Cosine similarity | Directional similarity | Higher is more similar |
| Euclidean distance | Straight-line distance | Lower is closer |
| Dot product | Alignment and magnitude | Higher often indicates stronger alignment |

The vector database determines how the comparison is performed. Always check which metric is configured before interpreting retrieval scores.

## 7. Using OpenAI Embeddings with LangChain

LangChain provides the `OpenAIEmbeddings` class through the `langchain-openai` integration package.

Installation:

```powershell
uv add langchain-openai
```

Import:

```python
from langchain_openai import OpenAIEmbeddings
```

Initialize:

```python
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)
```

The API key should be supplied securely through the `OPENAI_API_KEY` environment variable.

A simple example:

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

texts = [
    "Python is used for backend development.",
    "FastAPI is a framework for building APIs."
]

vectors = embeddings.embed_documents(texts)

query_vector = embeddings.embed_query(
    "How can I develop an API using Python?"
)

print("Number of document vectors:", len(vectors))
print("Query vector dimensions:", len(query_vector))
```

The embedding vectors can subsequently be stored and searched using a compatible vector database.

## 8. Embedding Dimensions

An embedding vector contains a fixed number of numerical values.

The number of values is called the embedding dimension.

For example, a vector with 1,536 numerical values has 1,536 dimensions.

Embedding dimensions matter because:

1. They determine the size of each stored vector.
2. They affect memory and storage requirements.
3. They must be compatible with the vector database collection.
4. They can influence retrieval performance and computational cost.

Some embedding models support configurable output dimensions.

When changing the model or its output dimensions, verify compatibility with the existing vector database.

Do not compare vectors generated by incompatible embedding spaces.

## 9. Important Considerations When Using Embeddings

### 9.1 Model Consistency

Use compatible embedding models for both document indexing and query processing.

If documents are embedded using one model and queries using an unrelated model, their vectors may not belong to compatible vector spaces.

This can produce unreliable retrieval results.

### 9.2 Chunk Size

Embedding quality is influenced by the content provided to the model.

If chunks are too small, important context may be lost.

If chunks are too large, a single embedding may represent several unrelated topics.

Chunk size and overlap should be evaluated using the actual knowledge base.

### 9.3 Token Limits

Embedding APIs have input limits.

Large documents should be split into appropriately sized chunks before embedding.

The application should handle inputs that exceed model limits.

### 9.4 Cost and Latency

Generating embeddings through a hosted API may involve usage costs and network latency.

For large document collections, consider:

- Batch processing.
- Caching previously generated embeddings.
- Avoiding unnecessary re-embedding.
- Monitoring API usage.
- Implementing retry and rate-limit handling.

### 9.5 Metadata

Document metadata such as source filename, page number, and document category is useful for filtering and source attribution.

However, metadata is not automatically part of the text sent to an embedding model in every vector-store workflow.

If metadata must influence semantic matching, deliberately include relevant information in the text being embedded or use an appropriate retrieval strategy.

## 10. Embeddings in a Vector Database

Embeddings are commonly stored in vector databases such as:

- Chroma
- FAISS
- Pinecone
- Qdrant
- Weaviate

A vector database stores vectors along with associated text and metadata.

During retrieval:

1. The user's question is converted into a vector.
2. The vector database compares it with stored vectors.
3. The closest matching vectors are identified.
4. Their associated document chunks are returned.

In LangChain, embedding models can be supplied directly to a vector store.

Example using Chroma:

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
```

The vector store can use the embedding function when adding documents and when processing similarity searches.

## 11. Embedding Caching

Embedding generation can become expensive and time-consuming when the same text is processed repeatedly.

Caching helps avoid unnecessary API calls by storing previously generated embeddings.

LangChain provides `CacheBackedEmbeddings` for this purpose.

A cache can improve efficiency when:

- The same documents are processed multiple times.
- An ingestion pipeline is rerun.
- Previously embedded text appears again.
- Repeated queries occur and query caching is enabled.

Cache namespaces should identify the embedding model and relevant configuration.

If the embedding model or dimensions change, use a separate cache namespace or rebuild the cache to avoid reusing incompatible vectors.

Caching does not replace proper document versioning or vector-store update logic.

## 12. Common Problems with Embeddings

### Problem 1: Poor Retrieval Results

Possible causes:

- Incorrect chunk size.
- Poorly structured source documents.
- An unsuitable embedding model.
- Ambiguous user queries.
- Incorrect similarity metric.
- Missing contextual information.

Possible improvements:

- Experiment with different chunk sizes.
- Evaluate alternative embedding models.
- Improve document preprocessing.
- Use metadata filtering.
- Evaluate retrieval with a representative question dataset.

### Problem 2: Embedding Dimension Mismatch

A vector database collection may expect vectors of a particular dimension.

If a different model or output dimension is introduced, the new vectors may not be compatible with the existing collection.

Possible solution:

- Create a new collection with the required configuration.
- Re-embed the documents.
- Rebuild the vector index.

### Problem 3: API Rate Limits

Large ingestion jobs may generate many embedding requests.

Possible improvements:

- Use batching where supported.
- Implement retries with exponential backoff.
- Monitor API usage.
- Process large collections in controlled batches.

### Problem 4: Unnecessary Re-embedding

Repeatedly embedding unchanged documents wastes time and API resources.

Possible improvements:

- Use content hashes.
- Track document versions.
- Cache embeddings.
- Re-embed only changed content.

## 13. Embedding Evaluation in a RAG Application

An embedding model should not be selected only because it is popular.

It should be evaluated against the application's actual retrieval requirements.

Useful evaluation measurements include:

- Recall@K: Measures whether relevant documents appear within the top K retrieved results.
- Precision@K: Measures how many of the top K retrieved results are relevant.
- Mean Reciprocal Rank (MRR): Measures how highly the first relevant result appears.
- Normalized Discounted Cumulative Gain (NDCG): Evaluates ranking quality while considering relevance and position.

A practical experiment can compare different embedding models using the same:

- Document collection.
- Chunking strategy.
- Golden question dataset.
- Retrieval configuration.

This helps identify whether a model improves retrieval quality rather than relying on assumptions.

## 14. Best Practices

1. Choose an embedding model based on retrieval requirements.
2. Use compatible models for document and query embeddings.
3. Select chunk sizes based on experimentation.
4. Keep document metadata for filtering and source attribution.
5. Monitor API costs and latency.
6. Use caching for repeated embedding operations.
7. Avoid unnecessary re-embedding of unchanged content.
8. Rebuild the vector index when changing incompatible embedding configurations.
9. Evaluate retrieval quality using a representative dataset.
10. Record the embedding model and configuration used for every experiment.

## 15. Summary

Embeddings convert text into numerical vectors that enable semantic search.

In a RAG application, they help retrieve relevant document chunks even when the user's wording differs from the original document.

LangChain provides a standard interface through:

- `embed_documents()` for document embeddings.
- `embed_query()` for query embeddings.

OpenAI, Hugging Face, Cohere, and other providers offer embedding models that can be integrated with LangChain.

The quality of a RAG retrieval system depends on several factors, including the embedding model, document preprocessing, chunking strategy, similarity metric, and retrieval configuration.

Embedding evaluation is therefore an important part of building a reliable RAG application.

## References

- LangChain Embedding Models: https://docs.langchain.com/oss/python/integrations/embeddings
- LangChain OpenAI Integration: https://docs.langchain.com/oss/python/integrations/providers/openai
- OpenAI Embeddings Guide: https://platform.openai.com/docs/guides/embeddings
- OpenAI Tokenizer: https://platform.openai.com/tokenizer