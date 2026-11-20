
import json
import logging
from pathlib import Path

from src.retriever import retrieve_documents
from src.query_rewriter import rewrite_query


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "golden_dataset.json"
)

REGRESSION_IDS = ["Q030", "Q043", "Q092"]

K = 10


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    return {
        item["id"]: item
        for item in dataset
    }


# --------------------------------------------------
# DIAGNOSTIC
# --------------------------------------------------

def diagnose_regressions():

    dataset = load_dataset()

    print("=" * 80)
    print("QUERY REWRITING RECALL REGRESSION DIAGNOSTIC")
    print("=" * 80)

    for question_id in REGRESSION_IDS:

        item = dataset[question_id]

        question = item["question"]
        expected_sources = item["expected_sources"]

        print("\n" + "=" * 80)
        print(f"QUESTION ID: {question_id}")
        print("=" * 80)

        print("\nOriginal question:")
        print(question)

        print("\nExpected sources:")
        for source in expected_sources:
            print(source)

        # ------------------------------------------
        # BASELINE RETRIEVAL
        # ------------------------------------------

        baseline_results = retrieve_documents(
            query=question,
            k=K
        )

        print("\n" + "-" * 80)
        print("BASELINE TOP 10")
        print("-" * 80)

        for rank, (doc, score) in enumerate(
            baseline_results,
            start=1
        ):

            source = doc.metadata.get("source")

            is_relevant = source in expected_sources

            print(f"\nRank: {rank}")
            print(f"Distance: {score:.4f}")
            print(f"Relevant source: {is_relevant}")
            print(f"Source: {source}")
            print(
                f"Chunk index: "
                f"{doc.metadata.get('chunk_index')}"
            )

            print("-" * 60)
            print(doc.page_content[:400])

        # ------------------------------------------
        # QUERY REWRITING
        # ------------------------------------------

        rewritten_query = rewrite_query(question)

        print("\n" + "-" * 80)
        print("REWRITTEN QUERY")
        print("-" * 80)

        print(rewritten_query)

        # ------------------------------------------
        # REWRITTEN RETRIEVAL
        # ------------------------------------------

        rewritten_results = retrieve_documents(
            query=rewritten_query,
            k=K
        )

        print("\n" + "-" * 80)
        print("REWRITTEN QUERY TOP 10")
        print("-" * 80)

        for rank, (doc, score) in enumerate(
            rewritten_results,
            start=1
        ):

            source = doc.metadata.get("source")

            is_relevant = source in expected_sources

            print(f"\nRank: {rank}")
            print(f"Distance: {score:.4f}")
            print(f"Relevant source: {is_relevant}")
            print(f"Source: {source}")
            print(
                f"Chunk index: "
                f"{doc.metadata.get('chunk_index')}"
            )

            print("-" * 60)
            print(doc.page_content[:400])


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    diagnose_regressions()
