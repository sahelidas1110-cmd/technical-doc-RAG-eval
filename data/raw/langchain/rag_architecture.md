# RAG Architecture

## 1. What Is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is an architecture that combines information retrieval with Large Language Model (LLM) generation.

Instead of relying only on the knowledge learned during model training, a RAG application retrieves relevant information from an external knowledge base and provides it to the LLM as context.

The LLM then generates an answer using the retrieved information.

RAG is especially useful when an application needs to answer questions using:

- Internal company documentation.
- Technical documentation.
- Research papers.
- PDF files.
- Product manuals.
- Policies and procedures.
- Frequently updated information.

### Example

Suppose an organization has a collection of internal HR policy documents.

An employee asks:

"What is the company's leave policy?"

A general-purpose LLM may not know the organization's specific policy.

A RAG application retrieves the relevant HR policy documents and provides their content to the LLM.

The LLM then generates an answer based on the retrieved policy.

## 2. Why Do We Need RAG?

LLMs have several limitations when used without external information.

### 2.1 Knowledge Limitations

An LLM's knowledge is influenced by its training data and training cutoff.

It may not know about newly published documents or recent organizational changes.

### 2.2 Private Data Limitations

A general-purpose LLM does not automatically have access to an organization's private documents.

### 2.3 Hallucinations

An LLM can generate plausible-sounding information that is incorrect or unsupported.

### 2.4 Limited Control Over Sources

Without retrieval, it can be difficult to establish which documents support a particular answer.

RAG helps address these limitations by retrieving external evidence and providing it to the model.

However, RAG does not completely eliminate hallucinations. Retrieval quality, prompt design, context quality, and model behavior still matter.

## 3. High-Level RAG Architecture

A typical RAG application consists of two major workflows:

1. Document ingestion and indexing.
2. Query processing and answer generation.

<text weight="semibold" size="md">Overall architecture</text>

```text
                  DOCUMENT INGESTION
                  ------------------

                  Source Documents
                         |
                         v
                   Document Loader
                         |
                         v
                    Text Cleaning
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
                    Vector Store


                  QUERY PROCESSING
                  ----------------

                    User Query
                         |
                         v
                  Query Processing
                         |
                         v
                  Embedding Model
                         |
                         v
                    Vector Search
                         |
                         v
                Retrieved Documents
                         |
                         v
                  Context Builder
                         |
                         v
                  Prompt Template
                         |
                         v
                       LLM
                         |
                         v
                  Generated Answer
                         |
                         v
                 Response to User
```

The ingestion workflow prepares information for retrieval.

The query workflow retrieves relevant information and uses it to generate an answer.

## 4. Document Ingestion Pipeline

The ingestion pipeline prepares source documents before they are stored in a vector database.

It is generally executed when documents are first added or when existing documents need to be updated.

### Step 1: Document Loading

The application loads information from different sources.

Examples:

- PDF files.
- Markdown files.
- Text files.
- Word documents.
- Web pages.
- Databases.

LangChain provides document loaders for different data sources.

Example:

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "data/raw/example.txt",
    encoding="utf-8"
)

documents = loader.load()
```

The loader returns LangChain Document objects.

A Document generally contains:

- `page_content`: The extracted text.
- `metadata`: Additional information about the source.

### Step 2: Document Cleaning

Raw documents may contain unnecessary or inconsistent content.

Examples include:

- Null characters.
- Repeated whitespace.
- Unwanted headers and footers.
- Formatting artifacts.
- Empty content.

Cleaning helps improve the quality of the text that will be embedded.

However, cleaning should preserve meaningful information such as headings, paragraph boundaries, and code formatting.

### Step 3: Text Splitting

Large documents are divided into smaller chunks.

Embedding models and LLMs have input-size constraints, and smaller chunks can improve retrieval precision.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

chunks = text_splitter.split_documents(documents)
```

Important parameters:

- `chunk_size`: Maximum target chunk size.
- `chunk_overlap`: Amount of text shared between adjacent chunks.

Chunk size and overlap should be evaluated using the actual document collection.

### Step 4: Embedding Generation

Each document chunk is converted into a vector representation.

