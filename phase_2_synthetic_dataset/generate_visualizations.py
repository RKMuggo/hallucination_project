import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

EVAL_DIR = os.path.join("generate_responses", "evaluated")
OUTPUT_DIR = "visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(EVAL_DIR):
    if not file.endswith("_hallucination_scores.csv"):
        continue

    model_name = file.replace("_hallucination_scores.csv", "")
    df = pd.read_csv(os.path.join(EVAL_DIR, file))

    if "trigger_type" not in df.columns or "hallucination_verdict" not in df.columns:
        print(f"Skipping {file} — required columns missing.")
        continue

    hallucinated = df[df["hallucination_verdict"] == "Hallucinated"]
    counts = hallucinated["trigger_type"].value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=counts.index, y=counts.values, palette="pastel")
    plt.title(f"{model_name}: Hallucinations by Trigger Type (Count)")
    plt.ylabel("Count of Hallucinations")
    plt.xlabel("Trigger Type")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"{model_name}_hallucinations_bar.png"))
    plt.close()

stacked_data = []

for file in os.listdir(EVAL_DIR):
    if not file.endswith("_hallucination_scores.csv"):
        continue

    model_name = file.replace("_hallucination_scores.csv", "")
    df = pd.read_csv(os.path.join(EVAL_DIR, file))
    hallucinated = df[df["hallucination_verdict"] == "Hallucinated"]
    counts = hallucinated["trigger_type"].value_counts(normalize=True) * 100
    stacked_data.append(counts.rename(model_name))

df_grouped = pd.DataFrame(stacked_data).fillna(0).T
df_grouped.index.name = "Trigger_Type"
df_grouped.reset_index(inplace=True)
melted = df_grouped.melt(id_vars="Trigger_Type", var_name="Model", value_name="Percentage")
plt.figure(figsize=(10, 6))
sns.barplot(data=melted, x="Trigger_Type", y="Percentage", hue="Model")
plt.ylabel("% Hallucinations")
plt.xlabel("Trigger Type")
plt.title("Grouped Bar Chart: % Hallucinations per Trigger Type (All Models)")
plt.legend(title="Model", bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "grouped_bar_all_models.png"))
plt.close()

leaderboard_data = []

for file in os.listdir(EVAL_DIR):
    if not file.endswith("_hallucination_scores.csv"):
        continue

    model_name = file.replace("_hallucination_scores.csv", "")
    df = pd.read_csv(os.path.join(EVAL_DIR, file))
    total = len(df)
    hallucinated = df[df["hallucination_verdict"] == "Hallucinated"]
    percent = (len(hallucinated) / total) * 100 if total > 0 else 0
    leaderboard_data.append((model_name, percent))

leaderboard_df = pd.DataFrame(leaderboard_data, columns=["Model", "Hallucination %"])
leaderboard_df = leaderboard_df.sort_values(by="Hallucination %", ascending=True)
plt.figure(figsize=(8, 5))
sns.barplot(data=leaderboard_df, x="Model", y="Hallucination %", palette="crest")
plt.title("Leaderboard: % Total Hallucinations per Model")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "leaderboard_hallucinations.png"))
plt.close()