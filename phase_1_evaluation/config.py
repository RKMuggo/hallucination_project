# config.py

DATA_DIR = "data"
RESPONSES_DIR = "responses"
OUTPUTS_DIR = "outputs"
DOMAINS = ["general", "medical", "legal", "finance"]

OPENAI_MODEL = "gpt-4o"
OPENAI_TEMPERATURE = {
    "low": 0.3,     # Evaluation
    "medium": 0.7,  # Balanced
    "high": 1.2     # Stress testing
}
OPENAI_API_KEY = " "

THRESHOLDS = {
    "fuzzy": 70,       
    "embedding": 0.75,       
    "nli": "entailment",      
    "factcheck": True         
}

DOMAIN_THRESHOLDS = {
    "general": {"fuzzy": 16, "embedding": 0.62},
    "medical": {"fuzzy": 16, "embedding": 0.62},
    "legal": {"fuzzy": 14, "embedding": 0.67},
    "finance": {"fuzzy": 14, "embedding": 0.64}
}

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
NLI_MODEL = "microsoft/deberta-large-mnli"
FACTCHECK_MODEL = "gpt-4o"