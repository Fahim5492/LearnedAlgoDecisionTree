from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement
from learned import build_learned_model, learned_page_replacement
from workload import generate_shift_trace


# Calculate metrics for a selected range of simulation steps
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


# Print before-shift, after-shift and overall results
def print_policy_results(name, results, shift_point, total_length):
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

    print(f"\n{name}")
    print("Phase A - Locality Heavy")
    print("Hits:", phase_a["hits"])
    print("Faults:", phase_a["faults"])
    print("Hit Ratio:", round(phase_a["hit_ratio"], 4))

    print("Phase B - Random")
    print("Hits:", phase_b["hits"])
    print("Faults:", phase_b["faults"])
    print("Hit Ratio:", round(phase_b["hit_ratio"], 4))

    print("Overall")
    print("Hits:", results["hits"])
    print("Faults:", results["faults"])
    print("Hit Ratio:", round(results["hit_ratio"], 4))


# Main execution starts here
if __name__ == "__main__":

    frame_count = 4

    workload = generate_shift_trace(
        phase_length=1000,
        total_pages=20,
        working_set_size=4,
        locality_probability=0.80,
        seed=42
    )

    reference_string = workload["full_trace"]
    shift_point = workload["shift_point"]

    model = build_learned_model()

    fifo_results = fifo_page_replacement(
        reference_string,
        frame_count
    )

    lru_results = lru_page_replacement(
        reference_string,
        frame_count
    )

    optimal_results = optimal_page_replacement(
        reference_string,
        frame_count
    )

    learned_results = learned_page_replacement(
        reference_string,
        frame_count,
        model
    )

    print("Final Workload-Shift Experiment")
    print("Frames:", frame_count)
    print("Virtual Pages: 20")
    print("Total References:", len(reference_string))
    print("Shift Point:", shift_point)

    print_policy_results(
        "FIFO",
        fifo_results,
        shift_point,
        len(reference_string)
    )

    print_policy_results(
        "LRU",
        lru_results,
        shift_point,
        len(reference_string)
    )

    print_policy_results(
        "OPTIMAL",
        optimal_results,
        shift_point,
        len(reference_string)
    )

    print_policy_results(
        "LEARNED DECISION TREE",
        learned_results,
        shift_point,
        len(reference_string)
    )
