# Phase 3 – Hallucination Mitigation

**Objective:**  
Reduce hallucination rates using advanced mitigation techniques tested on GPT-3.5 Turbo.

**Mitigation Strategies:**
- **Prompt Tuning:** Custom system prompts to enforce factual reasoning and refusal of speculation.  
- **Retrieval-Augmented Generation (RAG):** Factual grounding through context injection.  
- **Post-Generation Filtering:** Automated detection and rewriting of hallucinated responses.  
- **Combined Strategy:** Layered defense stack achieving **0% hallucination rate** across all 100 adversarial prompts.

**Outcome:**  
A mitigation pipeline integrating behavioral steering, retrieval grounding, and post-response validation.