import os
import pandas as pd

INPUT_DIR = "outputs"
OUTPUT_DIR = os.path.join("evaluations")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOMAINS = ["general", "medical", "legal", "finance"]
WEIGHTS = {
    "factcheck_verdict": 0.45,
    "embedding_score": 0.30,
    "fuzzy_score": 0.15,
    "nli_verdict": 0.10
}

FUZZY_THRESHOLDS = {
    "min_val": 0, "max_val": 100
}
EMBEDDING_THRESHOLDS = {
    "min_val": 0.5, "max_val": 0.85
}

FACTCHECK_SCORE = {"Yes": 1, "No": 0}
NLI_SCORE = {"entailment": 1, "neutral": 0.5, "contradiction": 0}

def normalize(val, min_val, max_val):
    return max(0, min(1, (val - min_val) / (max_val - min_val)))

def compute_final_score(row):
    factcheck = FACTCHECK_SCORE.get(str(row.get('factcheck_verdict', '')).strip(), 0)
    embedding = normalize(row.get('embedding_score', 0), **EMBEDDING_THRESHOLDS)
    fuzzy = normalize(row.get('fuzzy_score', 0), **FUZZY_THRESHOLDS)
    nli_raw = str(row.get('nli_score', row.get('nli_verdict', 'neutral'))).strip().lower()
    nli = NLI_SCORE.get(nli_raw, 0)
    
    return (
        WEIGHTS["factcheck_verdict"] * factcheck +
        WEIGHTS["embedding_score"] * embedding +
        WEIGHTS["fuzzy_score"] * fuzzy +
        WEIGHTS["nli_verdict"] * nli
    )

HALLUCINATION_THRESHOLD = 0.6

for domain in DOMAINS:
    path = os.path.join(INPUT_DIR, f"{domain}_evaluated.csv")
    if not os.path.exists(path):
        print(f"[!] File missing: {path}")
        continue

    df = pd.read_csv(path)
    if 'nli_score' not in df.columns and 'nli_verdict' in df.columns:
        df['nli_score'] = df['nli_verdict']
    df['final_score'] = df.apply(compute_final_score, axis=1)
    df['final_verdict'] = df['final_score'].apply(lambda x: "Hallucinated" if x < HALLUCINATION_THRESHOLD else "Not Hallucinated")
    save_path = os.path.join(OUTPUT_DIR, f"{domain}_evaluated_with_final.csv")
    df.to_csv(save_path, index=False)
    print(f"Saved final verdicts to {save_path}")