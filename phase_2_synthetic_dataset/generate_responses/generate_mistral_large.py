import requests
import os
from tqdm import tqdm
from helpers import load_all_prompts, save_responses_to_csv

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
API_URL = "https://api.mistral.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def generate_response(prompt, model):
    try:
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }
        res = requests.post(API_URL, headers=HEADERS, json=data)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] {str(e)}"

if __name__ == "__main__":
    model = "mistral-large-latest"
    prompts = load_all_prompts()
    results = []
    for p in tqdm(prompts, desc=f"Generating with {model}"):
        response = generate_response(p["question"], model)
        p["llm_response"] = response
        p["llm_model"] = model
        results.append(p)
    save_responses_to_csv(model, results)