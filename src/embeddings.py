import logging
from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL
)


logger = logging.getLogger(__name__)


# --------------------------------------------------
# EMBEDDING MODEL INITIALIZATION
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_model():

    if not EMBEDDING_MODEL:
        raise ValueError(
            "Embedding model name is not configured."
        )

    logger.info(
        "Initializing embedding model: %s",
        EMBEDDING_MODEL
    )

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
        max_retries=3,
        request_timeout=30
    )

    logger.info(
        "Embedding model initialized successfully."
    )

    return embeddings