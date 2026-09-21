"""
Constraint Checker Module
Automated validation of instruction-following, negative constraints,
sentence counts, and structural formatting for LLM responses.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ConstraintResult:
    constraint_name: str
    passed: bool
    details: str
    severity: str = "ERROR"  # "ERROR" or "WARNING"


class ConstraintChecker:
    """
    Evaluates LLM output against explicit prompt constraints.
    Supports negative constraints (forbidden terms), structural constraints
    (sentence counts, paragraph counts), and formatting rules.
    """

    def __init__(self, text: str):
        self.raw_text = text.strip()
        self.results: List[ConstraintResult] = []

    def check_negative_constraints(self, forbidden_terms: List[str]) -> bool:
        """
        Ensures none of the forbidden phrases or ingredients appear in the output.
        Example: ['soy milk', 'sugar', 'simple syrup']
        """
        all_passed = True
        for term in forbidden_terms:
            pattern = rf"\b{re.escape(term)}\b"
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                self.results.append(
                    ConstraintResult(
                        constraint_name=f"Negative Constraint: '{term}'",
                        passed=False,
                        details=f"Violation detected: Found forbidden term '{term}' in response.",
                        severity="ERROR",
                    )
                )
                all_passed = False
            else:
                self.results.append(
                    ConstraintResult(
                        constraint_name=f"Negative Constraint: '{term}'",
                        passed=True,
                        details=f"Successfully avoided forbidden term '{term}'.",
                    )
                )
        return all_passed

    def check_sentence_count(self, min_sentences: int, max_sentences: Optional[int] = None) -> bool:
        """
        Validates total sentence count across the text.
        """
        sentences = [s.strip() for s in re.split(r"[.!?]+", self.raw_text) if len(s.strip()) > 3]
        count = len(sentences)

        if count < min_sentences:
            self.results.append(
                ConstraintResult(
                    constraint_name="Sentence Count Bounds",
                    passed=False,
                    details=f"Failed: Found {count} sentences, minimum required was {min_sentences}.",
                    severity="ERROR",
                )
            )
            return False

        if max_sentences and count > max_sentences:
            self.results.append(
                ConstraintResult(
                    constraint_name="Sentence Count Bounds",
                    passed=False,
                    details=f"Failed: Found {count} sentences, maximum allowed was {max_sentences}.",
                    severity="ERROR",
                )
            )
            return False

        self.results.append(
            ConstraintResult(
                constraint_name="Sentence Count Bounds",
                passed=True,
                details=f"Passed: Response contains {count} sentences (Target: {min_sentences}-{max_sentences or 'inf'}).",
            )
        )
        return True

    def check_paragraph_count(self, min_paragraphs: int) -> bool:
        """
        Validates the number of distinct paragraphs (separated by blank lines).
        """
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", self.raw_text) if p.strip()]
        count = len(paragraphs)

        if count < min_paragraphs:
            self.results.append(
                ConstraintResult(
                    constraint_name="Paragraph Structure",
                    passed=False,
                    details=f"Failed: Found {count} paragraphs, minimum required was {min_paragraphs}.",
                    severity="ERROR",
                )
            )
            return False

        self.results.append(
            ConstraintResult(
                constraint_name="Paragraph Structure",
                passed=True,
                details=f"Passed: Found {count} distinct paragraphs (Required: >= {min_paragraphs}).",
            )
        )
        return True

    def check_bullet_single_sentences(self) -> bool:
        """
        Checks that every bullet point or numbered item contains exactly ONE sentence.
        """
        lines = self.raw_text.split("\n")
        bullet_pattern = re.compile(r"^\s*(?:[-*•]|\d+[\.)])\s*(.+)$")
        all_passed = True

        for idx, line in enumerate(lines, 1):
            match = bullet_pattern.match(line)
            if match:
                content = match.group(1).strip()
                sentences = [s.strip() for s in re.split(r"[.!?]+", content) if len(s.strip()) > 2]
                if len(sentences) > 1:
                    self.results.append(
                        ConstraintResult(
                            constraint_name=f"Single-Sentence Item (Line {idx})",
                            passed=False,
                            details=f"Line {idx} has {len(sentences)} sentences ('{content[:40]}...'). Required: exactly 1.",
                            severity="ERROR",
                        )
                    )
                    all_passed = False

        if all_passed:
            self.results.append(
                ConstraintResult(
                    constraint_name="Bullet Point Sentence Constraint",
                    passed=True,
                    details="All list items strictly adhere to the single-sentence rule.",
                )
            )
        return all_passed

    def check_greeting_formality(self) -> bool:
        """
        Evaluates whether an opening greeting is present and formally polite.
        """
        formal_openings = ["greetings", "dear", "good morning", "good afternoon", "it is a pleasure", "to whom it may concern"]
        first_chunk = self.raw_text[:120].lower()

        found = any(phrase in first_chunk for phrase in formal_openings)
        self.results.append(
            ConstraintResult(
                constraint_name="Formal Polite Greeting",
                passed=found,
                details="Formal greeting detected in opening lines." if found else "No formal greeting detected in opening.",
                severity="WARNING" if not found else "INFO",
            )
        )
        return found

    def summary(self) -> Dict[str, Any]:
        """
        Returns a structured summary of all constraint checks.
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        return {
            "total_constraints_checked": total,
            "passed": passed,
            "failed": failed,
            "success_rate_percent": round((passed / total * 100), 1) if total > 0 else 100,
            "violations": [r for r in self.results if not r.passed],
        }
