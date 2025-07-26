# Creates combined responses (after prompt tuning and RAG)
import os
import time
import pandas as pd
from openai import OpenAI

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(ROOT_DIR, "outputs", "rag_responses.csv")
PROMPT_PATH = os.path.join(ROOT_DIR, "config", "system_prompt.txt")
OUTPUT_PATH = os.path.join(ROOT_DIR, "outputs", "combined_responses.csv")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    system_prompt = f.read().strip()
df = pd.read_csv(INPUT_PATH)
df = df[["question", "ground_truth", "trigger_type", "rag_prompt"]].dropna()

client = OpenAI(api_key=" ")
model_name = "gpt-3.5-turbo"
temperature = 0
responses = []
for i, row in df.iterrows():
    prompt = row["rag_prompt"]
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = ""
    
    responses.append(reply)
    time.sleep(1)
df["llm_response"] = responses
df = df[["question", "ground_truth", "trigger_type", "rag_prompt", "llm_response"]]
df.to_csv(OUTPUT_PATH, index=False)
print(f"\nCombined prompt-tuned + RAG responses saved to: {OUTPUT_PATH}")