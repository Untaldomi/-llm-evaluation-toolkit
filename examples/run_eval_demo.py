#!/usr/bin/env python3
"""
LLM Evaluation Toolkit - Live Demo Runner
Demonstrates constraint checking, hallucination auditing, and side-by-side (SxS)
model comparison in an interactive terminal environment.
"""

import sys
import os
import json

# Ensure evaluator module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from evaluator.constraint_checker import ConstraintChecker
from evaluator.sxs_comparison import SideBySideEvaluator
from evaluator.hallucination_auditor import HallucinationAuditor


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title.upper()}")
    print("=" * 70)


def run_constraint_demo():
    print_header("Demo 1: Negative Constraint & Instruction Checker")

    sample_prompt = (
        "How do I make a London Fog? Instructions as single-sentence bullets. "
        "Greet formally. Provide 2 variations. I hate soy milk, and I can't have sugar."
    )

    bad_model_response = (
        "Greetings,\n"
        "It is a pleasure to assist you with this request.\n"
        "1. Steep one Earl Grey tea bag in half a cup of hot water.\n"
        "2. Froth half a cup of milk of your choice.\n"
        "3. Add one teaspoon of vanilla extract.\n"
        "Flavor Variation: Add lavender simple syrup to sweeten the beverage.\n"
        "Vegan Alternative: Substitute dairy milk with oat milk or soy milk.\n"
        "Ingredients: Earl Grey tea bag, water, milk (or oat, almond, or soy milk), (lavender simple syrup)"
    )

    print(f"Prompt: {sample_prompt}\n")
    print("Evaluating Model Response against prompt constraints...\n")

    checker = ConstraintChecker(bad_model_response)
    checker.check_greeting_formality()
    checker.check_negative_constraints(["soy milk", "sugar", "simple syrup"])
    checker.check_bullet_single_sentences()

    for res in checker.results:
        status = "[PASS]" if res.passed else "[FAIL]"
        print(f"  {status} {res.constraint_name}: {res.details}")

    summary = checker.summary()
    print(f"\nResult: {summary['passed']}/{summary['total_constraints_checked']} passed ({summary['success_rate_percent']}% compliance).")


def run_sxs_demo():
    print_header("Demo 2: Side-by-Side (SxS) Model Ranking & Rationale")

    user_query = "What workout should I do tomorrow morning?"

    # Model A: Natural integration
    resp_a = (
        "Here is a steady 45-minute outdoor tempo run to build endurance, followed by "
        "a 10-minute dynamic stretching routine for your legs."
    )

    # Model B: Robotic overnarrating
    resp_b = (
        "Based on your Gmail confirmations for the marathon and your YouTube watch history "
        "regarding running cadence, I have calculated you need to run 8 miles."
    )

    evaluator = SideBySideEvaluator(user_query, resp_a, resp_b)

    # Score Model A (Seamless, natural, grounded)
    scores_a = evaluator.score_response(
        grounding=4.8,
        instruction_following=4.9,
        naturalness=4.9,
        conciseness=4.5,
        overnarrating_penalty=0.0,
    )

    # Score Model B (Overnarrated, robotic)
    scores_b = evaluator.score_response(
        grounding=4.2,
        instruction_following=4.0,
        naturalness=2.1,
        conciseness=3.5,
        overnarrating_penalty=1.5,
    )

    report = evaluator.generate_report(scores_a, scores_b)

    print(f"Winner: {report.winner} ({report.margin})")
    print(f"  Model A Composite Score: {scores_a['composite_score']} / 5.0")
    print(f"  Model B Composite Score: {scores_b['composite_score']} / 5.0")
    print(f"\nGenerated Audit Rationale:\n\"{report.rationale}\"")


def run_hallucination_demo():
    print_header("Demo 3: Factuality & Hallucination Auditor")

    auditor = HallucinationAuditor()
    print("Testing claim: 'The Wager is a great book recommendation for poker fans'...")

    result = auditor.verify_claim("the_wager", "poker and gambling strategy")
    print(f"  Verified: {result.verified}")
    print(f"  Is Hallucination: {result.is_hallucination}")
    print(f"  Citation: {result.source_citation}")
    print(f"  Auditor Findings: {result.explanation}")


if __name__ == "__main__":
    print("\nStarting LLM Evaluation Toolkit Benchmark Suite...")
    run_constraint_demo()
    run_sxs_demo()
    run_hallucination_demo()
    print("\n" + "=" * 70)
    print("  ALL BENCHMARKS COMPLETED SUCCESSFULLY")
    print("=" * 70 + "\n")
