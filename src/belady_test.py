from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement
from learned import build_learned_model, learned_page_replacement


# Run one policy across multiple frame counts
def test_policy(
    policy_name,
    policy_function,
    reference_string,
    frame_counts,
    model=None
):
    results = []
    previous_faults = None

    for frame_count in frame_counts:

        if policy_name == "LEARNED":
            result = policy_function(
                reference_string,
                frame_count,
                model
            )
        else:
            result = policy_function(
                reference_string,
                frame_count
            )

        faults = result["faults"]

        anomaly = (
            previous_faults is not None
            and faults > previous_faults
        )

        results.append({
            "frames": frame_count,
            "faults": faults,
            "hits": result["hits"],
            "hit_ratio": result["hit_ratio"],
            "anomaly": anomaly
        })

        previous_faults = faults

    return results


# Print results for one policy
def print_policy_results(policy_name, results):
    print(f"\n{policy_name}")

    print(
        f"{'Frames':<10}"
        f"{'Faults':<10}"
        f"{'Hits':<10}"
        f"{'Hit Ratio':<12}"
        f"{'Anomaly'}"
    )

    for row in results:
        anomaly_text = "YES" if row["anomaly"] else "NO"

        print(
            f"{row['frames']:<10}"
            f"{row['faults']:<10}"
            f"{row['hits']:<10}"
            f"{row['hit_ratio']:<12.4f}"
            f"{anomaly_text}"
        )


# Main execution starts here
if __name__ == "__main__":

    classic_trace = [
        1, 2, 3, 4,
        1, 2, 5,
        1, 2, 3, 4, 5
    ]

    print("Belady Anomaly Test")

    print("\nChoose reference string:")
    print("1. Classic Belady anomaly trace")
    print("2. Enter custom trace")

    choice = input("\nChoice: ").strip()

    if choice == "1":
        reference_string = classic_trace

        print("\nUsing classic trace:")
        print(reference_string)

    elif choice == "2":
        reference_input = input(
            "\nEnter page references separated by spaces:\n"
        )

        try:
            reference_string = [
                int(page)
                for page in reference_input.split()
            ]
        except ValueError:
            print("Reference string must contain integers only.")
            raise SystemExit

        if not reference_string:
            print("Reference string cannot be empty.")
            raise SystemExit

    else:
        print("Invalid choice.")
        raise SystemExit

    frame_input = input(
        "\nEnter frame counts separated by spaces "
        "(example: 2 3 4 5 6):\n"
    )

    try:
        frame_counts = [
            int(frame)
            for frame in frame_input.split()
        ]
    except ValueError:
        print("Frame counts must contain integers only.")
        raise SystemExit

    if not frame_counts:
        print("At least one frame count is required.")
        raise SystemExit

    if any(frame <= 0 for frame in frame_counts):
        print("Frame counts must be greater than zero.")
        raise SystemExit

    frame_counts = sorted(set(frame_counts))

    model = build_learned_model()

    print("\nReference String:", reference_string)

    policies = [
        (
            "FIFO",
            fifo_page_replacement
        ),
        (
            "LRU",
            lru_page_replacement
        ),
        (
            "OPTIMAL",
            optimal_page_replacement
        ),
        (
            "LEARNED",
            learned_page_replacement
        )
    ]

    for policy_name, policy_function in policies:

        results = test_policy(
            policy_name,
            policy_function,
            reference_string,
            frame_counts,
            model
        )

        print_policy_results(
            policy_name,
            results
        )
