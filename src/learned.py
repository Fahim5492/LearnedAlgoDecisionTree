from train_model import (
    load_dataset,
    prepare_features,
    train_decision_tree
)

from generate_dataset import recent_frequency


# Train the final model using all broad training traces
def build_learned_model(
    dataset_path="data/training_data.csv"
):
    rows = load_dataset(dataset_path)

    features, labels = prepare_features(rows)

    model = train_decision_tree(
        features,
        labels
    )

    return model


# Learned Decision Tree page-replacement policy
def learned_page_replacement(
    reference_string,
    frame_count,
    model,
    window_size=50
):
    frames = []
    last_access = {}

    hits = 0
    faults = 0

    history = []

    evict_class_index = list(
        model.classes_
    ).index(1)

    for step, requested_page in enumerate(reference_string):

        victim = None
        confidence = None
        candidate_scores = {}
        frames_before = None

        if requested_page in frames:
            hits += 1
            result = "hit"

        else:
            faults += 1
            result = "fault"

            if len(frames) < frame_count:
                frames.append(requested_page)

            else:
                candidates = frames.copy()
                frames_before = frames.copy()

                candidate_features = []
                candidate_recencies = []

                for candidate_page in candidates:
                    recency = (
                        step - last_access[candidate_page]
                    )

                    frequency = recent_frequency(
                        reference_string,
                        step,
                        candidate_page,
                        window_size
                    )

                    candidate_features.append([
                        recency,
                        frequency
                    ])

                    candidate_recencies.append(
                        recency
                    )

                probabilities = model.predict_proba(
                    candidate_features
                )

                eviction_scores = [
                    probability[evict_class_index]
                    for probability in probabilities
                ]

                for candidate_page, score in zip(
                    candidates,
                    eviction_scores
                ):
                    candidate_scores[candidate_page] = score

                best_index = max(
                    range(len(candidates)),
                    key=lambda i: (
                        eviction_scores[i],
                        candidate_recencies[i]
                    )
                )

                victim = candidates[best_index]
                confidence = eviction_scores[best_index]

                frames.remove(victim)
                frames.append(requested_page)

        last_access[requested_page] = step

        history.append({
            "step": step,
            "page": requested_page,
            "frames": frames.copy(),
            "frames_before": frames_before,
            "result": result,
            "victim": victim,
            "confidence": confidence,
            "candidate_scores": candidate_scores
        })

    total_references = len(reference_string)

    hit_ratio = (
        hits / total_references
        if total_references > 0
        else 0
    )

    return {
        "hits": hits,
        "faults": faults,
        "hit_ratio": hit_ratio,
        "history": history
    }


# Main execution starts here
if __name__ == "__main__":

    model = build_learned_model()

    reference_string = [
        1, 2, 3, 4,
        1, 2, 5,
        1, 2, 3, 4, 5
    ]

    results = learned_page_replacement(
        reference_string,
        frame_count=3,
        model=model
    )

    print("Learned Decision Tree Policy")
    print("Hits:", results["hits"])
    print("Page Faults:", results["faults"])
    print("Hit Ratio:", results["hit_ratio"])

    print("\nReplacement Decisions:")

    for record in results["history"]:
        if record["victim"] is not None:
            print(
                f"Step {record['step']}: "
                f"requested {record['page']}, "
                f"evicted {record['victim']}, "
                f"confidence {record['confidence']:.4f}"
            )
