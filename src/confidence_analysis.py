import csv

from learned import build_learned_model, learned_page_replacement
from workload import generate_shift_trace
from generate_dataset import choose_optimal_victim


# Analyze learned decisions against Optimal decisions
def analyze_seed(seed, model, frame_count=4):
    workload = generate_shift_trace(
        phase_length=1000,
        total_pages=20,
        working_set_size=4,
        locality_probability=0.80,
        seed=seed
    )

    reference_string = workload["full_trace"]

    results = learned_page_replacement(
        reference_string,
        frame_count,
        model
    )

    rows = []

    for record in results["history"]:

        if record["victim"] is None:
            continue

        step = record["step"]
        frames_before = record["frames_before"]

        optimal_victim = choose_optimal_victim(
            frames_before,
            reference_string,
            step
        )

        correct = (
            record["victim"] == optimal_victim
        )

        phase = (
            "locality"
            if step < workload["shift_point"]
            else "random"
        )

        rows.append({
            "seed": seed,
            "step": step,
            "phase": phase,
            "learned_victim": record["victim"],
            "optimal_victim": optimal_victim,
            "confidence": record["confidence"],
            "correct": int(correct)
        })

    return rows


# Save detailed decision results
def save_results(rows, output_file):
    fieldnames = [
        "seed",
        "step",
        "phase",
        "learned_victim",
        "optimal_victim",
        "confidence",
        "correct"
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)


# Print confidence and correctness summary
def print_summary(rows):
    total = len(rows)

    correct = sum(
        row["correct"]
        for row in rows
    )

    accuracy = correct / total if total > 0 else 0

    correct_confidences = [
        row["confidence"]
        for row in rows
        if row["correct"] == 1
    ]

    incorrect_confidences = [
        row["confidence"]
        for row in rows
        if row["correct"] == 0
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
    print("Total replacement decisions:", total)
    print("Correct decisions:", correct)
    print("Decision accuracy:", round(accuracy, 4))

    print(
        "Average confidence when correct:",
        round(average_correct_confidence, 4)
    )

    print(
        "Average confidence when incorrect:",
        round(average_incorrect_confidence, 4)
    )

    phases = ["locality", "random"]

    for phase in phases:
        phase_rows = [
            row for row in rows
            if row["phase"] == phase
        ]

        phase_correct = sum(
            row["correct"]
            for row in phase_rows
        )

        phase_accuracy = (
            phase_correct / len(phase_rows)
            if phase_rows
            else 0
        )

        average_confidence = (
            sum(row["confidence"] for row in phase_rows)
            / len(phase_rows)
            if phase_rows
            else 0
        )

        print(f"\n{phase.capitalize()} Phase")
        print("Decisions:", len(phase_rows))
        print("Accuracy:", round(phase_accuracy, 4))
        print(
            "Average confidence:",
            round(average_confidence, 4)
        )


# Main execution starts here
if __name__ == "__main__":

    seeds = list(range(42, 52))

    model = build_learned_model()

    all_rows = []

    for seed in seeds:
        print(f"Analyzing seed {seed}...")

        rows = analyze_seed(
            seed,
            model,
            frame_count=4
        )

        all_rows.extend(rows)

    save_results(
        all_rows,
        "results/confidence_results.csv"
    )

    print_summary(all_rows)

    print("\nSaved detailed confidence results to:")
    print("results/confidence_results.csv")
