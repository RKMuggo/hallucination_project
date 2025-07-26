import os
import time
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, DOMAINS, DATA_DIR, RESPONSES_DIR



client = OpenAI(api_key=OPENAI_API_KEY)
TEMPERATURE = OPENAI_TEMPERATURE["low"]

def generate_llm_response(question):
    prompt = f"Answer the following question concisely and factually:\n{question}"
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a factual assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "ERROR"

def process_domain(domain):
    input_path = os.path.join(DATA_DIR, domain, f"{domain}_dataset.csv")
    os.makedirs(RESPONSES_DIR, exist_ok=True)
    output_path = os.path.join(RESPONSES_DIR, f"{domain}_dataset_with_llm.csv")
    df = pd.read_csv(input_path)
    df["llm_response"] = df["question"].apply(generate_llm_response)
    df.to_csv(output_path, index=False)
    print(f"Saved LLM responses for '{domain}' to: {output_path}")

if __name__ == "__main__":
    for domain in DOMAINS:
        print(f"Processing domain: {domain}")
        process_domain(domain)
        time.sleep(1)