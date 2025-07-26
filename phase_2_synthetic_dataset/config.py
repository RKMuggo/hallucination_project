# config.py

MODELS = {
    "gpt-4o": "gpt-4o",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "claude-3-sonnet": "claude-3-sonnet",
    "mistral-large-latest": "mistral-large-latest",
    "mistral-small": "mistral-small"
}

TRIGGER_TYPES = {
    "fictional_location": "Ask about places that don't exist.",
    "contradiction": "Introduce logical or factual contradictions.",
    "impossible_timeline": "Ask about events with wrong dates or fake chronology.",
    "entity_swap": "Swap real entities with made-up or incorrect ones."
}

PROMPTS_PER_TYPE = 25

SYNTHETIC_DATASET_DIR = "synthetic_dataset"

RESPONSES_DIR = "responses"

EVALUATIONS_DIR = "evaluations"

LEADERBOARD_DIR = "leaderboard"