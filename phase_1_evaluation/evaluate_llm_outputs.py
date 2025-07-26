import os
import pandas as pd
import numpy as np
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from openai import OpenAI
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import RESPONSES_DIR, OUTPUTS_DIR, DATA_DIR, DOMAINS, OPENAI_API_KEY, EMBEDDING_MODEL, NLI_MODEL, DOMAIN_THRESHOLDS

CACHE_FILE = os.path.join(OUTPUTS_DIR, "factcheck_cache.json")
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        factcheck_cache = json.load(f)
else:
    factcheck_cache = {}

embedder = SentenceTransformer(EMBEDDING_MODEL)
tokenizer = AutoTokenizer.from_pretrained(NLI_MODEL)
nli_model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL)
client = OpenAI(api_key=OPENAI_API_KEY)
FACTCHECK_MODEL = "gpt-4o"

def fuzzy_match(a, b):
    return fuzz.ratio(a, b)

def embedding_similarity(a, b):
    vecs = embedder.encode([a, b])
    return cosine_similarity([vecs[0]], [vecs[1]])[0][0]

def nli_entailment(premise, hypothesis):
    inputs = tokenizer(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = nli_model(**inputs).logits
    probs = torch.softmax(logits, dim=1)
    labels = ["entailment", "neutral", "contradiction"]
    return labels[probs.argmax().item()]

def fact_check_llm(question, response):
    key = f"{question} ||| {response}"
    if key in factcheck_cache:
        return factcheck_cache[key]

    prompt = (
        f"Question: {question}\n"
        f"Answer: {response}\n"
        f"Is the answer factual and grounded in reality? Just reply Yes or No."
    )
    try:
        reply = client.chat.completions.create(
            model=FACTCHECK_MODEL,
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        result = reply.choices[0].message.content.strip()
        factcheck_cache[key] = result

        with open(CACHE_FILE, "w") as f:
            json.dump(factcheck_cache, f, indent=2)

        return result
    except Exception as e:
        print(f"Fact-checker error: {e}")
        return "Error"

def evaluate_row(row, fuzzy_thresh, embed_thresh):
    q = row["question"]
    g = row["ground_truth"]
    r = row["llm_response"]

    fuzzy_score = fuzzy_match(g, r)
    fuzzy_verdict = "Yes" if fuzzy_score >= fuzzy_thresh else "No"

    embed_score = embedding_similarity(g, r)
    embed_verdict = "Yes" if embed_score >= embed_thresh else "No"

    nli_result = nli_entailment(g, r)
    nli_verdict = "Yes" if nli_result == "entailment" else "No"

    factcheck = fact_check_llm(q, r)
    factcheck_verdict = "Yes" if "yes" in factcheck.lower() else "No"

    return pd.Series([fuzzy_score, fuzzy_verdict, embed_score, embed_verdict, nli_result, nli_verdict, factcheck_verdict])

def process_domain(domain):
    input_path = os.path.join(RESPONSES_DIR, f"{domain}_dataset_with_llm.csv")
    output_path = os.path.join(OUTPUTS_DIR, f"{domain}_evaluated.csv")
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    df = pd.read_csv(input_path)
    print(f"Evaluating domain: {domain} with {len(df)} rows")

    thresholds = DOMAIN_THRESHOLDS[domain]
    fuzzy_thresh = thresholds["fuzzy"]
    embed_thresh = thresholds["embedding"]

    eval_df = df.copy()
    eval_cols = ["fuzzy_score", "fuzzy_verdict", "embedding_score", "embedding_verdict",
                 "nli_score", "nli_verdict", "factcheck_verdict"]

    eval_df[eval_cols] = df.apply(lambda row: evaluate_row(row, fuzzy_thresh, embed_thresh), axis=1)

    eval_df.to_csv(output_path, index=False)
    print(f"Saved evaluated results for '{domain}' to: {output_path}\n")

if __name__ == "__main__":
    for domain in DOMAINS:
        process_domain(domain)
