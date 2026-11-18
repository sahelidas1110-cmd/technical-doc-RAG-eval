---
title: LangChain Text Splitters and Chunking Strategies
domain: LangChain
source_url: https://docs.langchain.com/oss/python/integrations/splitters
document_type: technical_documentation
version: current
---

# LangChain Text Splitters and Chunking Strategies

## 1. Introduction to Text Splitting

Text splitting is the process of dividing large documents into smaller sections called chunks.

In LangChain, text splitters are used to divide large documents into smaller, manageable pieces while attempting to preserve meaningful context.

Text splitting is an important step in Retrieval-Augmented Generation (RAG) applications.

Large documents are often too long to pass directly into an LLM context window or retrieve efficiently as a single unit.

Chunking makes it possible to retrieve only the relevant portions of a document.

## 2. Why is Chunking Important in RAG?

Chunking plays an important role in retrieval quality.

Consider a technical document containing 50 pages.

If the entire document is stored as one vector, a query about a specific topic may retrieve the entire document rather than the relevant section.

By dividing the document into smaller chunks, the retrieval system can identify more focused pieces of information.

Benefits of chunking include:

- More focused retrieval.
- Better context selection.
- Reduced unnecessary context.
- Improved embedding representation.
- Better utilization of LLM context windows.
- Easier source attribution.
- More efficient document processing.

However, poorly designed chunking strategies can split related information and reduce retrieval quality.

## 3. Understanding Chunk Size

Chunk size determines the maximum size of an individual text chunk.

In many LangChain character-based splitters, `chunk_size` represents the maximum number of characters in a chunk.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500
)
```

This configures the splitter to create chunks with a target maximum size of approximately 500 characters.

The actual chunk size depends on the splitting algorithm and the separators used.

### Impact of Small Chunk Sizes

Advantages:
- More focused information.
- Less unrelated context.
- Potentially more precise retrieval.

Disadvantages:
- Important context may be separated.
- More chunks are generated.
- More embeddings may need to be stored.
- Answers may require retrieving several chunks.

### Impact of Large Chunk Sizes

Advantages:
- More surrounding context is preserved.
- Related information is more likely to remain together.
- Fewer chunks may be generated.

Disadvantages:
- Retrieved chunks may contain irrelevant information.
- Embeddings may represent multiple topics.
- Larger amounts of context may be passed to the LLM.

## 4. Understanding Chunk Overlap

Chunk overlap refers to the amount of text shared between consecutive chunks.

It helps preserve context across chunk boundaries.

Example:

Original text:

```text
Python is a programming language.
It supports object-oriented programming.
Python has many libraries.
```

Suppose the text is divided into chunks with an overlap.

Chunk 1:

```text
Python is a programming language.
It supports object-oriented
```

Chunk 2:

```text
It supports object-oriented
programming.
Python has many libraries.
```

The repeated text provides continuity between the chunks.

Example configuration:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
```

### Benefits of Chunk Overlap

- Preserves information near chunk boundaries.
- Reduces the chance of losing contextual continuity.
- Helps retrieve information that spans adjacent sections.

### Disadvantages of Excessive Overlap

- Increases the total number of chunks.
- Creates redundant content.
- Increases embedding and storage requirements.
- May cause near-duplicate retrieval results.

## 5. Understanding Separators

Separators determine where text splitting should occur.

A text splitter can use different separators to preserve natural text boundaries.

Common separators include:

| Separator | Purpose |
|---|---|
| `"\n\n"` | Paragraph boundaries |
| `"\n"` | Line boundaries |
| `" "` | Word boundaries |
| `""` | Character-level splitting |

For technical documents, paragraph and heading boundaries are often useful because they help preserve semantic structure.

## 6. RecursiveCharacterTextSplitter

`RecursiveCharacterTextSplitter` is a commonly used LangChain text splitter.

It attempts to split text using a prioritized list of separators.

The default separator order is generally:

```python
["\n\n", "\n", " ", ""]
```

It first attempts to split on paragraph boundaries.

If the resulting pieces are still too large, it tries line boundaries, then spaces, and finally individual characters.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Python is a high-level programming language.

It supports object-oriented programming.

Python is widely used in data science.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_text(text)

for index, chunk in enumerate(chunks):
    print(f"Chunk {index + 1}:")
    print(chunk)
```

### Important Parameters

| Parameter | Description |
|---|---|
| `chunk_size` | Maximum target chunk size |
| `chunk_overlap` | Number of overlapping characters |
| `separators` | Ordered list of splitting separators |
| `length_function` | Function used to measure text length |
| `keep_separator` | Controls whether separators are retained |
| `is_separator_regex` | Indicates whether separators are regular expressions |

RecursiveCharacterTextSplitter is a useful general-purpose option for technical documentation and RAG applications.

## 7. CharacterTextSplitter

`CharacterTextSplitter` splits text using a specified separator.

Example:

```python
from langchain_text_splitters import CharacterTextSplitter

text = """
Python is a programming language.

It is easy to learn.

It is widely used.
"""

splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print(chunk)
```

Unlike RecursiveCharacterTextSplitter, this splitter uses the configured separator rather than recursively falling back through multiple separator types.

It may produce chunks larger than the target size when a single separated piece exceeds the limit.

## 8. Splitting Documents Instead of Plain Text

LangChain text splitters support both plain text and Document objects.

### Using `split_text()`

`split_text()` accepts a string and returns a list of text chunks.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "Python is a programming language."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=20,
    chunk_overlap=5
)

chunks = splitter.split_text(text)
```

### Using `split_documents()`

`split_documents()` accepts a collection of LangChain Document objects.

It returns smaller Document objects and generally preserves the original metadata.

```python
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

documents = [
    Document(
        page_content="Python is a programming language. It supports multiple paradigms.",
        metadata={"source": "python_basics.md"}
    )
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=30,
    chunk_overlap=5
)

chunks = splitter.split_documents(documents)

for chunk in chunks:
    print(chunk.page_content)
    print(chunk.metadata)
```

Using `split_documents()` is particularly useful in RAG ingestion pipelines because source metadata is retained.

## 9. Token-Based Chunking

Character-based chunking measures the length of text using characters.

However, LLM context windows and many model limits are measured using tokens.

A token is a unit of text processed by a language model. It may represent a whole word, part of a word, punctuation, or another text unit.

The number of tokens in a text does not always correspond directly to its number of characters.

LangChain supports token-aware splitting through different methods and integrations.

Example using a tokenizer-backed splitter:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-4",
    chunk_size=200,
    chunk_overlap=30
)
```

This example uses a tokenizer to measure chunk size in tokens.

The appropriate tokenizer depends on the model being used.

Token-based chunking can help control the amount of text passed to an LLM.

## 10. Markdown Text Splitting

Technical documentation is frequently written in Markdown.

Markdown contains structural elements such as:

- Headings
- Paragraphs
- Lists
- Tables
- Code blocks

A generic character splitter may split content across meaningful Markdown sections.

LangChain provides Markdown-aware splitting options.

Example:

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_document = """
# Python

Python is a programming language.

## Data Structures

Python supports lists, tuples, sets, and dictionaries.

## Functions

Functions are reusable blocks of code.
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2")
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

documents = splitter.split_text(markdown_document)

for document in documents:
    print(document.page_content)
    print(document.metadata)
```

The splitter uses Markdown headings to create sections and adds heading information to metadata.

This is useful when processing structured technical documentation.

### Combining Markdown Splitting with Recursive Splitting

For large Markdown sections, a two-stage splitting strategy can be useful.

First, split by headings.

Then, split oversized sections into smaller chunks.

```python
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

markdown_document = """
# Python

Python is a programming language.

## Data Structures

Python supports lists, tuples, sets, and dictionaries.

## Functions

Functions are reusable blocks of code.
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2")
]

header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

header_documents = header_splitter.split_text(markdown_document)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

final_chunks = recursive_splitter.split_documents(header_documents)
```

This approach preserves document hierarchy while controlling chunk size.

## 11. HTML Text Splitting

HTML documents contain structural elements such as:

- Headings
- Paragraphs
- Lists
- Tables
- Divisions

LangChain provides HTML-aware splitting options.

Example:

```python
from langchain_text_splitters import HTMLHeaderTextSplitter

html_document = """
<h1>Python</h1>
<p>Python is a programming language.</p>

<h2>Data Structures</h2>
<p>Python supports lists and dictionaries.</p>
"""

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2")
]

splitter = HTMLHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

documents = splitter.split_text(html_document)

for document in documents:
    print(document.page_content)
    print(document.metadata)
```

HTML-aware splitting is useful when processing web-based documentation.

## 12. Code-Aware Text Splitting

Source code should not always be split using ordinary paragraph-based strategies.

Code-aware splitting attempts to preserve programming language structures such as:

- Classes
- Functions
- Methods
- Indentation
- Logical code blocks

LangChain provides `RecursiveCharacterTextSplitter` with language-specific separator configurations.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50
)

code = """
class Employee:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(self.name)
"""

chunks = python_splitter.split_text(code)

for chunk in chunks:
    print(chunk)
```

Language-specific splitting can help preserve code structure better than arbitrary character splitting.

## 13. Semantic Chunking

Semantic chunking attempts to divide text based on changes in meaning rather than relying only on fixed character counts.

The goal is to keep semantically related content together.

A typical semantic chunking workflow includes:

1. Divide the document into smaller sentences or segments.
2. Generate embeddings for those segments.
3. Compare semantic similarity between neighboring segments.
4. Identify significant changes in meaning.
5. Create chunks around those semantic boundaries.

Semantic chunking can help preserve meaningful information units.

However, it may require additional embedding computation and can be more expensive than basic character-based splitting.

The exact implementation depends on the selected splitter or integration.

## 14. Parent-Child Chunking

Parent-child chunking uses different levels of chunk granularity.

A document is divided into:

- Parent chunks: Larger sections containing broader context.
- Child chunks: Smaller sections used for more precise retrieval.

A common workflow is:

1. Split documents into larger parent chunks.
2. Split parent chunks into smaller child chunks.
3. Generate embeddings for child chunks.
4. Retrieve relevant child chunks.
5. Return the associated parent context to the LLM.

Benefits include:

- More focused retrieval.
- Access to broader surrounding context.
- Better separation of retrieval granularity and generation context.

This strategy is useful when small chunks improve retrieval but do not contain enough context to answer questions.

## 15. Chunk Metadata and Source Tracking

Metadata should be preserved when documents are split.

Example:

```python
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

