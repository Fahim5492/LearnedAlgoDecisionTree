import csv
import matplotlib.pyplot as plt


# Load evaluation results from CSV
def load_results(file_path):
    rows = []

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append({
                "seed": int(row["seed"]),
                "policy": row["policy"],
                "phase": row["phase"],
                "hits": int(row["hits"]),
                "faults": int(row["faults"]),
                "hit_ratio": float(row["hit_ratio"])
            })

    return rows


# Compute average metrics by policy and phase
def compute_averages(rows):
    grouped = {}

    for row in rows:
        key = (row["policy"], row["phase"])

        if key not in grouped:
            grouped[key] = {
                "hit_ratio_sum": 0.0,
                "faults_sum": 0.0,
                "count": 0
            }

        grouped[key]["hit_ratio_sum"] += row["hit_ratio"]
        grouped[key]["faults_sum"] += row["faults"]
        grouped[key]["count"] += 1

    summary = {}

    for key, values in grouped.items():
        summary[key] = {
            "avg_hit_ratio": (
                values["hit_ratio_sum"] / values["count"]
            ),
            "avg_faults": (
                values["faults_sum"] / values["count"]
            )
        }

    return summary


# Save averaged results as a CSV table
def save_summary_table(summary, output_file):
    policies = [
        "FIFO",
        "LRU",
        "OPTIMAL",
        "LEARNED"
    ]

    phases = [
        "locality",
        "random",
        "overall"
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "policy",
            "phase",
            "average_hit_ratio",
            "average_faults"
        ])

        for policy in policies:
            for phase in phases:
                values = summary[(policy, phase)]

                writer.writerow([
                    policy,
                    phase,
                    round(values["avg_hit_ratio"], 4),
                    round(values["avg_faults"], 2)
                ])


# Plot average hit ratio for locality and random phases
def plot_hit_ratio_comparison(summary, output_file):
    policies = [
        "FIFO",
        "LRU",
        "OPTIMAL",
        "LEARNED"
    ]

    locality_values = [
        summary[(policy, "locality")]["avg_hit_ratio"]
        for policy in policies
    ]

    random_values = [
        summary[(policy, "random")]["avg_hit_ratio"]
        for policy in policies
    ]

    x_positions = list(range(len(policies)))
    width = 0.35

    left_positions = [
        x - width / 2
        for x in x_positions
    ]

    right_positions = [
        x + width / 2
        for x in x_positions
    ]

    plt.figure(figsize=(10, 6))

    locality_bars = plt.bar(
        left_positions,
        locality_values,
        width=width,
        label="Locality-heavy",
        color="blue"
    )

    random_bars = plt.bar(
        right_positions,
        random_values,
        width=width,
        label="Random",
        color="red"
    )

    plt.xticks(
        x_positions,
        policies
    )

    plt.ylabel("Average Hit Ratio")
    plt.xlabel("Page Replacement Policy")
    plt.title("Average Hit Ratio Before and After Workload Shift")
    plt.ylim(0, 1)
    plt.legend()

    plt.bar_label(
        locality_bars,
        fmt="%.3f",
        padding=3
    )

    plt.bar_label(
        random_bars,
        fmt="%.3f",
        padding=3
    )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


# Plot overall average page faults
def plot_page_fault_comparison(summary, output_file):
    policies = [
        "FIFO",
        "LRU",
        "OPTIMAL",
        "LEARNED"
    ]

    overall_faults = [
        summary[(policy, "overall")]["avg_faults"]
        for policy in policies
    ]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        policies,
        overall_faults,
        color="blue"
    )

    plt.ylabel("Average Page Faults")
    plt.xlabel("Page Replacement Policy")
    plt.title("Overall Average Page Faults by Policy")

    plt.bar_label(
        bars,
        fmt="%.1f",
        padding=3
    )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


# Main execution starts here
if __name__ == "__main__":

    input_file = "results/results.csv"

    output_hit_ratio = "results/hit_ratio_comparison.png"
    output_page_faults = "results/page_fault_comparison.png"
    output_summary = "results/summary_table.csv"

    rows = load_results(input_file)
    summary = compute_averages(rows)

    save_summary_table(summary, output_summary)
    plot_hit_ratio_comparison(summary, output_hit_ratio)
    plot_page_fault_comparison(summary, output_page_faults)

    print("Charts and summary table created.")

    print("\nSaved files:")
    print(output_hit_ratio)
    print(output_page_faults)
    print(output_summary)
