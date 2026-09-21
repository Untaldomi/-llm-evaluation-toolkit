"""
Side-by-Side (SxS) Evaluator Module
Engine for stack-ranking two model outputs, evaluating personalization quality,
scoring key dimensions, and generating defensible evaluation rationales.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class EvaluationReport:
    prompt: str
    model_a_name: str
    model_b_name: str
    winner: str  # "Model A", "Model B", or "Tie"
    margin: str  # "Much Better", "Better", "Slightly Better", "Negligible"
    scores_a: Dict[str, float]
    scores_b: Dict[str, float]
    rationale: str


class SideBySideEvaluator:
    """
    Simulates production RLHF and AI Quality Analysis evaluation.
    Compares two model responses across core quality dimensions:
    - Grounding (Factuality & evidence alignment)
    - Instruction Following (Constraint adherence)
    - Naturalness & Integration (Absence of awkward overnarrating)
    - Conciseness & Tone
    """

    def __init__(self, prompt: str, response_a: str, response_b: str):
        self.prompt = prompt
        self.response_a = response_a
        self.response_b = response_b

    def score_response(
        self,
        grounding: float,
        instruction_following: float,
        naturalness: float,
        conciseness: float,
        overnarrating_penalty: float = 0.0,
    ) -> Dict[str, float]:
        """
        Calculates composite quality score across 4 dimensions with penalties.
        Range for each dimension: 1.0 to 5.0.
        """
        raw_score = (grounding * 0.35) + (instruction_following * 0.35) + (naturalness * 0.20) + (conciseness * 0.10)
        final_score = max(1.0, raw_score - overnarrating_penalty)
        return {
            "grounding": grounding,
            "instruction_following": instruction_following,
            "naturalness": naturalness,
            "conciseness": conciseness,
            "overnarrating_penalty": overnarrating_penalty,
            "composite_score": round(final_score, 2),
        }

    def generate_report(
        self,
        scores_a: Dict[str, float],
        scores_b: Dict[str, float],
        custom_rationale: Optional[str] = None,
    ) -> EvaluationReport:
        """
        Generates an audit report determining the winner and compiling the rationale.
        """
        diff = scores_a["composite_score"] - scores_b["composite_score"]

        if abs(diff) < 0.2:
            winner = "Tie"
            margin = "About the same"
        elif diff > 0:
            winner = "Model A"
            margin = "Much Better" if diff >= 1.0 else ("Better" if diff >= 0.5 else "Slightly Better")
        else:
            winner = "Model B"
            margin = "Much Better" if diff <= -1.0 else ("Better" if diff <= -0.5 else "Slightly Better")

        # Auto-generate rationale if none provided
        if not custom_rationale:
            custom_rationale = self._synthesize_rationale(winner, margin, scores_a, scores_b)

        return EvaluationReport(
            prompt=self.prompt,
            model_a_name="Model A",
            model_b_name="Model B",
            winner=winner,
            margin=margin,
            scores_a=scores_a,
            scores_b=scores_b,
            rationale=custom_rationale,
        )

    def _synthesize_rationale(
        self, winner: str, margin: str, a: Dict[str, float], b: Dict[str, float]
    ) -> str:
        """
        Synthesizes a structured 3-4 sentence professional evaluation rationale.
        """
        if winner == "Tie":
            return (
                "Both models deliver comparable performance. Neither model exhibited major factual hallucinations "
                "or constraint violations, and both appropriately addressed the user's core intent with similar tone and structure."
            )

        w_scores = a if winner == "Model A" else b
        l_scores = b if winner == "Model A" else a
        loser = "Model B" if winner == "Model A" else "Model A"

        points = []
        if w_scores["instruction_following"] > l_scores["instruction_following"]:
            points.append(f"{winner} adhered strictly to all negative and structural prompt constraints, whereas {loser} overlooked key instructions")
        if w_scores["grounding"] > l_scores["grounding"]:
            points.append(f"{winner} remained fully grounded in verifiable evidence without generating unsubstantiated claims")
        if l_scores["overnarrating_penalty"] > 0:
            points.append(f"{loser} suffered from severe overnarrating by awkwardly disclosing its internal context retrieval")
        elif w_scores["naturalness"] > l_scores["naturalness"]:
            points.append(f"{winner} integrated contextual information much more conversationally and naturally")

        details_str = "; ".join(points) if points else "it delivered higher overall relevance and clarity"
        return (
            f"{winner} is {margin.lower()} than {loser}. "
            f"Specifically, {details_str}. "
            f"Consequently, {winner} provides a superior, safer, and more helpful user experience."
        )
