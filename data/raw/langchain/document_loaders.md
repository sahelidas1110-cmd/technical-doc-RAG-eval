---
title: LangChain Document Loaders
domain: LangChain
source_url: https://docs.langchain.com/oss/python/integrations/document_loaders
document_type: technical_documentation
version: current
---

# LangChain Document Loaders

## 1. Introduction to Document Loaders

Document loaders are components in LangChain that load data from different sources and convert it into a standardized LangChain Document format.

They allow applications to work with different data sources without needing to implement a separate document-processing interface for every source.

Document loaders can load data from:

- PDF files
- Text files
- Markdown files
- CSV files
- JSON files
- Web pages
- Databases
- Cloud storage
- Productivity platforms such as Notion and Slack

Document loaders are commonly used in Retrieval-Augmented Generation (RAG) applications to ingest external knowledge before performing text splitting, embedding generation, and vector database storage.

## 2. Understanding the LangChain Document Object

LangChain represents loaded content using the `Document` object.

A Document generally contains two important attributes:

1. `page_content`: The textual content of the document.
2. `metadata`: Additional information associated with the document.

Example:

```python
from langchain_core.documents import Document

document = Document(
    page_content="Python is a high-level programming language.",
    metadata={
        "source": "python_basics.md",
        "category": "Python",
        "page": 1
    }
)

print(document.page_content)
print(document.metadata)
```

Output:

```text
Python is a high-level programming language.

{'source': 'python_basics.md', 'category': 'Python', 'page': 1}
```

### Why is Metadata Important?

Metadata provides additional context about the origin and characteristics of a document.

Common metadata fields include:

| Metadata Field | Description |
|---|---|
| `source` | Original file path or source location |
| `page` | Page number in a document |
| `title` | Document title |
| `category` | Document category |
| `author` | Document author |
| `file_type` | File format such as PDF or Markdown |

Metadata is useful for:

- Identifying the original source of retrieved information.
- Displaying source citations in RAG applications.
- Filtering documents during retrieval.
- Tracking document versions.
- Organizing documents by category.

The metadata fields available depend on the document loader and any additional metadata processing performed by the application.

## 3. Understanding the BaseLoader Interface

LangChain document loaders follow a common interface based on `BaseLoader`.

Although individual loaders have different configuration parameters, they provide common methods for retrieving documents.

Important methods include:

| Method | Description |
|---|---|
| `load()` | Loads all documents and returns them as a list |
| `lazy_load()` | Loads documents lazily, yielding them one at a time |
| `aload()` | Asynchronously loads documents |
| `alazy_load()` | Asynchronously yields documents |

The methods supported by a particular loader can depend on its implementation.

Example:

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "sample.txt",
    encoding="utf-8"
)

documents = loader.load()

for document in documents:
    print(document.page_content)
```

The loader reads the text file and converts its content into LangChain Document objects.

## 4. Loading PDF Documents

PDF files are one of the most common knowledge sources in RAG applications.

PDF document loaders extract text and associated metadata from PDF files.

### 4.1 PyPDFLoader

`PyPDFLoader` is a classic LangChain Community integration that uses the `pypdf` library to extract text from PDF files.

Example:

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("technical_documentation.pdf")

documents = loader.load()

print(f"Total pages loaded: {len(documents)}")

for document in documents:
    print(document.page_content)
    print(document.metadata)
```

Typically, the loader returns a separate Document for each PDF page.

Metadata can include the source file and page information.

### 4.2 Loading a PDF Lazily

For larger documents, lazy loading can help process pages incrementally.

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("technical_documentation.pdf")

for document in loader.lazy_load():
    print(document.page_content)
