import random


# Locality-heavy workload generator
def generate_locality_trace(
    length,
    total_pages,
    working_set_size,
    locality_probability=0.80,
    rng=None
):
    """Generate a locality-heavy page-reference trace."""

    if rng is None:
        rng = random.Random()

    all_pages = list(range(total_pages))
    working_set = rng.sample(all_pages, working_set_size)

    cold_pages = [
        page for page in all_pages
        if page not in working_set
    ]

    trace = []

    for _ in range(length):
        if rng.random() < locality_probability:
            page = rng.choice(working_set)
        else:
            page = rng.choice(cold_pages) if cold_pages else rng.choice(working_set)

        trace.append(page)

    return trace


# Random workload generator
def generate_random_trace(
    length,
    total_pages,
    rng=None
):
    """Generate a uniformly random page-reference trace."""

    if rng is None:
        rng = random.Random()

    return [
        rng.randrange(total_pages)
        for _ in range(length)
    ]


# Sequential workload generator
def generate_sequential_trace(
    length,
    total_pages,
    rng=None
):
    """Generate sequential page accesses with wrap-around."""

    if rng is None:
        rng = random.Random()

    start_page = rng.randrange(total_pages)

    return [
        (start_page + i) % total_pages
        for i in range(length)
    ]


# Bursty workload generator
def generate_bursty_trace(
    length,
    total_pages,
    min_burst_length=10,
    max_burst_length=40,
    min_hot_set_size=2,
    max_hot_set_size=5,
    burst_locality_probability=0.90,
    rng=None
):
    """Generate a workload with changing short-term hot page sets."""

    if rng is None:
        rng = random.Random()

    trace = []
    all_pages = list(range(total_pages))

    while len(trace) < length:
        hot_set_size = rng.randint(
            min_hot_set_size,
            min(max_hot_set_size, total_pages)
        )

        hot_set = rng.sample(
            all_pages,
            hot_set_size
        )

        burst_length = rng.randint(
            min_burst_length,
            max_burst_length
        )

        for _ in range(burst_length):
            if len(trace) >= length:
                break

            if rng.random() < burst_locality_probability:
                page = rng.choice(hot_set)
            else:
                page = rng.choice(all_pages)

            trace.append(page)

    return trace


# Training workload collection generator
def generate_training_traces(
    traces_per_type=5,
    trace_length=2000,
    total_pages=20,
    seed=100
):
    """Generate balanced training workloads of multiple access patterns."""

    master_rng = random.Random(seed)
    workloads = []

    for _ in range(traces_per_type):
        trace_seed = master_rng.randint(0, 1_000_000)
        rng = random.Random(trace_seed)

        working_set_size = rng.randint(3, 6)
        locality_probability = rng.uniform(0.70, 0.90)

        trace = generate_locality_trace(
            trace_length,
            total_pages,
            working_set_size,
            locality_probability,
            rng
        )

        workloads.append({
            "type": "locality",
            "trace": trace,
            "seed": trace_seed,
            "parameters": {
                "working_set_size": working_set_size,
                "locality_probability": locality_probability
            }
        })

    for _ in range(traces_per_type):
        trace_seed = master_rng.randint(0, 1_000_000)
        rng = random.Random(trace_seed)

        trace = generate_sequential_trace(
            trace_length,
            total_pages,
            rng
        )

        workloads.append({
            "type": "sequential",
            "trace": trace,
            "seed": trace_seed,
            "parameters": {}
        })

    for _ in range(traces_per_type):
        trace_seed = master_rng.randint(0, 1_000_000)
        rng = random.Random(trace_seed)

        trace = generate_random_trace(
            trace_length,
            total_pages,
            rng
        )

        workloads.append({
            "type": "random",
            "trace": trace,
            "seed": trace_seed,
            "parameters": {}
        })

    for _ in range(traces_per_type):
        trace_seed = master_rng.randint(0, 1_000_000)
        rng = random.Random(trace_seed)

        min_burst_length = rng.randint(8, 15)
        max_burst_length = rng.randint(25, 50)
        burst_probability = rng.uniform(0.80, 0.95)

        trace = generate_bursty_trace(
            trace_length,
            total_pages,
            min_burst_length,
            max_burst_length,
            burst_locality_probability=burst_probability,
            rng=rng
        )

        workloads.append({
            "type": "bursty",
            "trace": trace,
            "seed": trace_seed,
            "parameters": {
                "min_burst_length": min_burst_length,
                "max_burst_length": max_burst_length,
                "burst_locality_probability": burst_probability
            }
        })

    master_rng.shuffle(workloads)

    return workloads


# Final shifted workload generator used for evaluation
def generate_shift_trace(
    phase_length=1000,
    total_pages=20,
    working_set_size=4,
    locality_probability=0.80,
    seed=42
):
    """Generate the final locality-to-random evaluation workload."""

    rng = random.Random(seed)

    phase_a = generate_locality_trace(
        phase_length,
        total_pages,
        working_set_size,
        locality_probability,
        rng
    )

    phase_b = generate_random_trace(
        phase_length,
        total_pages,
        rng
    )

    return {
        "phase_a": phase_a,
        "phase_b": phase_b,
        "full_trace": phase_a + phase_b,
        "shift_point": phase_length,
        "seed": seed,
        "parameters": {
            "total_pages": total_pages,
            "working_set_size": working_set_size,
            "locality_probability": locality_probability
        }
    }


# Main execution starts here
if __name__ == "__main__":
    training_workloads = generate_training_traces(
        traces_per_type=2,
        trace_length=50,
        total_pages=20,
        seed=100
    )

    print("Training Workloads")

    for index, workload in enumerate(training_workloads):
        print(
            f"\nTrace {index + 1}"
            f" | Type: {workload['type']}"
            f" | Seed: {workload['seed']}"
        )

        print("First 25 references:", workload["trace"][:25])
        print("Parameters:", workload["parameters"])

    test_workload = generate_shift_trace(
        phase_length=50,
        total_pages=20,
        working_set_size=4,
        locality_probability=0.80,
        seed=42
    )

    print("\nFinal Shifted Test Workload")
    print("\nPhase A:", test_workload["phase_a"][:30])
    print("\nPhase B:", test_workload["phase_b"][:30])
    print("\nShift point:", test_workload["shift_point"])
    print("Total references:", len(test_workload["full_trace"]))
