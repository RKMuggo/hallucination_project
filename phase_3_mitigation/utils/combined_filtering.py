# Post eval filtering on evaluated prompt tuned and RAG responses
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

os.chdir(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT_PATH = "config/system_prompt.txt"
INPUT_FILE = "evaluations/combined_responses_evaluated.csv"
OUTPUT_FILE = "outputs/filtered_combined_responses_evaluated.csv"
if not os.path.exists(SYSTEM_PROMPT_PATH):
    raise FileNotFoundError("Missing system prompt at config/system_prompt.txt")

with open(SYSTEM_PROMPT_PATH, "r") as f:
    system_prompt = f.read().strip()
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows")
hallucinated_mask = df["hallucination_verdict"] == "Hallucinated"
to_filter = df[hallucinated_mask].copy()
print(f"Rewriting {len(to_filter)} hallucinated responses")
new_responses = []

for _, row in tqdm(to_filter.iterrows(), total=len(to_filter), desc="Rewriting"):
    try:
        user_prompt = f"{row['question']}\n\nContext:\n{row['rag_prompt']}"

        reply = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
        )

        new_response = reply.choices[0].message.content.strip()
        new_responses.append(new_response)
    except Exception as e:
        print(f"[Error] {e}")
        new_responses.append(row["llm_response"])  # Fallback to original
df.loc[hallucinated_mask, "llm_response"] = new_responses
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Saved filtered responses to: {OUTPUT_FILE}")