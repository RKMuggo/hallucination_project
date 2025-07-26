import os

RAG_DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "inputs", "rag_docs"))

def load_rag_context(trigger_type):
    doc_path = os.path.join(RAG_DOCS_DIR, f"{trigger_type}.txt")
    
    if not os.path.exists(doc_path):
        print(f"Warning: No RAG document found for trigger type: {trigger_type}")
        return ""
    
    with open(doc_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def construct_rag_prompt(question, context):
    return f"{context}\n\nQuestion: {question}"
