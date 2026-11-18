import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small"
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", 120)
)

CHROMA_COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION_NAME",
    "technical_documentation"
)

CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"


if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. Check your .env file."
    )