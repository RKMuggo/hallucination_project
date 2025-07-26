import pandas as pd
import json
import os

base_path = "synthetic_dataset"

trigger_files = {
    "fictional_location": os.path.join(base_path, "fictional_location.jsonl"),
    "contradiction": os.path.join(base_path, "contradiction.jsonl"),
    "entity_swap": os.path.join(base_path, "entity_swap.jsonl"),
    "impossible_timeline": os.path.join(base_path, "impossible_timeline.jsonl")
}

rows = []

for trigger_type, filepath in trigger_files.items():
    with open(filepath, "r") as f:
        for line in f:
            item = json.loads(line)
            rows.append({
                "question": item["question"],
                "ground_truth": item["ground_truth"],
                "trigger_type": trigger_type
            })

df = pd.DataFrame(rows)
output_path = "inputs/synthetic_dataset.csv"
df.to_csv(output_path, index=False)
print(f"Saved: {output_path}")