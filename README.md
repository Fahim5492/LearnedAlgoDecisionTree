# Learned Page Replacement Using a Decision Tree

This is my term paper project on page replacement under changing workloads for the course "CSE-307: Operating Systems" at the "Military Institute of Science and Technology".

The project implements FIFO, LRU, Optimal, and a Decision Tree based learned replacement policy. It also includes workload generation, model training, evaluation, confidence analysis, Belady anomaly testing, result plots, the final term paper, and the demo walkthrough.

## Directory Structure

```text
LearnedAlgoDecisionTree/
├── src/
│   ├── fifo.py
│   ├── lru.py
│   ├── optimal.py
│   ├── learned.py
│   ├── workload.py
│   ├── generate_dataset.py
│   ├── train_model.py
│   ├── save_model.py
│   ├── experiment.py
│   ├── evaluate.py
│   ├── confidence_analysis.py
│   ├── confidence_summary.py
│   ├── demo.py
│   ├── belady_test.py
│   └── plot_results.py
│
├── data/
│   └── training_data.csv
│
├── models/
│   └── decision_tree.joblib
│
├── results/
│   ├── results.csv
│   ├── confidence_results.csv
│   ├── summary_table.csv
│   ├── confidence_summary.csv
│   ├── hit_ratio_comparison.png
│   ├── page_fault_comparison.png
│   └── confidence_summary_chart.png
│
├── report/
│   ├── Term_Paper.pdf
│   └── Walkthrough.pdf
│
├── .gitignore
└── README.md
```

## Requirements

- Python 3
- Git
- scikit-learn
- joblib
- matplotlib

## Setup

Clone the repository:

```bash
git clone https://github.com/Fahim5492/LearnedAlgoDecisionTree.git
cd LearnedAlgoDecisionTree
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required libraries:

```bash
python3 -m pip install scikit-learn joblib matplotlib
```

## Manual Simulation

Run all four page replacement policies using a manually entered reference string and frame count:

```bash
python3 src/demo.py
```

## Belady Anomaly Test

Run the Belady anomaly test using either the classic reference string or a custom trace:

```bash
python3 src/belady_test.py
```

## Main Workload-Shift Experiment

```bash
python3 src/experiment.py
```

## Multi-Seed Evaluation

```bash
python3 src/evaluate.py
```

Output:

```text
results/results.csv
```

## Confidence Analysis

Generate decision-level confidence results:

```bash
python3 src/confidence_analysis.py
```

Output:

```text
results/confidence_results.csv
```

Generate the confidence summary and chart:

```bash
python3 src/confidence_summary.py
```

Outputs:

```text
results/confidence_summary.csv
results/confidence_summary_chart.png
```

## Generate Result Plots

```bash
python3 src/plot_results.py
```

Outputs:

```text
results/hit_ratio_comparison.png
results/page_fault_comparison.png
results/summary_table.csv
```

## Decision Tree Training

Regenerate the training dataset:

```bash
python3 src/generate_dataset.py
```

Train and validate the Decision Tree:

```bash
python3 src/train_model.py
```

Train and save the final model:

```bash
python3 src/save_model.py
```

Saved model:

```text
models/decision_tree.joblib
```

## Full Reproduction

```bash
python3 src/generate_dataset.py
python3 src/train_model.py
python3 src/save_model.py
python3 src/experiment.py
python3 src/evaluate.py
python3 src/confidence_analysis.py
python3 src/confidence_summary.py
python3 src/plot_results.py
```

## Documentation

Term paper:

```text
report/Term_Paper.pdf
```

Demo walkthrough:

```text
report/Walkthrough.pdf
```

## AI Assistance Disclosure

ChatGPT with "GPT-5.6 Sol" was used for implementation guidance, debugging support, code review, and documentation assistance.

The author conducted the experimental evaluation, validation, interpretation of the results, and preparation of the final submission.
