import anthropic
import os
from tqdm import tqdm
from helpers import load_all_prompts, save_responses_to_csv

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_response(prompt):
    try:
        msg = client.messages.create(
            model = "claude-3-7-sonnet-20250219",
            max_tokens=1024,
            temperature=0,
            system="You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"[ERROR] {str(e)}"

if __name__ == "__main__":
    prompts = load_all_prompts()
    results = []
    for p in tqdm(prompts, desc="Generating with Claude 3 Sonnet"):
        response = generate_response(p["question"])
        p["llm_response"] = response
        p["llm_model"] = "claude-3-7-sonnet-20250219"
        results.append(p)
    save_responses_to_csv("claude-3-sonnet", results)