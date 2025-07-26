import pandas as pd
import os

INPUT_CSV_PATH = "hallucination_project/phase_1_evaluation/TruthfulQA.csv"
OUTPUT_BASE_PATH = "hallucination_project/phase_1_evaluation/data"

domains = ["medical", "legal", "finance", "general"]
for d in domains:
    os.makedirs(os.path.join(OUTPUT_BASE_PATH, d), exist_ok=True)
category_to_domain = {
    "Health": "medical",
    "Nutrition": "medical",
    "Psychology": "medical",
    "Science": "medical",
    "Law": "legal",
    "Politics": "legal",
    "Finance": "finance",
    "Economics": "finance",
    "Statistics": "finance",
    "Advertising": "general",
    "Confusion: Other": "general",
    "Confusion: People": "general",
    "Confusion: Places": "general",
    "Conspiracies": "general",
    "Distraction": "general",
    "Education": "general",
    "Fiction": "general",
    "History": "general",
    "Indexical Error: Identity": "general",
    "Indexical Error: Location": "general",
    "Indexical Error: Other": "general",
    "Language": "general",
    "Logical Falsehood": "general",
    "Mandela Effect": "general",
    "Misconceptions": "general",
    "Misconceptions: Topical": "general",
    "Misinformation": "general",
    "Misquotations": "general",
    "Myths and Fairytales": "general",
    "Paranormal": "general",
    "Proverbs": "general",
    "Religion": "general",
    "Sociology": "general",
    "Stereotypes": "general",
    "Subjective": "general",
    "Superstitions": "general",
    "Weather": "general"
}

df = pd.read_csv(INPUT_CSV_PATH)
df["domain"] = df["Category"].map(category_to_domain)
df = df.dropna(subset=["domain"])
df = df.rename(columns={
    "Question": "question",
    "Best Answer": "ground_truth"
})

for domain in domains:
    domain_df = df[df["domain"] == domain]
    output_path = os.path.join(OUTPUT_BASE_PATH, domain, f"{domain}_dataset.csv")
    domain_df[["question", "ground_truth", "domain"]].to_csv(output_path, index=False)
    print(f"Saved {len(domain_df)} samples to {output_path}")
