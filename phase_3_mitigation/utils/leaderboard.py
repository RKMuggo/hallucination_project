import os
import pandas as pd

input_files = {
    "evaluations/baseline_responses_evaluated.csv": "GPT-3.5 Baseline",
    "evaluations/rag_responses_evaluated.csv": "GPT-3.5 - RAG",
    "evaluations/prompt_tuned_responses_evaluated.csv": "GPT-3.5 - Prompt Tuned",
    "evaluations/filtered_responses_evaluated.csv": "GPT-3.5 - Filtered Responses",
    "evaluations/final_combined_evaluated.csv": "GPT-3.5 - Combined"
}

all_triggers = set()
for path in input_files:
    if os.path.exists(path):
        df_temp = pd.read_csv(path)
        if "trigger_type" in df_temp.columns:
            all_triggers.update(df_temp["trigger_type"].dropna().unique())

trigger_types = sorted(all_triggers)

leaderboard_rows = []

for file_path, model_name in input_files.items():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    df = pd.read_csv(file_path)

    if "hallucination_verdict" not in df.columns or "trigger_type" not in df.columns:
        print(f"Missing required columns in: {file_path}")
        continue

    total = len(df)
    hallucinated = df[df["hallucination_verdict"] == "Hallucinated"]
    halluc_percent = round(len(hallucinated) / total * 100, 2) if total > 0 else 0

    row = {"Model": model_name, "Total Hallucination %": halluc_percent}

    for trigger in trigger_types:
        trigger_df = df[df["trigger_type"] == trigger]
        trigger_total = len(trigger_df)
        trigger_halluc = len(trigger_df[trigger_df["hallucination_verdict"] == "Hallucinated"])
        trigger_percent = round(trigger_halluc / trigger_total * 100, 2) if trigger_total > 0 else 0
        row[trigger] = trigger_percent

    leaderboard_rows.append(row)
leaderboard_df = pd.DataFrame(leaderboard_rows)
leaderboard_df.sort_values(by="Total Hallucination %", ascending=False, inplace=True)
output_path = "evaluations/final_ranking.csv"
leaderboard_df.to_csv(output_path, index=False)
print(f"Saved leaderboard to {output_path}")