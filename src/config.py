import os
from pathlib import Path

from dotenv import load_dotenv


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


# --------------------------------------------------
# ENVIRONMENT VARIABLE HELPERS
# --------------------------------------------------

def get_int_env(variable_name, default):

    value = os.getenv(variable_name, str(default))

    try:
        return int(value)

    except ValueError as error:
        raise ValueError(
            f"{variable_name} must be an integer. "
            f"Received: {value}"
        ) from error


def get_float_env(variable_name, default):

    value = os.getenv(variable_name, str(default))

    try:
        return float(value)

    except ValueError as error:
        raise ValueError(
            f"{variable_name} must be a number. "
            f"Received: {value}"
        ) from error


# --------------------------------------------------
# OPENAI CONFIGURATION
# --------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small"
)

CHAT_MODEL = os.getenv(
    "OPENAI_CHAT_MODEL",
    "gpt-4.1-mini"
)


# --------------------------------------------------
# TEXT SPLITTING CONFIGURATION
# --------------------------------------------------

CHUNK_SIZE = get_int_env(
    "CHUNK_SIZE",
    800
)

CHUNK_OVERLAP = get_int_env(
    "CHUNK_OVERLAP",
    120
)

if CHUNK_SIZE <= 0:
    raise ValueError("CHUNK_SIZE must be greater than zero.")

if CHUNK_OVERLAP < 0:
    raise ValueError("CHUNK_OVERLAP cannot be negative.")

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError(
        "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
    )


# --------------------------------------------------
# RETRIEVAL CONFIGURATION
# --------------------------------------------------

MAX_RETRIEVAL_DISTANCE = get_float_env(
    "MAX_RETRIEVAL_DISTANCE",
    1.0
)

if MAX_RETRIEVAL_DISTANCE < 0:
    raise ValueError(
        "MAX_RETRIEVAL_DISTANCE cannot be negative."
    )


# --------------------------------------------------
# CHROMA DATABASE CONFIGURATION
# --------------------------------------------------

CHROMA_COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION_NAME",
    "technical_documentation"
)

CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"


# --------------------------------------------------
# API KEY VALIDATION
# --------------------------------------------------

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please check your project's .env file."
    )