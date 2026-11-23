
import json
import logging
from pathlib import Path

from evaluation.retrieval_metrics import calculate_retrieval_metrics
from src.reranker import retrieve_reranked_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EVALUATION_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVALUATION_DIR / "golden_dataset.json"
REPORT_PATH = EVALUATION_DIR / "reranking_report.json"

K = 3
CANDIDATE_K = 20


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    answerable_questions = [
        item for item in dataset
        if item["should_answer"]
    ]

    results = []

    total_metrics = {
        "precision": 0.0,
        "recall": 0.0,
        "hit_rate": 0.0,
        "mrr": 0.0,
    }

    metric_mapping = {
        "precision": "precision_at_k",
        "recall": "recall_at_k",
        "hit_rate": "hit_rate_at_k",
        "mrr": "mrr",
    }

    logger.info(
        "Evaluating reranking on %d answerable questions.",
        len(answerable_questions)
    )

    for item in answerable_questions:
        question_id = item["id"]
        question = item["question"]
        expected_sources = item["expected_sources"]

        retrieved_documents = retrieve_reranked_documents(
            query=question,
            k=K,
            candidate_k=CANDIDATE_K
        )

        metrics = calculate_retrieval_metrics(
            retrieved_results=retrieved_documents,
            expected_sources=expected_sources,
            k=K
        )

        result = {
            "id": question_id,
            "question": question,
            "expected_sources": expected_sources,
            "metrics": metrics,
        }

        results.append(result)

        for metric_name, actual_key in metric_mapping.items():
            total_metrics[metric_name] += metrics[actual_key]

        logger.info(
            "%s | Precision: %.4f | Recall: %.4f | Hit Rate: %.4f | MRR: %.4f",
            question_id,
            metrics["precision_at_k"],
            metrics["recall_at_k"],
            metrics["hit_rate_at_k"],
            metrics["mrr"],
        )

    number_of_questions = len(answerable_questions)

    average_metrics = {
        metric_name: round(
            metric_value / number_of_questions, 4
        )
        for metric_name, metric_value in total_metrics.items()
    }

    report = {
        "experiment": "Dense Retrieval + Cross-Encoder Reranking",
        "retrieval_method": "Dense retrieval followed by Cross-Encoder reranking",
        "candidate_k": CANDIDATE_K,
        "final_k": K,
        "reranking_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "total_questions": number_of_questions,
        "average_metrics": average_metrics,
        "results": results,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("RERANKING EVALUATION RESULTS")
    print("=" * 70)

    print(f"Total questions: {number_of_questions}")
    print(f"Precision@{K}:  {average_metrics['precision']:.4f}")
    print(f"Recall@{K}:    {average_metrics['recall']:.4f}")
    print(f"Hit Rate@{K}:  {average_metrics['hit_rate']:.4f}")
    print(f"MRR:           {average_metrics['mrr']:.4f}")

    print("=" * 70)
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
