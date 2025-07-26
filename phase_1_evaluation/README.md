# Phase 1 – Multi-Layer Hallucination Detection System

**Objective:**  
Design and implement a modular detection pipeline to identify hallucinations in LLM responses using the TruthfulQA dataset.

**Key Components:**
- **Detection Layers:**  
  - Fuzzy string matching for lexical similarity.  
  - Embedding-based semantic similarity with SentenceTransformers.  
  - Natural Language Inference (NLI) for logical alignment.  
  - LLM-based fact-checking with GPT-4o.
- **Weighted Scoring:**  
  A 4-layer weighted aggregation method to compute final hallucination verdicts, with thresholds calibrated per domain.

**Outcome:**  
A reusable, domain-adaptive detection pipeline capable of evaluating LLM outputs across various datasets and models.
