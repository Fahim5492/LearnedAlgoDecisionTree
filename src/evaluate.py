import csv

from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement
from learned import build_learned_model, learned_page_replacement
from workload import generate_shift_trace


# Calculate metrics for a section of one simulation
def calculate_phase_metrics(history, start_step, end_step):
    phase_history = [
        record
        for record in history
        if start_step <= record["step"] < end_step
    ]

    hits = sum(
        record["result"] == "hit"
        for record in phase_history
    )

    faults = sum(
        record["result"] == "fault"
        for record in phase_history
    )

    total = len(phase_history)
    hit_ratio = hits / total if total > 0 else 0

    return {
        "hits": hits,
        "faults": faults,
        "hit_ratio": hit_ratio
    }


# Convert one policy result into rows for CSV output
def collect_policy_rows(
    policy_name,
    seed,
    results,
    shift_point,
    total_length
):
    phase_a = calculate_phase_metrics(
        results["history"],
        0,
        shift_point
    )

    phase_b = calculate_phase_metrics(
        results["history"],
        shift_point,
        total_length
    )

    return [
        {
            "seed": seed,
            "policy": policy_name,
            "phase": "locality",
            "hits": phase_a["hits"],
            "faults": phase_a["faults"],
            "hit_ratio": phase_a["hit_ratio"]
        },
        {
            "seed": seed,
            "policy": policy_name,
            "phase": "random",
            "hits": phase_b["hits"],
            "faults": phase_b["faults"],
            "hit_ratio": phase_b["hit_ratio"]
        },
        {
            "seed": seed,
            "policy": policy_name,
            "phase": "overall",
            "hits": results["hits"],
            "faults": results["faults"],
            "hit_ratio": results["hit_ratio"]
        }
    ]


# Run all policies on one shifted workload
def run_single_seed(seed, model, frame_count=4):
    workload = generate_shift_trace(
        phase_length=1000,
        total_pages=20,
        working_set_size=4,
        locality_probability=0.80,
        seed=seed
    )

    reference_string = workload["full_trace"]
    shift_point = workload["shift_point"]

    policy_results = {
        "FIFO": fifo_page_replacement(
            reference_string,
            frame_count
        ),
        "LRU": lru_page_replacement(
            reference_string,
            frame_count
        ),
        "OPTIMAL": optimal_page_replacement(
            reference_string,
            frame_count
        ),
        "LEARNED": learned_page_replacement(
            reference_string,
            frame_count,
            model
        )
    }

    rows = []

    for policy_name, results in policy_results.items():
        rows.extend(
            collect_policy_rows(
                policy_name,
                seed,
                results,
                shift_point,
                len(reference_string)
            )
        )

    return rows


# Save all evaluation rows to CSV
def save_results(rows, output_file):
    fieldnames = [
        "seed",
        "policy",
        "phase",
        "hits",
        "faults",
        "hit_ratio"
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)


# Print average results across all seeds
def print_averages(rows):
    grouped = {}

    for row in rows:
        key = (
            row["policy"],
            row["phase"]
        )

        if key not in grouped:
            grouped[key] = {
                "hit_ratio_sum": 0,
                "faults_sum": 0,
                "count": 0
            }

        grouped[key]["hit_ratio_sum"] += row["hit_ratio"]
        grouped[key]["faults_sum"] += row["faults"]
        grouped[key]["count"] += 1

    print("\nAverage Results Across Seeds")

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

    for policy in policies:
        print(f"\n{policy}")

        for phase in phases:
            values = grouped[(policy, phase)]

            average_hit_ratio = (
                values["hit_ratio_sum"] / values["count"]
            )

            average_faults = (
                values["faults_sum"] / values["count"]
            )

            print(
                f"{phase.capitalize():10} "
                f"Hit Ratio: {average_hit_ratio:.4f} "
                f"| Avg Faults: {average_faults:.2f}"
            )


# Main execution starts here
if __name__ == "__main__":

    seeds = list(range(42, 52))
    frame_count = 4

    model = build_learned_model()

    all_rows = []

    for seed in seeds:
        print(f"Running seed {seed}...")

        rows = run_single_seed(
            seed,
            model,
            frame_count
        )

        all_rows.extend(rows)

    save_results(
        all_rows,
        "results/results.csv"
    )

    print_averages(all_rows)

    print("\nSaved detailed results to:")
    print("results/results.csv")
