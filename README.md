# 🛡️ LLM Evaluation & AI Safety Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Domain: AI Quality & RLHF](https://img.shields.io/badge/Domain-RLHF%20%26%20AI%20Evaluation-orange.svg)]()
[![Author: Rafael Tifá](https://img.shields.io/badge/Author-Rafael%20Tifá-purple.svg)](https://github.com/Untaldomi)

A modular Python framework and benchmark suite designed for **AI Quality Analysts**, **Prompt Engineers**, and **RLHF Evaluators**. It provides automated tools to audit Large Language Model (LLM) responses against negative constraints, detect factual hallucinations, perform Side-by-Side (SxS) stack-rankings, and penalize robotic overnarrating.

---

## 📌 Motivation & Objectives

State-of-the-art frontier models (such as Google Gemini, OpenAI GPT-4, and Claude) frequently struggle with subtle failure modes:
1. **Constraint Neglect:** Recommending forbidden ingredients or violating explicit formatting boundaries (e.g., single-sentence constraints).
2. **Semantic Hallucinations:** Confusing lexical similarity with factual relevance (e.g., misclassifying 18th-century naval history as poker literature).
3. **Overnarrating in Personalization:** Awkwardly announcing internal data sources rather than delivering natural, seamless assistance.

This toolkit provides reproducible auditing tools and case-study benchmarks to systematically evaluate and document these behaviors.

---

## 🚀 Key Modules

### 1. `ConstraintChecker` (`evaluator/constraint_checker.py`)
* **Negative Constraint Enforcement:** Regex-based boundary matching to catch forbidden terms (allergens, prohibited keywords, cliches).
* **Structural Validation:** Automated verification of sentence counts, paragraph thresholds, and single-sentence list rules.
* **Greeting & Formality Verification:** Linguistic checks for appropriate conversational openings.

### 2. `SideBySideEvaluator` (`evaluator/sxs_comparison.py`)
* **Multi-Dimensional Scoring:** Evaluates Grounding (35%), Instruction Following (35%), Naturalness (20%), and Conciseness (10%).
* **Overnarrating Penalty Engine:** Deducts points when personal data is integrated robotically.
* **Automated Rationale Generation:** Produces defensible, structured 3-4 sentence audit justifications.

### 3. `HallucinationAuditor` (`evaluator/hallucination_auditor.py`)
* **Knowledge Base Claim Cross-Referencing:** Verifies entities and thematic claims against verified bibliographic and historical ground-truth.
* **Fabricated URL Detection:** Flags hallucinated hyperlinks and malformed domains.

---

## 📊 Benchmark Case Studies

The repository includes real-world evaluation benchmarks (`examples/sample_evaluations.json`):

| ID | Evaluation Domain | Challenge / Constraint | Result / Finding |
| :--- | :--- | :--- | :--- |
| **BENCH-001** | Negative Constraints | Prompt: "I hate soy milk & can't have sugar" | ❌ **FAIL** - Model recommended soy milk & sugar syrup |
| **BENCH-002** | Factuality & Relevance | Biography of Doyle Brunson vs. *The Wager* | ❌ **HALLUCINATION** - Naval shipwreck tragedy misclassified as poker |
| **BENCH-003** | Historical Grounding | First issue date & original title of NYT | ❌ **FLAGGED** - Fabricated "NY Daily Chronicle" & fake URL |
| **BENCH-004** | AI Personalization | Gemini Personalization vs. Overnarrating | ✅ **MODEL A WIN** - Seamless integration without robotic overnarrating |

---

## 💻 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Untaldomi/llm-evaluation-toolkit.git
cd llm-evaluation-toolkit
```

### 2. Run the interactive evaluation suite
No heavy dependencies required (runs directly with Python standard library):

```bash
python examples/run_eval_demo.py
```

### Sample Output:
```text
======================================================================
  DEMO 1: NEGATIVE CONSTRAINT & INSTRUCTION CHECKER
======================================================================
Prompt: How do I make a London Fog? ... I hate soy milk, and I can't have sugar.

  [PASS] Formal Polite Greeting: Formal greeting detected in opening lines.
  [FAIL] Negative Constraint: 'soy milk': Violation detected: Found forbidden term 'soy milk'.
  [PASS] Negative Constraint: 'sugar': Successfully avoided forbidden term 'sugar'.
  [FAIL] Negative Constraint: 'simple syrup': Violation detected: Found forbidden term 'simple syrup'.
  [PASS] Bullet Point Sentence Constraint: All list items strictly adhere to the single-sentence rule.

Result: 3/5 passed (60.0% compliance).
```

---

## 📖 Documentation
Detailed evaluation rubrics and methodologies are documented in [docs/methodology_guide.md](docs/methodology_guide.md).

---

## 👤 Author
**Tirson Rafael Tifá**
* 📍 New York, NY
* 💼 Bilingual AI Quality Analyst & IT Systems Specialist
* 🌐 GitHub: [@Untaldomi](https://github.com/Untaldomi)
* 🔗 LinkedIn: [linkedin.com/in/rafael-tifa](https://linkedin.com/in/rafael-tifa/)

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
