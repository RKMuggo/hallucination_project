import os
import json
import pandas as pd
from config import DATA_DIR

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return pd.DataFrame(data)

def load_csv(file_path):
    return pd.read_csv(file_path)

def load_dataset(domain: str, version: str = "v1", file_type: str = "jsonl") -> pd.DataFrame:
    file_path = os.path.join(DATA_DIR, domain, version, f"dataset.{file_type}")
    if file_type == "jsonl":
        return load_jsonl(file_path)
    elif file_type == "csv":
        return load_csv(file_path)
    else:
        raise ValueError("Unsupported file type")

if __name__ == "__main__":
    df = load_dataset("general", version="v1", file_type="jsonl")
    print(df.sample(5))
