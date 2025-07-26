import os
import json
import glob
import pandas as pd

REQUIRED_FIELDS = [
    "question", "ground_truth", "hallucination_trigger", "trigger_type",
    "domain", "expected_behavior", "difficulty_level", "source"
]

def validate_jsonl(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    valid = 0
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            print(f"JSON decode error in {filepath}, line {i+1}")
            continue

        for field in REQUIRED_FIELDS:
            if field not in obj:
                print(f"Missing field '{field}' in {filepath}, line {i+1}")
        valid += 1

    return valid

def sample_jsonl_files(files, n=10):
    data = []
    for file in files:
        with open(file, "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except:
                    continue
    df = pd.DataFrame(data)
    sample = df.sample(n=min(n, len(df)), random_state=42)
    return sample

if __name__ == "__main__":
    path = "synthetic_dataset"
    files = glob.glob(os.path.join(path, "*.jsonl"))

    print("Validating synthetic prompt files...\n")
    total = 0
    for file in files:
        count = validate_jsonl(file)
        print(f"{file} — {count} prompts checked\n")
        total += count

    print(f"\nTotal prompts validated: {total}")

    print("\nSampling 10 random prompts across all types:\n")
    sample_df = sample_jsonl_files(files, n=10)
    print(sample_df[["question", "trigger_type", "domain"]])