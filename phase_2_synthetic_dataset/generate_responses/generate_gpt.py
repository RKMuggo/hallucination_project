import os
from openai import OpenAI
from tqdm import tqdm
from helpers import load_all_prompts, save_responses_to_csv
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt, model):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[ERROR] {str(e)}"

if __name__ == "__main__":
    prompts = load_all_prompts()
    
    for model in ["gpt-4o", "gpt-3.5-turbo"]:
        results = []
        for p in tqdm(prompts, desc=f"Generating with {model}"):
            response = generate_response(p["question"], model)
            p["llm_response"] = response
            p["llm_model"] = model
            results.append(p)
        save_responses_to_csv(model, results)