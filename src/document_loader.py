from pathlib import Path
import logging
import re

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_core.documents import Document


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"

SUPPORTED_TEXT_FORMATS = {".txt", ".md"}

logger = logging.getLogger(__name__)


# --------------------------------------------------
# DOCUMENT LOADING
# --------------------------------------------------

def load_documents():

    documents = []

    if not DATA_DIR.exists():
        logger.warning("Data directory does not exist: %s", DATA_DIR)
        return documents

    for file_path in sorted(DATA_DIR.rglob("*")):

        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        try:

            # Load PDF documents
            if suffix == ".pdf":
                loader = PyPDFLoader(str(file_path))

            # Load text and Markdown documents
            elif suffix in SUPPORTED_TEXT_FORMATS:
                loader = TextLoader(
                    str(file_path),
                    encoding="utf-8",
                    autodetect_encoding=True
                )

            else:
                logger.info(
                    "Skipping unsupported file: %s",
                    file_path
                )
                continue

            loaded_docs = loader.load()

            relative_path = file_path.relative_to(
                PROJECT_ROOT
            ).as_posix()

            # Extract category from directory structure
            # Example: data/raw/python/functions.md -> python

            relative_to_data = file_path.relative_to(DATA_DIR)

            category = (
                relative_to_data.parts[0]
                if len(relative_to_data.parts) > 1
                else "general"
            )

            for doc in loaded_docs:

                metadata = dict(doc.metadata)

                metadata.update({
                    "source": relative_path,
                    "file_name": file_path.name,
                    "file_type": suffix.lstrip("."),
                    "category": category
                })

                # PyPDFLoader uses zero-based page numbers.
                # Convert them to one-based page numbers.

                if suffix == ".pdf" and "page" in metadata:
                    metadata["page_number"] = metadata["page"] + 1

                documents.append(
                    Document(
                        page_content=doc.page_content,
                        metadata=metadata
                    )
                )

            logger.info(
                "Loaded %d document pages from %s",
                len(loaded_docs),
                relative_path
            )

        except Exception as error:

            logger.exception(
                "Failed to load file %s: %s",
                file_path,
                error
            )

    logger.info(
        "Total documents loaded: %d",
        len(documents)
    )

    return documents


# --------------------------------------------------
# DOCUMENT CLEANING
# --------------------------------------------------

def clean_documents(documents):

    cleaned_documents = []

    for doc in documents:

        text = doc.page_content

        # Remove null characters
        text = text.replace("\x00", "")

        # Normalize Windows and Mac line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove unnecessary spaces and tabs
        # without flattening paragraph structure

        lines = [
            line.rstrip()
            for line in text.split("\n")
        ]

        text = "\n".join(lines)

        # Limit excessive consecutive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove leading and trailing whitespace
        text = text.strip()

        if not text:
            continue

        cleaned_documents.append(
            Document(
                page_content=text,
                metadata=dict(doc.metadata)
            )
        )

    logger.info(
        "Documents remaining after cleaning: %d",
        len(cleaned_documents)
    )

    return cleaned_documents