```

This avoids requiring the application to collect every loaded page into a list before processing begins.

### 4.3 Alternative PDF Loaders

Other PDF parsing integrations include:

- PyMuPDFLoader
- PDFPlumberLoader
- PDFMinerLoader
- UnstructuredPDFLoader
- DoclingLoader

Different PDF loaders have different extraction capabilities.

For example, some tools provide additional support for layout information, tables, images, and structured elements.

The choice depends on document complexity and extraction requirements.

**Version note:** PyPDFLoader, PyMuPDFLoader, PDFPlumberLoader, and PDFMinerLoader belong to the classic `langchain-community` integration ecosystem. Current LangChain documentation identifies this package as unmaintained and recommends using supported partner integrations for new projects. The examples above are included for compatibility with existing applications.

## 5. Loading Text Files

`TextLoader` loads text files and converts their contents into LangChain Document objects.

Example:

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "python_basics.txt",
    encoding="utf-8"
)

documents = loader.load()

print(documents[0].page_content)
print(documents[0].metadata)
```

The text content is stored in `page_content`.

The source file path is generally stored in the metadata.

TextLoader is useful for ingesting:

- `.txt` files
- Plain-text technical documentation
- Extracted textual content
- Application notes

For Markdown files, a text loader can read the file as text. A specialized Markdown parser may be needed when preserving document structure is important.

## 6. Loading Markdown Documents

Markdown is commonly used for technical documentation and knowledge bases.

A Markdown file contains structured content using elements such as:

- Headings
- Paragraphs
- Lists
- Tables
- Code blocks
- Links

A classic approach is to use `TextLoader`.

Example:

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "fastapi_basics.md",
    encoding="utf-8"
)

documents = loader.load()

print(documents[0].page_content)
```

The Markdown content is loaded as text.

The loader does not automatically convert YAML front matter into metadata fields. If a Markdown file contains metadata such as title, domain, and source URL in front matter, the application must parse that information separately.

This is important when building a structured technical documentation knowledge base.

## 7. Loading Multiple Files Using DirectoryLoader

`DirectoryLoader` loads files from a directory using a specified loader class.

It is useful when an application needs to ingest multiple files from a folder.

Example:

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

loader = DirectoryLoader(
    "data/raw",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()

print(f"Total documents loaded: {len(documents)}")
```

### Understanding the Parameters

| Parameter | Description |
|---|---|
| `path` | Directory containing the files |
| `glob` | Pattern used to identify files |
| `loader_cls` | Loader class used for each file |
| `loader_kwargs` | Additional arguments passed to the loader |

The pattern `**/*.md` matches Markdown files in the directory and its subdirectories.

### Loading Different File Types

A directory can contain multiple file formats.

In such cases, an application can use separate loaders based on file extensions.

Example:

```python
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

def load_documents(directory):
    documents = []

    for file_path in Path(directory).rglob("*"):

        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))

        elif suffix in [".txt", ".md"]:
            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

        else:
            continue

        loaded_documents = loader.load()

        for document in loaded_documents:
            document.metadata["source"] = str(file_path)
            document.metadata["file_type"] = suffix[1:]

        documents.extend(loaded_documents)

    return documents
```

This approach allows an ingestion pipeline to process different file formats using their appropriate loaders.

## 8. Loading CSV Files

CSV stands for Comma-Separated Values.

CSV files are commonly used to store structured tabular data.

LangChain provides a classic `CSVLoader` integration through the Community package.

Example:

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="employees.csv"
)

documents = loader.load()

for document in documents:
    print(document.page_content)
    print(document.metadata)
```

By default, each CSV row is represented as a separate Document.

The row's values are converted into text, commonly using column names and their corresponding values.

### CSVLoader with a Source Column

A CSV file may contain a column identifying the source of each record.

Example:

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="employees.csv",
    source_column="employee_id"
)

documents = loader.load()
```

The `source_column` parameter allows the loader to use a selected CSV column as the document source.

CSV loading is useful when structured records need to be converted into text for retrieval.

For analytical workflows, pandas may be more suitable when the application needs extensive tabular transformations before converting rows into Documents.

## 9. Loading JSON Files

JSON stands for JavaScript Object Notation.

It is a commonly used format for storing structured information and exchanging data between applications.

