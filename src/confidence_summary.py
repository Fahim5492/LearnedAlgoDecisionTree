import csv
import matplotlib.pyplot as plt


# Load confidence-analysis results from CSV
def load_results(file_path):
    rows = []

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append({
                "phase": row["phase"],
                "confidence": float(row["confidence"]),
                "correct": int(row["correct"])
            })

    return rows


# Summarize one workload phase
def summarize_phase(rows, phase):
    phase_rows = [
        row for row in rows
        if row["phase"] == phase
    ]

    total = len(phase_rows)

    correct_rows = [
        row for row in phase_rows
        if row["correct"] == 1
    ]

    wrong_rows = [
        row for row in phase_rows
        if row["correct"] == 0
    ]

    agreement = (
        len(correct_rows) / total
        if total > 0
        else 0
    )

    average_confidence = (
        sum(row["confidence"] for row in phase_rows) / total
        if total > 0
        else 0
    )

    average_correct_confidence = (
        sum(row["confidence"] for row in correct_rows)
        / len(correct_rows)
        if correct_rows
        else 0
    )

    average_wrong_confidence = (
        sum(row["confidence"] for row in wrong_rows)
        / len(wrong_rows)
        if wrong_rows
        else 0
    )

    return {
        "total": total,
        "correct": len(correct_rows),
        "wrong": len(wrong_rows),
        "agreement": agreement,
        "average_confidence": average_confidence,
        "correct_confidence": average_correct_confidence,
        "wrong_confidence": average_wrong_confidence
    }


# Save confidence summary to CSV
def save_summary_csv(locality_result, random_result, output_file):
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "phase",
            "total_decisions",
            "correct_matches",
            "incorrect_matches",
            "optimal_victim_agreement",
            "average_confidence",
            "average_confidence_when_correct",
            "average_confidence_when_incorrect"
        ])

        writer.writerow([
            "locality",
            locality_result["total"],
            locality_result["correct"],
            locality_result["wrong"],
            round(locality_result["agreement"], 4),
            round(locality_result["average_confidence"], 4),
            round(locality_result["correct_confidence"], 4),
            round(locality_result["wrong_confidence"], 4)
        ])

        writer.writerow([
            "random",
            random_result["total"],
            random_result["correct"],
            random_result["wrong"],
            round(random_result["agreement"], 4),
            round(random_result["average_confidence"], 4),
            round(random_result["correct_confidence"], 4),
            round(random_result["wrong_confidence"], 4)
        ])


# Generate confidence comparison chart
def plot_confidence_summary(
    locality_result,
    random_result,
    output_file
):
    phases = [
        "Locality-heavy",
        "Random"
    ]

    agreement_values = [
        locality_result["agreement"],
        random_result["agreement"]
    ]

    average_confidence_values = [
        locality_result["average_confidence"],
        random_result["average_confidence"]
    ]

    correct_confidence_values = [
        locality_result["correct_confidence"],
        random_result["correct_confidence"]
    ]

    wrong_confidence_values = [
        locality_result["wrong_confidence"],
        random_result["wrong_confidence"]
    ]

    x_positions = [0, 1]
    width = 0.18

    bar1_positions = [
        x - 1.5 * width
        for x in x_positions
    ]

    bar2_positions = [
        x - 0.5 * width
        for x in x_positions
    ]

    bar3_positions = [
        x + 0.5 * width
        for x in x_positions
    ]

    bar4_positions = [
        x + 1.5 * width
        for x in x_positions
    ]

    plt.figure(figsize=(12, 6))

    agreement_bars = plt.bar(
        bar1_positions,
        agreement_values,
        width=width,
        label="Optimal-Victim Agreement",
        color="blue"
    )

    average_confidence_bars = plt.bar(
        bar2_positions,
        average_confidence_values,
        width=width,
        label="Average Confidence",
        color="red"
    )

    correct_confidence_bars = plt.bar(
        bar3_positions,
        correct_confidence_values,
        width=width,
        label="Confidence When Correct",
        color="green"
    )

    wrong_confidence_bars = plt.bar(
        bar4_positions,
        wrong_confidence_values,
        width=width,
        label="Confidence When Incorrect",
        color="orange"
    )

    plt.xticks(
        x_positions,
        phases
    )

    plt.ylabel("Value")
    plt.xlabel("Workload Phase")

    plt.title(
        "Learned Policy Agreement and Confidence Across Workload Shift"
    )

    plt.ylim(0, 1)
    plt.legend()

    plt.bar_label(
        agreement_bars,
        fmt="%.3f",
        padding=3
    )

    plt.bar_label(
        average_confidence_bars,
        fmt="%.3f",
        padding=3
    )

    plt.bar_label(
        correct_confidence_bars,
        fmt="%.3f",
        padding=3
    )

    plt.bar_label(
        wrong_confidence_bars,
        fmt="%.3f",
        padding=3
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300
    )

    plt.close()


# Main execution starts here
if __name__ == "__main__":

    rows = load_results(
        "results/confidence_results.csv"
    )

    locality_result = summarize_phase(
        rows,
        "locality"
    )

    random_result = summarize_phase(
        rows,
        "random"
    )

    print("\nLOCALITY PHASE")
    print("Total decisions:", locality_result["total"])
    print("Correct matches:", locality_result["correct"])
    print("Incorrect matches:", locality_result["wrong"])

    print(
        "Optimal-victim agreement:",
        round(locality_result["agreement"], 4)
    )

    print(
        "Average confidence:",
        round(locality_result["average_confidence"], 4)
    )

    print(
        "Average confidence when correct:",
        round(locality_result["correct_confidence"], 4)
    )

    print(
        "Average confidence when incorrect:",
        round(locality_result["wrong_confidence"], 4)
    )

    print("\nRANDOM PHASE")
    print("Total decisions:", random_result["total"])
    print("Correct matches:", random_result["correct"])
    print("Incorrect matches:", random_result["wrong"])

    print(
        "Optimal-victim agreement:",
        round(random_result["agreement"], 4)
    )

    print(
        "Average confidence:",
        round(random_result["average_confidence"], 4)
    )

    print(
        "Average confidence when correct:",
        round(random_result["correct_confidence"], 4)
    )

    print(
        "Average confidence when incorrect:",
        round(random_result["wrong_confidence"], 4)
    )

    save_summary_csv(
        locality_result,
        random_result,
        "results/confidence_summary.csv"
    )

    plot_confidence_summary(
        locality_result,
        random_result,
        "results/confidence_summary_chart.png"
    )

    print("\nSaved files:")
    print("results/confidence_summary.csv")
    print("results/confidence_summary_chart.png")
