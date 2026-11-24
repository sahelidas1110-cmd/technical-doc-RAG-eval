from pydantic import BaseModel, Field, field_validator
from typing import Any


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question to ask the technical documentation RAG assistant."
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty or contain only spaces.")

        return value


class QueryResponse(BaseModel):
    answer: str
    sources: list[Any] = Field(default_factory=list)