A classic LangChain Community integration provides `JSONLoader` for loading JSON data using a `jq`-style schema.

Example:

```python
from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="employees.json",
    jq_schema=".employees[]",
    text_content=False
)

documents = loader.load()

for document in documents:
    print(document.page_content)
    print(document.metadata)
```

The `jq_schema` parameter specifies which JSON elements should be extracted.

The exact schema depends on the structure of the input JSON file.

For example, consider:

```json
{
    "employees": [
        {
            "name": "Alice",
            "department": "IT"
        },
        {
            "name": "Bob",
            "department": "Finance"
        }
    ]
}
```

The expression `.employees[]` selects each object inside the employees array.

JSONLoader belongs to the classic Community integration ecosystem. For new applications, check the current LangChain integration catalog and choose a supported parser or partner integration.

## 10. Loading Web Pages

LangChain supports loading content from web pages through web document loader integrations.

A classic integration is `WebBaseLoader`.

Example:

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    "https://docs.python.org/3/"
)

documents = loader.load()

print(documents[0].page_content)
print(documents[0].metadata)
```

The loader retrieves webpage content and extracts text into LangChain Document objects.

### Common Applications

Web document loading is useful for:

- Technical documentation ingestion.
- Knowledge base creation.
- Website content retrieval.
- Research and information extraction.
- Building documentation-based RAG systems.

### Important Considerations

Web loading depends on:
- Network connectivity.
- Website accessibility.
- Website structure.
- HTML parsing behavior.
- Website access policies.

Some websites use JavaScript to render content dynamically. Basic HTML loaders may not extract all dynamically rendered content.

In such cases, browser-based or specialized web extraction integrations may be necessary.

Always respect website terms, robots policies, authentication requirements, and rate limits.

## 11. Loading Documents from Databases

LangChain provides integrations for loading data from different database systems.

Examples include:
- SQL databases
- MongoDB
- PostgreSQL
- Elasticsearch
- Other supported database systems

Database loaders can retrieve records and convert them into Document objects.

A common SQL approach uses `SQLDatabaseLoader` from the classic Community integration ecosystem.

The exact implementation depends on the database, connection configuration, and supported integration.

Database loading is useful when an application needs to build a searchable knowledge base from structured database records.

## 12. Loading Documents from Cloud Storage and Productivity Platforms

LangChain has integrations for loading data from external platforms.

Examples include:

| Source | Example Integration |
|---|---|
| Google Drive | Google Drive loaders |
| Amazon S3 | S3 loaders |
| Microsoft OneDrive | OneDrive loaders |
| Notion | Notion loaders |
| Slack | Slack loaders |
| GitHub | GitHub loaders |

These integrations may require:
- API credentials
- Authentication tokens
- Cloud permissions
- Additional Python packages
- External service configuration

The exact setup depends on the selected integration.

Community integrations should be reviewed carefully because they may be maintained by third parties.

## 13. Understanding Document Metadata

Metadata is important for organizing and retrieving documents.

Consider a loaded PDF document:

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("fastapi_guide.pdf")

documents = loader.load()

for document in documents:

    print("Content:")
    print(document.page_content)

    print("Metadata:")
    print(document.metadata)
```

The metadata may contain information such as:

```python
{
    "source": "fastapi_guide.pdf",
    "page": 0
}
```

An application can enrich the metadata with additional fields.

Example:

```python
for document in documents:
    document.metadata["domain"] = "FastAPI"
    document.metadata["document_type"] = "technical_documentation"
```

Metadata enrichment helps support:
- Domain-based filtering.
- Source attribution.
- Document version tracking.
- Retrieval organization.
- Evaluation and debugging.

## 14. Loading Documents vs Splitting Documents

Document loading and document splitting are two separate stages in a RAG ingestion pipeline.

### Document Loading

Document loading extracts content from an external source and converts it into Document objects.

Example:

```python
loader = TextLoader("python_basics.md")

documents = loader.load()
```

### Document Splitting

Document splitting divides large Documents into smaller chunks.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

