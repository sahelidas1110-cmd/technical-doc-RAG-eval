from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.api.schemas import QueryRequest, QueryResponse
from src.rag_pipeline import generate_answer
from src.ingest import run_ingestion


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting ingestion pipeline...")

    run_ingestion()

    print("Ingestion completed. API is ready.")

    yield


app = FastAPI(
    title="Technical Documentation RAG API",
    description="API for querying a technical documentation RAG assistant.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "message": "Technical Documentation RAG API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):

    try:

        result = generate_answer(request.question)

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        print(f"Error processing query: {e}")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your question."
        )