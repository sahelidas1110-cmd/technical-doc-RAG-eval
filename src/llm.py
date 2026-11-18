import logging
from functools import lru_cache

from langchain_openai import ChatOpenAI

from src.config import (
    OPENAI_API_KEY,
    CHAT_MODEL
)


logger = logging.getLogger(__name__)


# --------------------------------------------------
# CHAT MODEL INITIALIZATION
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_chat_model():

    if not CHAT_MODEL:
        raise ValueError(
            "Chat model name is not configured."
        )

    logger.info(
        "Initializing chat model: %s",
        CHAT_MODEL
    )

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=0,
        max_retries=3,
        timeout=30
    )

    logger.info(
        "Chat model initialized successfully."
    )

    return llm