chunks = splitter.split_documents(documents)
```

### Difference Between Loading and Splitting

| Document Loading | Document Splitting |
|---|---|
| Extracts content from source files | Divides extracted content into smaller pieces |
| Produces Document objects | Produces smaller Document objects |
| Handles source formats | Handles chunk boundaries and size |
| Uses document loaders | Uses text splitters |

The two operations are complementary but serve different purposes.

## 15. Document Loaders in a RAG Pipeline

Document loaders form the initial stage of a typical RAG ingestion pipeline.

A simplified workflow is:

1. Identify source documents.
2. Load documents using appropriate loaders.
3. Clean extracted text.
4. Enrich document metadata.
5. Split documents into chunks.
6. Generate embeddings.
7. Store embeddings and associated documents in a vector database.

Example architecture:

```text
PDF / TXT / Markdown / Web Pages
              |
              v
       Document Loaders
              |
              v
       LangChain Documents
              |
              v
       Text Cleaning
              |
              v
       Metadata Enrichment
              |
              v
        Text Splitting
              |
              v
       Embedding Generation
              |
              v
         Vector Store
```

## 16. Document Loaders in an Enterprise RAG Application

In a production-oriented RAG application, document loading requires more than simply extracting text.

Important considerations include:

### Source Tracking

Every document should retain information about its original source.

This enables traceability and source citations.

### Metadata Management

Documents should contain useful metadata such as:
- Document title
- Domain
- File type
- Source path
- Document version
- Page number
- Ingestion timestamp

### Error Handling

The ingestion process should handle:
- Missing files.
- Corrupted PDFs.
- Unsupported formats.
- Permission errors.
- Extraction failures.
- Network failures.

### Incremental Ingestion

A production pipeline should identify new or updated documents rather than unnecessarily processing the entire knowledge base every time.

### Duplicate Detection

The ingestion pipeline should avoid storing duplicate document content.

A document hash or another stable identifier can help identify repeated or unchanged content.

### Document Versioning

When a source document changes, the system should have a strategy for updating or replacing its previous indexed content.

### Security

Sensitive documents should be handled according to access permissions and data protection requirements.

A RAG system should not expose information to users who are not authorized to access it.

## 17. Best Practices for Using Document Loaders

- Select a loader appropriate for the source format.
- Preserve source information in metadata.
- Validate extracted content before indexing.
- Handle unsupported and corrupted files.
- Use lazy loading when appropriate for large document collections.
- Enrich metadata with useful domain information.
- Avoid unnecessary duplicate ingestion.
- Track document versions and updates.
- Evaluate extraction quality, especially for complex PDFs and tables.
- Review the maintenance status of third-party integrations before adopting them.

## 18. Key Concepts Summary

| Concept | Description |
|---|---|
| Document Loader | Component that extracts data from a source |
| Document | LangChain representation of textual content and metadata |
| `page_content` | Main text content of a Document |
| `metadata` | Additional information about a Document |
| `BaseLoader` | Common document loader interface |
| `load()` | Loads all documents into a list |
| `lazy_load()` | Produces documents incrementally |
| `aload()` | Asynchronously loads documents |
| `TextLoader` | Classic loader for text files |
| `PyPDFLoader` | Classic loader for PDF files |
| `CSVLoader` | Classic loader for CSV files |
| `JSONLoader` | Classic loader for JSON files |
| `DirectoryLoader` | Loads files from a directory |
| `WebBaseLoader` | Classic loader for web pages |
| Metadata Enrichment | Adds useful information to document metadata |

## 19. Official References

- LangChain Documentation — Document Loader Integrations: https://docs.langchain.com/oss/python/integrations/document_loaders
- LangChain Reference — Document Loaders: https://reference.langchain.com/python/langchain-community/document_loaders
- LangChain Documentation — PDF Integrations: https://docs.langchain.com/oss/python/integrations/document_loaders
- LangChain Core — Documents: https://reference.langchain.com/python/langchain-core/documents/base/Document