"""
LLM Evaluation Toolkit
A lightweight, rigorous Python library for evaluating, benchmarking, and auditing
Large Language Model (LLM) responses under RLHF, safety, and constraint-satisfaction rubrics.
"""

from .constraint_checker import ConstraintChecker, ConstraintResult
from .sxs_comparison import SideBySideEvaluator, EvaluationReport
from .hallucination_auditor import HallucinationAuditor, FactCheckResult

__all__ = [
    "ConstraintChecker",
    "ConstraintResult",
    "SideBySideEvaluator",
    "EvaluationReport",
    "HallucinationAuditor",
    "FactCheckResult",
]
