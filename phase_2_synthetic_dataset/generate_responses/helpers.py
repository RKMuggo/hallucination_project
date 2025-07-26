import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def load_all_prompts(base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "synthetic_dataset"))):
    all_data = []
    for file in os.listdir(base_path):
        if file.endswith(".jsonl"):
            path = os.path.join(base_path, file)
            with open(path, "r") as f:
                for line in f:
                    data = json.loads(line)
                    all_data.append(data)
    return all_data

def save_responses_to_csv(model_name, results, save_dir="responses"):
    os.makedirs(save_dir, exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv(os.path.join(save_dir, f"{model_name}.csv"), index=False)
    print(f"Saved {len(results)} responses to {save_dir}/{model_name}.csv")
