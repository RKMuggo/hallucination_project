# A Multi-Phase Framework for Detecting, Benchmarking, and Mitigating Hallucinations in Large Language Models

**Author:** Raaed Kamran Muggo  
**Date:** July 26, 2025  

---

## Overview

This repository presents a comprehensive three-phase framework addressing hallucinations—factually incorrect or fabricated content—in large language models (LLMs). The work combines detection, benchmarking, and mitigation techniques to build reliable, hallucination-aware AI systems suitable for high-stakes domains such as healthcare, finance, and law.

---

## Project Summary

- **Phase 1 – Detection:**  
  Developed a modular, multi-layer detection pipeline integrating fuzzy string matching, semantic embeddings, natural language inference (NLI), and LLM-based fact-checking. Applied to the TruthfulQA dataset to establish thresholds and scoring logic.

- **Phase 2 – Benchmarking:**  
  Created a synthetic dataset of 100 adversarial prompts designed to trigger hallucinations (entity swaps, fictional locations, contradictions, and impossible timelines). Benchmarked leading LLMs—GPT-4o, GPT-3.5 Turbo, Claude-3 Sonnet, and Mistral—highlighting vulnerabilities and producing a hallucination leaderboard.

- **Phase 3 – Mitigation:**  
  Implemented and evaluated mitigation strategies including Prompt Tuning, Retrieval-Augmented Generation (RAG), and Post-Generation Filtering.


---

## Full Report

For detailed methodology, results, visualizations, and references, see the full report:  
[**Hallucination_in_LLMs.pdf**](Hallucination_in_LLMs.pdf)

---

## References

- [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958)  
- [Survey of Hallucination in Natural Language Generation](http://dx.doi.org/10.1145/3571730)  
- [Q2: Evaluating Factual Consistency in Knowledge-Grounded Dialogues](https://arxiv.org/abs/2104.08202)  
- [LegalBench: A Benchmark for Measuring Legal Reasoning](https://arxiv.org/abs/2308.11462)