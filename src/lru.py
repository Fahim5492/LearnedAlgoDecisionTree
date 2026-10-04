def lru_page_replacement(reference_string, frame_count):
    frames = []

    hits = 0
    faults = 0

    history = []

    for step, page in enumerate(reference_string):

        if page in frames:
            hits += 1
            result = "hit"

            # Move recently used page to the end
            frames.remove(page)
            frames.append(page)

        else:
            faults += 1
            result = "fault"

            if len(frames) < frame_count:
                frames.append(page)

            else:
                # First item is the least recently used
                frames.pop(0)
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

    results = lru_page_replacement(reference_string, frame_count)

    print("LRU")
    print("Hits:", results["hits"])
    print("Page Faults:", results["faults"])
    print("Hit Ratio:", results["hit_ratio"])

    print("\nStep-by-step history:")
    for record in results["history"]:
        print(record)
