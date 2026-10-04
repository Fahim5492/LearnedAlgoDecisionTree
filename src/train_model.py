import csv
import random

from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report


# Load dataset from CSV
def load_dataset(file_path):
    rows = []

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append({
                "trace_id": int(row["trace_id"]),
                "workload_type": row["workload_type"],
                "recency": int(row["recency"]),
                "recent_frequency": int(row["recent_frequency"]),
                "label": int(row["label"])
            })

    return rows


# Split complete traces into training and validation sets
def split_by_trace(rows, seed=42):
    rng = random.Random(seed)

    traces_by_type = {}

    for row in rows:
        workload_type = row["workload_type"]
        trace_id = row["trace_id"]

        if workload_type not in traces_by_type:
            traces_by_type[workload_type] = set()

        traces_by_type[workload_type].add(trace_id)

    validation_trace_ids = set()

    for workload_type, trace_ids in traces_by_type.items():
        trace_ids = list(trace_ids)
        rng.shuffle(trace_ids)

        # Hold out one complete trace from each workload type
        validation_trace_ids.add(trace_ids[0])

    training_rows = []
    validation_rows = []

    for row in rows:
        if row["trace_id"] in validation_trace_ids:
            validation_rows.append(row)
        else:
            training_rows.append(row)

    return training_rows, validation_rows, validation_trace_ids


# Convert rows into model features and labels
def prepare_features(rows):
    features = []
    labels = []

    for row in rows:
        features.append([
            row["recency"],
            row["recent_frequency"]
        ])

        labels.append(row["label"])

    return features, labels


# Train the Decision Tree
def train_decision_tree(x_train, y_train):
    model = DecisionTreeClassifier(
        max_depth=5,
        class_weight="balanced",
        random_state=42
    )

    model.fit(x_train, y_train)

    return model


# Main execution starts here
if __name__ == "__main__":
    rows = load_dataset(
        "data/training_data.csv"
    )

    training_rows, validation_rows, validation_trace_ids = split_by_trace(
        rows
    )

    x_train, y_train = prepare_features(training_rows)
    x_validation, y_validation = prepare_features(validation_rows)

    model = train_decision_tree(
        x_train,
        y_train
    )

    predictions = model.predict(
        x_validation
    )

    accuracy = accuracy_score(
        y_validation,
        predictions
    )

    print("Decision Tree training complete.")

    print("\nTraining examples:", len(training_rows))
    print("Validation examples:", len(validation_rows))

    print(
        "Held-out trace IDs:",
        sorted(validation_trace_ids)
    )

    print("\nValidation Accuracy:", round(accuracy, 4))

    print("\nClassification Report:")
    print(
        classification_report(
            y_validation,
            predictions,
            digits=4
        )
    )

    print("\nFeature Importance:")
    print(
        "Recency:",
        round(model.feature_importances_[0], 4)
    )

    print(
        "Recent Frequency:",
        round(model.feature_importances_[1], 4)
    )

    print("\nLearned Tree Rules:")
    print(
        export_text(
            model,
            feature_names=[
                "recency",
                "recent_frequency"
            ]
        )
    )
