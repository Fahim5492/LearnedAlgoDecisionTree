def optimal_page_replacement(reference_string, frame_count):
    frames = []

    hits = 0
    faults = 0

    history = []

    for step, page in enumerate(reference_string):

        if page in frames:
            hits += 1
            result = "hit"

        else:
            faults += 1
            result = "fault"

            if len(frames) < frame_count:
                frames.append(page)

            else:
                future = reference_string[step + 1:]

                farthest_distance = -1
                victim_index = -1

                for i, resident_page in enumerate(frames):

                    # If page never appears again,
                    # it is the best page to evict.
                    if resident_page not in future:
                        victim_index = i
                        break

                    # Otherwise find how far away
                    # its next use is.
                    next_use = future.index(resident_page)

                    if next_use > farthest_distance:
                        farthest_distance = next_use
                        victim_index = i

                frames.pop(victim_index)
                frames.append(page)

        history.append({
            "step": step,
            "page": page,
            "frames": frames.copy(),
            "result": result
        })

    total_references = len(reference_string)
    hit_ratio = hits / total_references

    return {
        "hits": hits,
        "faults": faults,
        "hit_ratio": hit_ratio,
        "history": history
    }


if __name__ == "__main__":
    reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    frame_count = 3

    results = optimal_page_replacement(reference_string, frame_count)

    print("OPTIMAL")
    print("Hits:", results["hits"])
    print("Page Faults:", results["faults"])
    print("Hit Ratio:", results["hit_ratio"])

    print("\nStep-by-step history:")
    for record in results["history"]:
        print(record)
