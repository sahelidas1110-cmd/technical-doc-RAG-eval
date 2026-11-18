from langchain_openai import ChatOpenAI

from src.config import CHAT_MODEL


def get_chat_model():
    """
    Initialize and return the OpenAI chat model.
    """

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0,
        max_retries=2,
        timeout=30
    )

    return llm