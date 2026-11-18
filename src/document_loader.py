from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_core.documents import Document


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_documents():

    documents = []

    for file_path in DATA_DIR.rglob("*"):

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

        loaded_docs = loader.load()

        for doc in loaded_docs:

            relative_path = file_path.relative_to(
                PROJECT_ROOT
            )

            doc.metadata["source"] = str(relative_path)
            doc.metadata["file_type"] = suffix[1:]

            documents.append(doc)

    return documents


def clean_documents(documents):

    cleaned_documents = []

    for doc in documents:

        text = doc.page_content

        text = text.replace("\x00", "")
        text = " ".join(text.split())

        if not text.strip():
            continue

        cleaned_documents.append(
            Document(
                page_content=text,
                metadata=doc.metadata
            )
        )

    return cleaned_documents