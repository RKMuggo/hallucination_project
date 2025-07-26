import os
import pandas as pd
from tqdm import tqdm
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
INPUT_CSV = "inputs/synthetic_dataset.csv"
SYSTEM_PROMPT_FILE = "config/system_prompt.txt"
OUTPUT_CSV = "outputs/prompt_tuned_responses.csv"
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.0
MAX_RETRIES = 3
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
with open(SYSTEM_PROMPT_FILE, "r") as f:
    system_prompt = f.read().strip()
df = pd.read_csv(INPUT_CSV)
df["system_prompt"] = system_prompt
df["prompt_tuned_response"] = ""

def generate_response(system_msg, user_msg):
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error: {e} — retrying ({attempt + 1}/{MAX_RETRIES})")
            sleep(2)
    return "API call failed after retries"

print("Generating responses with system prompt...")
for i, row in tqdm(df.iterrows(), total=len(df)):
    user_prompt = row["question"]
    response = generate_response(system_prompt, user_prompt)
    df.at[i, "prompt_tuned_response"] = response
df[["question", "ground_truth", "system_prompt", "prompt_tuned_response"]].to_csv(OUTPUT_CSV, index=False)
print(f"Saved to {OUTPUT_CSV}")