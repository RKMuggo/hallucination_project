import os
import pandas as pd

EVAL_DIR = os.path.join("generate_responses", "evaluated")
OUTPUT_DIR = "leaderboard"
os.makedirs(OUTPUT_DIR, exist_ok=True)

leaderboard_data = []
categories = set()

for file in os.listdir(EVAL_DIR):
    if not file.endswith("_hallucination_scores.csv"):
        continue

    model_name = file.replace("_hallucination_scores.csv", "")
    df = pd.read_csv(os.path.join(EVAL_DIR, file))

    if 'trigger_type' not in df.columns or 'hallucination_verdict' not in df.columns:
        print(f"Skipping {file} — missing required columns.")
        continue

    total = len(df)
    hallucinated = df[df["hallucination_verdict"] == "Hallucinated"]
    total_hallucination_pct = round((len(hallucinated) / total) * 100, 2)

    row = {
        "Model": model_name,
        "Total Hallucination %": total_hallucination_pct
    }

    grouped = hallucinated["trigger_type"].value_counts(normalize=True) * 100
    for cat, pct in grouped.items():
        row[cat] = round(pct, 2)
        categories.add(cat)

    leaderboard_data.append(row)

df_leaderboard = pd.DataFrame(leaderboard_data)
for cat in categories:
    if cat not in df_leaderboard.columns:
        df_leaderboard[cat] = 0.0

df_leaderboard.sort_values("Total Hallucination %", ascending=False, inplace=True)
ordered_cols = ["Model", "Total Hallucination %"] + sorted(list(categories))
df_leaderboard = df_leaderboard[ordered_cols]

output_path = os.path.join(OUTPUT_DIR, "leaderboard.csv")
df_leaderboard.to_csv(output_path, index=False)
print(f"Leaderboard saved to {output_path}")
