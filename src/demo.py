from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement
from learned import build_learned_model, learned_page_replacement
from generate_dataset import choose_optimal_victim


# Print results for one replacement policy
def print_result(name, result):
    print(f"\n{name}")
    print("Hits:", result["hits"])
    print("Page Faults:", result["faults"])
    print("Hit Ratio:", round(result["hit_ratio"], 4))


# Analyze Learned policy decisions against Optimal
def analyze_confidence(reference_string, learned_result):
    decisions = []

    for record in learned_result["history"]:
        if record["victim"] is None:
            continue

        optimal_victim = choose_optimal_victim(
            record["frames_before"],
            reference_string,
            record["step"]
        )

        correct = record["victim"] == optimal_victim

        decisions.append({
            "step": record["step"],
            "requested_page": record["page"],
            "learned_victim": record["victim"],
            "optimal_victim": optimal_victim,
            "confidence": record["confidence"],
            "correct": correct
        })

    return decisions


# Print confidence-analysis results
def print_confidence_results(decisions):
    if not decisions:
        print("\nNo replacement decisions were required.")
        return

    correct_count = sum(
        decision["correct"]
        for decision in decisions
    )

    decision_accuracy = (
        correct_count / len(decisions)
    )

    correct_confidences = [
        decision["confidence"]
        for decision in decisions
        if decision["correct"]
    ]

    incorrect_confidences = [
        decision["confidence"]
        for decision in decisions
        if not decision["correct"]
    ]

    average_correct_confidence = (
        sum(correct_confidences) / len(correct_confidences)
        if correct_confidences
        else 0
    )

    average_incorrect_confidence = (
        sum(incorrect_confidences) / len(incorrect_confidences)
        if incorrect_confidences
        else 0
    )

    print("\nConfidence Analysis")
    print("Replacement Decisions:", len(decisions))
    print("Correct Decisions:", correct_count)
    print("Decision Accuracy:", round(decision_accuracy, 4))
    print(
        "Average Confidence When Correct:",
        round(average_correct_confidence, 4)
    )
    print(
        "Average Confidence When Wrong:",
        round(average_incorrect_confidence, 4)
    )

    print("\nIndividual Learned Decisions")

    for decision in decisions:
        status = "CORRECT" if decision["correct"] else "WRONG"

        print(
            f"Step {decision['step']} | "
            f"Requested: {decision['requested_page']} | "
            f"Learned: {decision['learned_victim']} | "
            f"Optimal: {decision['optimal_victim']} | "
            f"Confidence: {decision['confidence']:.4f} | "
            f"{status}"
        )


# Main execution starts here
if __name__ == "__main__":

    print("Page Replacement Simulator")

    reference_input = input(
        "\nEnter page references separated by spaces:\n"
    )

    reference_string = [
        int(page)
        for page in reference_input.split()
    ]

    frame_count = int(
        input("\nEnter number of frames: ")
    )

    if not reference_string:
        print("Reference string cannot be empty.")
        raise SystemExit

    if frame_count <= 0:
        print("Frame count must be greater than zero.")
        raise SystemExit

    model = build_learned_model()

    fifo_result = fifo_page_replacement(
        reference_string,
        frame_count
    )

    lru_result = lru_page_replacement(
        reference_string,
        frame_count
    )

    optimal_result = optimal_page_replacement(
        reference_string,
        frame_count
    )

    learned_result = learned_page_replacement(
        reference_string,
        frame_count,
        model
    )

    print("\nResults")

    print_result("FIFO", fifo_result)
    print_result("LRU", lru_result)
    print_result("OPTIMAL", optimal_result)
    print_result("LEARNED DECISION TREE", learned_result)

    confidence_decisions = analyze_confidence(
        reference_string,
        learned_result
    )

    print_confidence_results(
        confidence_decisions
    )
