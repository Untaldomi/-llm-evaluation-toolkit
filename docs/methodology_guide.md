# LLM Evaluation & RLHF Methodology Guide

This guide outlines core frameworks and evaluation principles used by AI Quality Analysts and Prompt Engineers to benchmark Large Language Models (LLMs) under Reinforcement Learning from Human Feedback (RLHF), Direct Preference Optimization (DPO), and Trust & Safety rubrics.

---

## 1. Core Evaluation Dimensions

When stack-ranking model outputs (Side-by-Side / SxS), evaluations are broken down into four foundational pillars:

### A. Instruction Following & Constraint Satisfaction
* **Positive Constraints:** Explicit structural requirements (e.g., *"write exactly two paragraphs"*, *"use a 3-stage dialogue tree"*, *"format as a single-sentence bullet list"*).
* **Negative Constraints:** Forbidden terms or topics (e.g., *"do not include soy milk"*, *"avoid robotic sound descriptors"*).
* **Critical Trap:** LLMs frequently suffer from *attention drift* when negative constraints appear late in a long prompt. Strict automated parsing and human audits are required to catch subtle leaks.

### B. Grounding & Factuality (Hallucination Prevention)
* **Definition:** Every factual assertion must be traceable to verified ground-truth data or provided context.
* **Failure Modes:**
  * **Entity Fabrication:** Inventing non-existent organizations (e.g., *"New York Daily Chronicle"*).
  * **URL Fabrication:** Generating plausible-looking but dead or fake hyperlinks.
  * **Contextual Misattribution:** Recommending a book about an 18th-century naval shipwreck (*The Wager*) as a card/poker strategy guide simply because the word "Wager" sounds like gambling.

### C. Naturalness & Integration vs. "Overnarrating"
* **Seamless Integration:** When personalizing responses based on user context (search history, preferences), the model should organically tailor its answers without explicitly stating how it acquired the information.
* **The Overnarrating Penalty:** Disclosing private internal context retrieval (e.g., *"Based on your email from yesterday where you bought tickets..."*) breaks conversational immersion and creates a robotic, intrusive user experience.

### D. Tone, Persona & Formality
* **Consistency:** Maintaining uniform address (*formal "usted"* vs. *informal "tú"*, professional vs. colloquial) without jarring shifts mid-response.
* **Adversarial Red-Teaming:** Testing whether a model maintains neutrality and adheres to ethical guidelines when probed with jailbreak attempts or provocative premises.

---

## 2. Writing Defensible Evaluation Rationales

A high-quality evaluation rationale must satisfy the **3-Point Rule**:
1. **Declare the Winner & Margin:** Explicitly state whether Model A or B won and by what margin (*Much Better*, *Better*, *Slightly Better*, *Tie*).
2. **Cite Specific Textual Evidence:** Quote exact phrases or reference specific turn numbers where the failure or success occurred.
3. **Contrast the Trade-offs:** Explain why the winning model's advantages outweigh any minor formatting flaws, or why a critical failure (like a negative constraint breach) instantly invalidates a response.
