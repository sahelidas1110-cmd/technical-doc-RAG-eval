
import json
import logging
from pathlib import Path

from src.rag_pipeline import generate_answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EVALUATION_DIR = Path(__file__).resolve().parent
GOLDEN_DATASET_PATH = EVALUATION_DIR / "golden_dataset.json"
OUTPUT_PATH = EVALUATION_DIR / "deepeval_dataset.json"


def main():

    with open(
        GOLDEN_DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        golden_dataset = json.load(file)

    answerable_questions = [
        item
        for item in golden_dataset
        if item["should_answer"]
    ]

    evaluation_results = []

    logger.info(
        "Preparing DeepEval dataset for %d questions.",
        len(answerable_questions),
    )

    for index, item in enumerate(answerable_questions, start=1):

        question_id = item["id"]
        question = item["question"]

        logger.info(
            "Processing %d/%d: %s",
            index,
            len(answerable_questions),
            question_id,
        )

        rag_result = generate_answer(question)

        retrieved_documents = rag_result.get(
            "retrieved_documents",
            [],
        )

        retrieval_context = [
            doc.page_content
            for doc, score in retrieved_documents
        ]

        retrieved_sources = [
            doc.metadata.get("source", "Unknown source")
            for doc, score in retrieved_documents
        ]

        evaluation_item = {
            "id": question_id,
            "input": question,
            "actual_output": rag_result["answer"],
            "expected_output": item["expected_answer"],
            "retrieval_context": retrieval_context,
            "expected_sources": item["expected_sources"],
            "retrieved_sources": retrieved_sources,
            "category": item["category"],
            "should_answer": item["should_answer"],
        }

        evaluation_results.append(evaluation_item)

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            evaluation_results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    logger.info(
        "DeepEval dataset successfully saved."
    )

    print("=" * 70)
    print("DEEPEVAL DATASET PREPARATION")
    print("=" * 70)
    print(f"Questions processed: {len(evaluation_results)}")
    print(f"Output file: {OUTPUT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()
