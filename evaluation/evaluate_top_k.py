
import json
import logging
from pathlib import Path

from evaluation.retrieval_metrics import calculate_retrieval_metrics
from src.retriever import retrieve_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EVALUATION_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVALUATION_DIR / "golden_dataset.json"
REPORT_PATH = EVALUATION_DIR / "top_k_experiment_report.json"

K_VALUES = [1, 3, 5, 8, 10]


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    answerable_questions = [
        item for item in dataset if item["should_answer"]
    ]

    metric_mapping = {
        "precision": "precision_at_k",
        "recall": "recall_at_k",
        "hit_rate": "hit_rate_at_k",
        "mrr": "mrr",
    }

    experiment_results = []

    logger.info(
        "Starting Top-K experiment on %d answerable questions.",
        len(answerable_questions),
    )

    for k in K_VALUES:

        logger.info("Evaluating K=%d", k)

        total_metrics = {
            "precision": 0.0,
            "recall": 0.0,
            "hit_rate": 0.0,
            "mrr": 0.0,
        }

        question_results = []

        for item in answerable_questions:

            question_id = item["id"]
            question = item["question"]
            expected_sources = item["expected_sources"]

            retrieved_documents = retrieve_documents(
                query=question,
                k=k,
            )

            metrics = calculate_retrieval_metrics(
                retrieved_results=retrieved_documents,
                expected_sources=expected_sources,
                k=k,
            )

            question_results.append(
                {
                    "id": question_id,
                    "question": question,
                    "expected_sources": expected_sources,
                    "metrics": metrics,
                }
            )

            for metric_name, actual_key in metric_mapping.items():
                total_metrics[metric_name] += metrics[actual_key]

        number_of_questions = len(answerable_questions)

        average_metrics = {
            metric_name: round(
                metric_value / number_of_questions, 4
            )
            for metric_name, metric_value in total_metrics.items()
        }

        experiment_results.append(
            {
                "k": k,
                "total_questions": number_of_questions,
                "average_metrics": average_metrics,
                "results": question_results,
            }
        )

        print("\n" + "=" * 60)
        print(f"RESULTS FOR K={k}")
        print("=" * 60)
        print(f"Precision@{k}: {average_metrics['precision']:.4f}")
        print(f"Recall@{k}:    {average_metrics['recall']:.4f}")
        print(f"Hit Rate@{k}:  {average_metrics['hit_rate']:.4f}")
        print(f"MRR:           {average_metrics['mrr']:.4f}")

    report = {
        "experiment": "Top-K Retrieval Tuning",
        "retrieval_method": "Dense retrieval",
        "embedding_model": "text-embedding-3-large",
        "chunk_size": 400,
        "chunk_overlap": 80,
        "k_values": K_VALUES,
        "total_questions": len(answerable_questions),
        "results": experiment_results,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("TOP-K EXPERIMENT SUMMARY")
    print("=" * 70)

    print(
        f"{'K':<8}{'Precision':<15}{'Recall':<15}"
        f"{'Hit Rate':<15}{'MRR':<15}"
    )

    for result in experiment_results:
        metrics = result["average_metrics"]

        print(
            f"{result['k']:<8}"
            f"{metrics['precision']:<15.4f}"
            f"{metrics['recall']:<15.4f}"
            f"{metrics['hit_rate']:<15.4f}"
            f"{metrics['mrr']:<15.4f}"
        )

    print("=" * 70)
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
