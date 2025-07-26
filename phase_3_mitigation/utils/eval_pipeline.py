import os
import pandas as pd
import json
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set. Set it in .env or export it in the shell.")

CACHE_FILE = "factcheck_cache.json"
FACTCHECK_MODEL = "gpt-4o"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
NLI_MODEL = "roberta-large-mnli"
FUZZY_THRESH = 60
EMBEDDING_THRESH = 0.75
HALLUCINATION_THRESHOLD = 0.6

WEIGHTS = {
    "factcheck_verdict": 0.45,
    "embedding_score": 0.30,
    "fuzzy_score": 0.15,
    "nli_verdict": 0.10
}

FACTCHECK_SCORE = {"Yes": 1, "No": 0}
NLI_SCORE = {"entailment": 1, "neutral": 0.5, "contradiction": 0}
embedder = SentenceTransformer(EMBEDDING_MODEL)
tokenizer = AutoTokenizer.from_pretrained(NLI_MODEL)
nli_model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL)
client = OpenAI(api_key=OPENAI_API_KEY)

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        factcheck_cache = json.load(f)
else:
    factcheck_cache = {}

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

def fact_check_llm(ground_truth, response):
    key = f"{ground_truth} ||| {response}"
    if key in factcheck_cache:
        return factcheck_cache[key]

    prompt = (
        f"You are a fact-checker. Determine if the following answer is accurate based on the provided reference.\n\n"
        f"Reference (ground truth): {ground_truth}\n"
        f"Answer to evaluate: {response}\n\n"
        f"Reply with 'Yes' if the answer is factually correct and consistent with the reference. Otherwise, reply with 'No'."
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
        print(f"[Fact-check error] {e}")
        return "Error"

def normalize(val, min_val, max_val):
    return max(0, min(1, (val - min_val) / (max_val - min_val)))

def compute_final_score(row):
    factcheck = FACTCHECK_SCORE.get(str(row.get('factcheck_verdict', '')).strip(), 0)
    embedding = normalize(row.get('embedding_score', 0), 0.5, 0.85)
    fuzzy = normalize(row.get('fuzzy_score', 0), 0, 100)
    nli_raw = str(row.get('nli_label', row.get('nli_verdict', 'neutral'))).strip().lower()
    nli = NLI_SCORE.get(nli_raw, 0)

    return (
        WEIGHTS["factcheck_verdict"] * factcheck +
        WEIGHTS["embedding_score"] * embedding +
        WEIGHTS["fuzzy_score"] * fuzzy +
        WEIGHTS["nli_verdict"] * nli
    )

def evaluate_model(model_name, input_path, output_path, response_column):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    print(f"Evaluating: {model_name} ({len(df)} prompts)")

    fuzzy_scores, fuzzy_verdicts = [], []
    embed_scores, embed_verdicts = [], []
    nli_labels, nli_verdicts = [], []
    factcheck_verdicts = []
    final_scores, final_verdicts = [], []

    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Scoring {model_name}"):
        g = row["ground_truth"]
        r = row.get(response_column, "")

        fuzzy = fuzzy_match(g, r)
        fuzzy_v = "Yes" if fuzzy >= FUZZY_THRESH else "No"

        embed = embedding_similarity(g, r)
        embed_v = "Yes" if embed >= EMBEDDING_THRESH else "No"

        nli_result = nli_entailment(g, r)
        nli_v = "Yes" if nli_result == "entailment" else "No"

        factcheck = fact_check_llm(g, r)
        factcheck_v = "Yes" if "yes" in factcheck.lower() else "No"

        score = compute_final_score({
            "factcheck_verdict": factcheck_v,
            "embedding_score": embed,
            "fuzzy_score": fuzzy,
            "nli_label": nli_result,
            "nli_verdict": nli_v
        })
        verdict = "Not Hallucinated" if score >= HALLUCINATION_THRESHOLD else "Hallucinated"

        fuzzy_scores.append(fuzzy)
        fuzzy_verdicts.append(fuzzy_v)
        embed_scores.append(embed)
        embed_verdicts.append(embed_v)
        nli_labels.append(nli_result)
        nli_verdicts.append(nli_v)
        factcheck_verdicts.append(factcheck_v)
        final_scores.append(score)
        final_verdicts.append(verdict)

    df["fuzzy_score"] = fuzzy_scores
    df["fuzzy_verdict"] = fuzzy_verdicts
    df["embedding_score"] = embed_scores
    df["embedding_verdict"] = embed_verdicts
    df["nli_label"] = nli_labels
    df["nli_verdict"] = nli_verdicts
    df["factcheck_verdict"] = factcheck_verdicts
    df["final_score"] = final_scores
    df["hallucination_verdict"] = final_verdicts

    df.to_csv(output_path, index=False)
    print(f"Saved evaluation: {output_path}")

evaluate_model(
    model_name="Post-Filtered-GPT3.5",
    input_path="outputs/filtered_responses.csv",
    output_path="evaluations/filtered_responses_evaluated.csv",
    response_column="llm_response"
)