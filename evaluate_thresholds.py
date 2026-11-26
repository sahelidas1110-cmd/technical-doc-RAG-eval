import pandas as pd

from src.retriever import retrieve_documents
from threshold_test_dataset import TEST_QUESTIONS


# --------------------------------------------------
# THRESHOLDS TO EVALUATE
# --------------------------------------------------

THRESHOLDS = [1.05, 1.10, 1.15, 1.20]

TOP_K = 3


# --------------------------------------------------
# RETRIEVE DOCUMENTS ONCE PER QUESTION
# --------------------------------------------------

print("Retrieving documents for evaluation questions...")

retrieval_results = {}

for test_case in TEST_QUESTIONS:

    question = test_case["question"]

    results = retrieve_documents(
        query=question,
        k=TOP_K
    )

    retrieval_results[test_case["id"]] = results

print("Retrieval completed.\n")


# --------------------------------------------------
# EVALUATE EACH THRESHOLD
# --------------------------------------------------

evaluation_results = []

for threshold in THRESHOLDS:

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for test_case in TEST_QUESTIONS:

        question_id = test_case["id"]
        expected = test_case["expected"]

        retrieved_documents = retrieval_results[question_id]

        # Accept if at least one retrieved document
        # passes the threshold.

        accepted_documents = [
            (doc, score)
            for doc, score in retrieved_documents
            if score <= threshold
        ]

        predicted_in_scope = bool(accepted_documents)

        actual_in_scope = expected == "in_scope"

        if threshold == 1.15:
            print("\n" + "=" * 80)
            print(f"QUESTION ID: {question_id}")
            print(f"QUESTION: {test_case['question']}")
            print(f"EXPECTED: {expected}")
            print(
                f"PREDICTED: "
                f"{'in_scope' if predicted_in_scope else 'out_of_scope'}"
            )
            print(
                f"RETRIEVAL DISTANCES: "
                f"{[round(score, 4) for _, score in retrieved_documents]}"
            )
            print(
                f"ACCEPTED DISTANCES: "
                f"{[round(score, 4) for _, score in accepted_documents]}"
            )
            print("=" * 80)

        if actual_in_scope and predicted_in_scope:
            TP += 1

        elif not actual_in_scope and predicted_in_scope:
            FP += 1

        elif not actual_in_scope and not predicted_in_scope:
            TN += 1

        elif actual_in_scope and not predicted_in_scope:
            FN += 1

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    precision = TP / (TP + FP) if (TP + FP) else 0

    recall = TP / (TP + FN) if (TP + FN) else 0

    specificity = TN / (TN + FP) if (TN + FP) else 0

    accuracy = (
        (TP + TN) / (TP + TN + FP + FN)
        if (TP + TN + FP + FN)
        else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0
    )

    evaluation_results.append({
        "Threshold": threshold,
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN,
        "Precision": precision,
        "Recall": recall,
        "Specificity": specificity,
        "Accuracy": accuracy,
        "F1": f1
    })


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

df = pd.DataFrame(evaluation_results)

print("\nTHRESHOLD EVALUATION RESULTS\n")

print(
    df.round(4).to_string(index=False)
)


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

df.to_csv(
    "threshold_evaluation_results.csv",
    index=False
)

print("\nResults saved to threshold_evaluation_results.csv")