document = Document(
    page_content="Python is a programming language. It supports multiple paradigms.",
    metadata={
        "source": "python_basics.md",
        "domain": "Python",
        "version": "current"
    }
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
    add_start_index=True
)

chunks = splitter.split_documents([document])

for chunk in chunks:
    print(chunk.page_content)
    print(chunk.metadata)
```

The metadata is carried into the generated chunks.

The `add_start_index` option adds a character offset indicating where the chunk starts in the original text.

Useful metadata fields include:

- Source file
- Document title
- Domain
- Section heading
- Page number
- Chunk index
- Start character index
- Document version

Metadata supports source citations, filtering, debugging, and evaluation.

## 16. Choosing the Right Chunking Strategy

Different document types may require different chunking strategies.

| Document Type | Suggested Strategy |
|---|---|
| Plain text | Recursive character splitting |
| Markdown documentation | Markdown header splitting followed by recursive splitting |
| HTML documentation | HTML header splitting |
| Python source code | Language-aware splitting |
| Large PDF documents | Page-aware extraction followed by recursive splitting |
| Semantically complex text | Semantic chunking |
| Long documents requiring context | Parent-child chunking |

These are starting points rather than universal rules. The best strategy should be determined through retrieval experiments.

## 17. Common Chunking Problems

### 17.1 Chunks Too Small

Very small chunks may lose important contextual information.

A retrieved chunk might contain only a definition without the explanation needed to answer a question.

### 17.2 Chunks Too Large

Very large chunks may contain multiple unrelated topics.

This can reduce retrieval precision and increase unnecessary context.

### 17.3 No Chunk Overlap

Without overlap, information near chunk boundaries may become difficult to retrieve together.

### 17.4 Excessive Chunk Overlap

Excessive overlap can produce redundant chunks and unnecessary embedding costs.

### 17.5 Splitting Across Logical Boundaries

A splitter may separate:
- A heading from its explanation.
- A question from its answer.
- A code block from its description.
- A table from its header.

Structure-aware splitting can help reduce these problems.

## 18. Chunking Experiments for RAG Evaluation

Chunking parameters should be evaluated rather than selected arbitrarily.

Useful experiments include:

| Experiment | Chunk Size | Overlap |
|---|---:|---:|
| Experiment A | 400 | 50 |
| Experiment B | 600 | 100 |
| Experiment C | 800 | 120 |
| Experiment D | 1000 | 150 |
| Experiment E | 1200 | 200 |

These values are example configurations, not recommended universal settings.

For each experiment, evaluate:

- Number of generated chunks.
- Average chunk length.
- Retrieval precision.
- Retrieval recall.
- Context relevance.
- Answer correctness.
- Faithfulness.
- Embedding and storage costs.

The best configuration should balance retrieval quality, contextual completeness, and operational cost.

## 19. Best Practices

- Choose chunk sizes based on document structure and model requirements.
- Use overlap to preserve context across boundaries.
- Avoid excessive overlap.
- Prefer structure-aware splitting for Markdown, HTML, and code.
- Preserve source metadata during splitting.
- Use token-aware splitting when model token limits matter.
- Inspect sample chunks before embedding.
- Evaluate chunking strategies using a representative question dataset.
- Keep chunking parameters configurable.
- Record experiment settings so results can be reproduced.

## 20. Key Concepts Summary

| Concept | Description |
|---|---|
| Chunking | Dividing large documents into smaller pieces |
| Chunk Size | Target maximum size of an individual chunk |
| Chunk Overlap | Repeated text shared between neighboring chunks |
| Separator | Boundary used to split text |
| RecursiveCharacterTextSplitter | Splitter that tries multiple separators recursively |
| CharacterTextSplitter | Splits text using a configured separator |
| MarkdownHeaderTextSplitter | Splits Markdown using heading structure |
| HTMLHeaderTextSplitter | Splits HTML using heading structure |
| Token-Based Splitting | Measures chunk size using tokens |
| Semantic Chunking | Splits based on semantic changes |
| Parent-Child Chunking | Uses smaller retrieval chunks and larger context chunks |
| `split_text()` | Splits a plain text string |
| `split_documents()` | Splits LangChain Document objects |
| `add_start_index` | Adds the chunk's starting character position to metadata |

## 21. Official References

- LangChain Documentation — Text Splitters: https://docs.langchain.com/oss/python/integrations/splitters
- LangChain Reference — Text Splitters: https://reference.langchain.com/python/langchain-text-splitters
- RecursiveCharacterTextSplitter: https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter
- MarkdownHeaderTextSplitter: https://reference.langchain.com/python/langchain-text-splitters/markdown/MarkdownHeaderTextSplitter
- HTMLHeaderTextSplitter: https://reference.langchain.com/python/langchain-text-splitters/html/HTMLHeaderTextSplitter