Example:

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectors = embeddings.embed_documents(
    [chunk.page_content for chunk in chunks]
)
```

These vectors capture numerical representations of the input text.

They enable semantic comparison between documents and user queries.

### Step 5: Vector Storage

The embeddings, document text, and metadata are stored in a vector database.

Example:

```python
from langchain_chroma import Chroma

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="technical_documentation",
    persist_directory="./chroma_db"
)
```

The vector database makes it possible to search for relevant document chunks later.

## 5. Query Processing Pipeline

After the knowledge base has been indexed, users can submit questions.

The query processing pipeline retrieves relevant documents and generates answers.

### Step 1: Receive User Query

Example:

"What is FastAPI and how is it used?"

The application receives this question from the user interface or API endpoint.

### Step 2: Query Embedding

The embedding model converts the question into a vector.

```python
query_vector = embeddings.embed_query(
    "What is FastAPI and how is it used?"
)
```

The query vector represents the question in the embedding space.

### Step 3: Retrieve Relevant Documents

The vector store compares the query embedding with the stored document embeddings.

Example:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

retrieved_docs = retriever.invoke(
    "What is FastAPI and how is it used?"
)
```

The retriever returns the top three matching documents.

### Step 4: Build Context

The retrieved documents are combined into a context string.

Example:

```python
context = "\n\n".join(
    doc.page_content
    for doc in retrieved_docs
)
```

In a production application, context building may also include:

- Source references.
- Metadata.
- Token limits.
- Duplicate removal.
- Context ordering.

### Step 5: Construct the Prompt

The retrieved context and user question are inserted into a prompt template.

Example:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context.

If the answer is not available in the context,
say that you do not have enough information.

Context:
{context}

