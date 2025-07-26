# Phase 2 – Synthetic Dataset Creation and LLM Benchmarking

**Objective:**  
Evaluate hallucination tendencies of leading LLMs using a custom adversarial dataset created to test hallucinations in LLMs.

**Key Components:**
- **Synthetic Dataset:**  
  - 100 manually crafted prompts targeting four hallucination triggers:  
    **Contradictions, Entity Swaps, Fictional Locations, Impossible Timelines.**
  - Stored in structured `.jsonl` format with ground truth references.
- **Benchmarking:**  
  - Models: GPT-4o, GPT-3.5 Turbo, Claude-3 Sonnet, Mistral (Small & Large).
  - Unified evaluation pipeline from Phase 1 for fair comparison.
- **Results:**  
  - **Claude-3 Sonnet:** Lowest hallucination rate at 10%.  
  - **GPT-4o:** 20% hallucination, halving GPT-3.5's 41%.  
  - **Mistral models:** 44% hallucination, highlighting alignment gaps.

**Outcome:**  
A robust benchmarking framework with a hallucination leaderboard and detailed analysis of model vulnerabilities by trigger type.