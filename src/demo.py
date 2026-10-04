from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement
from learned import build_learned_model, learned_page_replacement


# Print results for one replacement policy
def print_result(name, result):
    print(f"\n{name}")
    print("Hits:", result["hits"])
    print("Page Faults:", result["faults"])
    print("Hit Ratio:", round(result["hit_ratio"], 4))


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
