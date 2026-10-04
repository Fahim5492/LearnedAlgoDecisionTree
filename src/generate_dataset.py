import csv

from workload import generate_training_traces


# Find the victim that Optimal would evict
def choose_optimal_victim(frames, reference_string, current_step):
    future = reference_string[current_step + 1:]

    victim = None
    farthest_distance = -1

    for page in frames:

        if page not in future:
            return page

        next_use = future.index(page)

        if next_use > farthest_distance:
            farthest_distance = next_use
            victim = page

    return victim


# Count how often a page appeared in the recent access window
def recent_frequency(reference_string, current_step, page, window_size):
    start = max(0, current_step - window_size)
    recent_window = reference_string[start:current_step]

    return recent_window.count(page)


# Generate labeled examples from one training trace
def extract_training_examples(
    reference_string,
    workload_type,
    trace_id,
    frame_count=4,
    window_size=50
):
    frames = []
    last_access = {}

    examples = []

    for step, requested_page in enumerate(reference_string):

        if requested_page in frames:
            last_access[requested_page] = step
            continue

        if len(frames) < frame_count:
            frames.append(requested_page)
            last_access[requested_page] = step
            continue

        optimal_victim = choose_optimal_victim(
            frames,
            reference_string,
            step
        )

        for candidate_page in frames:

            recency = step - last_access[candidate_page]

            frequency = recent_frequency(
                reference_string,
                step,
                candidate_page,
                window_size
            )

            label = 1 if candidate_page == optimal_victim else 0

            examples.append({
                "trace_id": trace_id,
                "workload_type": workload_type,
                "step": step,
                "candidate_page": candidate_page,
                "recency": recency,
                "recent_frequency": frequency,
                "label": label
            })

        frames.remove(optimal_victim)
        frames.append(requested_page)

        last_access[requested_page] = step

    return examples


# Generate the full training dataset
def generate_dataset(
    output_file="data/training_data.csv",
    traces_per_type=5,
    trace_length=2000,
    total_pages=20,
    frame_count=4,
    window_size=50,
    seed=100
):
    workloads = generate_training_traces(
        traces_per_type=traces_per_type,
        trace_length=trace_length,
        total_pages=total_pages,
        seed=seed
    )

    all_examples = []

    for trace_id, workload in enumerate(workloads):

        examples = extract_training_examples(
            reference_string=workload["trace"],
            workload_type=workload["type"],
            trace_id=trace_id,
            frame_count=frame_count,
            window_size=window_size
        )

        all_examples.extend(examples)

    fieldnames = [
        "trace_id",
        "workload_type",
        "step",
        "candidate_page",
        "recency",
        "recent_frequency",
        "label"
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(all_examples)

    return all_examples


# Main execution starts here
if __name__ == "__main__":

    examples = generate_dataset()

    positive_examples = sum(
        example["label"] == 1
        for example in examples
    )

    negative_examples = len(examples) - positive_examples

    print("Training dataset created.")
    print("Total examples:", len(examples))
    print("Evict examples:", positive_examples)
    print("Keep examples:", negative_examples)
    print("Saved to: data/training_data.csv")
