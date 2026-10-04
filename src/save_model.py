from joblib import dump

from train_model import (
    load_dataset,
    prepare_features,
    train_decision_tree
)


# Main execution starts here
if __name__ == "__main__":

    rows = load_dataset(
        "data/training_data.csv"
    )

    features, labels = prepare_features(rows)

    model = train_decision_tree(
        features,
        labels
    )

    dump(
        model,
        "models/decision_tree.joblib"
    )

    print("Final Decision Tree model trained.")
    print("Training examples:", len(features))
    print("Saved to: models/decision_tree.joblib")