Question:
{question}
""")
```

The prompt provides instructions to the LLM about how to use the retrieved information.

### Step 6: Generate the Answer

The prompt and context are passed to the LLM.

Example:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

chain = prompt | llm

response = chain.invoke({
    "context": context,
    "question": "What is FastAPI and how is it used?"
})

print(response.content)
```

The LLM generates an answer using the supplied context.

### Step 7: Return the Response

The application returns the answer to the user.

A well-designed application can also return:

- Source documents.
- Page numbers.
- Document names.
- Relevant excerpts.
- Confidence or retrieval diagnostics, when appropriately defined.

## 6. Important Components of a RAG Architecture

| Component | Responsibility |
|---|---|
| Document Loader | Loads information from source documents |
| Document Cleaner | Removes unwanted content while preserving meaning |
| Text Splitter | Divides documents into manageable chunks |
| Embedding Model | Converts text into vectors |
| Vector Store | Stores vectors, text, and metadata |
| Retriever | Finds relevant document chunks |
| Context Builder | Combines retrieved information |
| Prompt Template | Defines instructions and input structure |
| LLM | Generates the final answer |
| User Interface | Accepts questions and displays responses |
| Evaluation System | Measures retrieval and generation quality |

Each component affects the quality and reliability of the overall application.

## 7. Types of RAG Architecture

RAG systems can be designed with different levels of complexity.

### 7.1 Basic or Naive RAG

Basic RAG follows a straightforward retrieval-and-generation workflow.

Steps:

1. Load documents.
2. Split documents into chunks.
3. Generate embeddings.
4. Store embeddings in a vector database.
5. Retrieve relevant chunks.
6. Pass retrieved context to an LLM.
7. Generate an answer.

Advantages:

- Simple to understand.
- Easy to implement.
- Useful as a starting point.
- Suitable for small and medium-sized knowledge bases.

Limitations:

- Retrieval may return irrelevant chunks.
- Complex questions may require information from multiple sources.
- Query wording can affect retrieval.
- Context may contain redundant information.

### 7.2 Advanced RAG

Advanced RAG introduces additional techniques to improve retrieval and answer quality.

Possible techniques include:

- Query rewriting.
- Multi-query retrieval.
- Hybrid search.
- Metadata filtering.
- Maximum Marginal Relevance.
- Reranking.
- Contextual compression.
- Parent document retrieval.

These techniques can improve the retrieval process, but they also add complexity, cost, and latency.

### 7.3 Modular RAG

Modular RAG uses separate components that can be combined or replaced depending on the application's requirements.

For example:

- Query transformation module.
- Retrieval module.
- Reranking module.
- Context processing module.
- Generation module.
- Evaluation module.

This architecture makes it easier to experiment with different retrieval and generation strategies.

## 8. Query Transformation

The original user query is not always suitable for retrieval.

Query transformation modifies or expands the question before searching the knowledge base.

Common techniques include:

### 8.1 Query Rewriting

Rewrites a question to make it clearer.

Original:

"How does it work in FastAPI?"

Rewritten:

"How does dependency injection work in FastAPI?"

### 8.2 Query Expansion

Adds related terms to improve retrieval coverage.

Original:

"Python API validation"

Expanded:

"Python API request validation, Pydantic models, type hints, and input validation."

### 8.3 Multi-Query Retrieval

Generates multiple alternative questions and searches using each one.

This can improve recall when different documents use different terminology.

### 8.4 Query Decomposition

Breaks a complex question into smaller questions.

Example:

"Compare FastAPI and Flask in terms of validation, performance, and API documentation."

This could be decomposed into:

1. How does FastAPI handle request validation?
2. How does Flask handle request validation?
3. What are their performance characteristics?
4. How do their API documentation capabilities differ?

The results can then be combined to answer the original question.

## 9. Reranking in RAG

A retriever may return several relevant-looking documents, but their ranking may not be optimal.

A reranker is a component that evaluates retrieved candidates and reorders them according to their relevance to the query.

### How Reranking Works

1. Retrieve an initial set of candidate documents.
2. Compare each candidate with the user's query.
3. Calculate a relevance score.
4. Reorder the documents.
5. Pass the best-ranked documents to the LLM.

Example:

```text
User Query
    |
    v
Initial Retriever
    |
    v
Top 20 Documents
    |
    v
Reranker
    |
    v
Top 5 Documents
    |
    v
LLM
```

### Bi-Encoder vs Cross-Encoder

**Bi-Encoder:**

- Encodes the query and documents separately.
- Compares their vector representations.
- Suitable for efficient large-scale retrieval.

**Cross-Encoder:**

- Processes the query and document together.
- Produces a relevance score for the pair.
- Often useful for reranking a smaller set of retrieved candidates.

Reranking can improve the quality of retrieved context, but it adds processing cost and latency.

## 10. Context Management

The retrieved context is an important input to the LLM.

Poor context management can reduce answer quality even when the retriever finds relevant documents.

Important considerations include:

### 10.1 Context Length

LLMs have context-window limits.

The application must ensure that the combined prompt, context, and expected response fit within the model's limits.

### 10.2 Duplicate Information

Multiple retrieved chunks may contain overlapping content.

Duplicate information can waste context space.

### 10.3 Context Ordering

The order of retrieved information may influence how an LLM uses it.

Relevant and important evidence should be presented clearly.

### 10.4 Source Attribution

The application should preserve source metadata so that generated answers can be linked to the documents that support them.

### 10.5 Missing Evidence

If the retrieved context does not contain enough information, the application should be able to abstain rather than invent an answer.

## 11. RAG vs Fine-Tuning

RAG and fine-tuning solve different problems.

| Feature | RAG | Fine-Tuning |
|---|---|---|
| Main purpose | Supply external knowledge at inference time | Adapt model behavior through additional training |
| Uses external documents | Yes | Not necessarily |
| Knowledge updates | Update the knowledge base | May require further training |
| Training required | Not necessarily | Yes |
| Source attribution | Can preserve retrieved sources | Not automatically provided |
| Typical use | Question answering over documents | Style, task, or behavior adaptation |

### When Should We Use RAG?

Use RAG when:

- The application needs access to private documents.
- Information changes frequently.
- Answers should be grounded in external sources.
- Users need document-based question answering.

### When Should We Use Fine-Tuning?

Consider fine-tuning when:

- The model needs consistent task-specific behavior.
- A specialized output format is required.
- The model needs to learn a particular style or pattern.
- Prompting alone is insufficient for the desired behavior.

RAG and fine-tuning can also be combined when the application requires both external knowledge and specialized model behavior.

## 12. Common RAG Failure Points

A RAG application can fail at several stages.

### 12.1 Document Loading Failure

**Problem:** Some source content is not extracted correctly.

Possible causes:

- Scanned PDFs without OCR.
- Unsupported file formats.
- Corrupted documents.
- Incorrect text extraction.

**Possible improvements:**

- Validate extracted text.
- Use OCR when necessary.
- Log files that fail to load.
- Track document-processing errors.

### 12.2 Chunking Failure

**Problem:** Relevant information is split across chunks or loses its surrounding context.

**Possible improvements:**

- Experiment with chunk size.
- Adjust overlap.
- Use structure-aware splitting.
- Consider parent document retrieval.

### 12.3 Embedding Failure

**Problem:** Semantically related documents are not retrieved.

**Possible improvements:**

- Compare embedding models.
- Check document preprocessing.
- Verify model consistency.
- Evaluate retrieval performance.

### 12.4 Retrieval Failure

**Problem:** The retriever returns irrelevant documents or misses important evidence.

**Possible improvements:**

- Tune K.
- Try MMR.
- Add metadata filtering.
- Evaluate hybrid search.
- Introduce reranking.

### 12.5 Context Failure

**Problem:** The LLM receives incomplete, redundant, or excessive context.

**Possible improvements:**

- Remove duplicate chunks.
- Improve context construction.
- Apply compression carefully.
- Control the number of retrieved documents.

### 12.6 Generation Failure

**Problem:** The LLM produces an incorrect or unsupported answer.

**Possible improvements:**

- Improve prompt instructions.
- Require evidence-based answers.
- Preserve source references.
- Introduce abstention behavior.
- Evaluate faithfulness and answer relevance.

## 13. RAG Evaluation

A RAG application should be evaluated at both the retrieval and generation stages.

A correct answer depends on retrieving the right evidence and generating an answer that accurately uses it.

### 13.1 Retrieval Evaluation

Retrieval evaluation measures whether the correct documents are found.

Common metrics:

- Precision@K.
- Recall@K.
- Mean Reciprocal Rank (MRR).
- Normalized Discounted Cumulative Gain (NDCG).

### 13.2 Generation Evaluation

Generation evaluation measures the quality of the final answer.

Important evaluation dimensions include:

**Faithfulness**

Does the answer stay consistent with the retrieved context?

**Answer Relevance**

Does the answer address the user's question?

**Context Relevance**

Is the retrieved context relevant to the question?

**Correctness**

Does the answer agree with the expected or reference answer?

### 13.3 RAG Evaluation Tools

Several tools can support RAG evaluation:

- DeepEval.
- Ragas.
- LangSmith.
- Custom evaluation pipelines.

These tools provide different evaluation metrics, tracing capabilities, and experiment workflows.

Evaluation should combine automated measurements with manual inspection of representative examples.

## 14. Production Considerations

A working RAG prototype is not automatically a production-ready application.

Production deployment requires additional engineering.

### 14.1 Security

- Protect API keys.
- Authenticate users.
- Enforce authorization.
- Restrict access to sensitive documents.
- Validate uploaded files.
- Avoid exposing internal prompts or secrets.

### 14.2 Reliability

- Handle embedding API failures.
- Implement retries with appropriate backoff.
- Handle vector-store outages.
- Validate inputs and outputs.
- Log application errors.

### 14.3 Performance

- Optimize document retrieval.
- Use embedding caching where appropriate.
- Control prompt and context size.
- Monitor latency.
- Consider asynchronous processing for suitable workloads.

### 14.4 Monitoring

Monitor:

- Request volume.
- Retrieval latency.
- LLM latency.
- Token consumption.
- API costs.
- Failed requests.
- Retrieval quality.
- User feedback.

### 14.5 Document Lifecycle

A production knowledge base needs a reliable document lifecycle.

This includes:

- Adding new documents.
- Updating existing documents.
- Removing obsolete documents.
- Tracking document versions.
- Rebuilding indexes when necessary.

## 15. RAG Architecture in Our Portfolio Project

Our project is an Enterprise RAG Application with an Automated Evaluation Harness.

Its purpose is to demonstrate a complete document-based question-answering system with measurable retrieval and generation quality.

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangChain | RAG components and orchestration |
| OpenAI Embeddings | Text embedding generation |
| Chroma | Vector storage |
| OpenAI Chat Model | Answer generation |
| DeepEval | Automated evaluation |
| LangSmith | Tracing and monitoring |
| FastAPI | Backend API |
| Streamlit | User interface |
| pytest | Automated testing |
| Docker | Application packaging |
| GitHub Actions | CI automation |

### Current Project Architecture

```text
                 DOCUMENT INGESTION
                         |
                         v
                 data/raw/
                         |
                         v
                 Document Loader
                         |
                         v
                  Text Cleaning
                         |
                         v
                  Text Splitter
                         |
                         v
                 OpenAI Embeddings
                         |
                         v
                    Chroma DB
                         |
                         |
                         v
                   USER QUERY
                         |
                         v
                 RAG Application
                         |
                         v
                    Retriever
                         |
                         v
                Retrieved Documents
                         |
                         v
                  Context Builder
                         |
                         v
                  Prompt Template
                         |
                         v
                 OpenAI Chat Model
                         |
                         v
                  Generated Answer
                         |
                         v
                  Source References
```

### Project Evaluation Architecture

```text
                Golden Evaluation Dataset
                           |
                           v
                    Test Questions
                           |
                           v
                    RAG Application
                           |
                           v
                   Generated Answers
                           |
                           v
                    Evaluation Engine
                           |
                           v
                 Retrieval and Answer Metrics
                           |
                           v
                  Experiment Comparison
                           |
                           v
                   Evaluation Reports
```

### Planned Project Improvements

The project will progressively introduce:

1. A larger and more realistic technical documentation corpus.
2. Better document metadata and ingestion management.
3. A larger golden evaluation dataset.
4. Retrieval experiments using different K values.
5. Similarity search and MMR comparisons.
6. Retrieval-quality measurements.
7. Automated answer evaluation.
8. Experiment tracking.
9. FastAPI deployment.
10. Streamlit interface.
11. Docker packaging.
12. CI automation and testing.

These improvements will be introduced and evaluated incrementally.

## 16. Best Practices for Building RAG Applications

1. Start with a simple, understandable RAG architecture.
2. Use reliable source documents.
3. Preserve useful document structure during preprocessing.
4. Experiment with chunk size and overlap.
5. Select embedding models based on retrieval evaluation.
6. Store useful metadata.
7. Use stable document IDs.
8. Evaluate retrieval independently from answer generation.
9. Inspect retrieved context when debugging incorrect answers.
10. Require source-grounded responses where appropriate.
11. Implement abstention when evidence is insufficient.
12. Monitor latency, reliability, and cost.
13. Test document updates and deletion.
14. Keep evaluation datasets separate from development data when appropriate.
15. Record experiments so that improvements are reproducible.

## 17. Summary

Retrieval-Augmented Generation combines information retrieval with LLM-based answer generation.

A typical RAG architecture contains two major workflows:

**Ingestion:**

- Document loading.
- Cleaning.
- Text splitting.
- Embedding generation.
- Vector storage.

**Query processing:**

- Query processing.
- Document retrieval.
- Context construction.
- Prompt generation.
- LLM response generation.

More advanced RAG architectures can introduce query transformation, hybrid retrieval, reranking, contextual compression, and other techniques.

A reliable RAG application must be evaluated across the entire pipeline rather than focusing only on the final LLM response.

## References

- LangChain RAG Tutorials: https://docs.langchain.com/oss/python/langchain/rag
- LangChain Retrieval Concepts: https://docs.langchain.com/oss/python/langchain/retrieval
- LangChain Document Loaders: https://docs.langchain.com/oss/python/integrations/document_loaders
- LangChain Vector Stores: https://docs.langchain.com/oss/python/integrations/vectorstores
- OpenAI Embeddings Guide: https://platform.openai.com/docs/guides/embeddings
- Ragas Documentation: https://docs.ragas.io/
- DeepEval Documentation: https://deepeval.com/docs/getting-started
- LangSmith Documentation: https://docs.langchain.com/langsmith/home