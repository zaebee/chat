"""
🐝⚡ ScoreTransformation (T Primitive) ⚡🐝

Pure transformation functions for AGRO scoring logic.
Stateless processing functions that transform analysis data into scores and severity levels.

Sacred Principle: "Transformation primitives are pure functions with no side effects"
"""

from typing import Dict, Any, List

from ..config.fibonacci_sequences import (
    FIBONACCI_89,
    FIBONACCI_55,
    FIBONACCI_34,
    FIBONACCI_21,
    FIBONACCI_13,
    FIBONACCI_8,
    FIBONACCI_5,
)
from .review_aggregate import AgroSeverity


class AgroScoringConstants:
    """Sacred constants for AGRO scoring calculations"""

    # Score boundaries
    MIN_SCORE = 0
    MAX_SCORE = 100

    # Severity thresholds (aligned with Fibonacci)
    DIVINE_THRESHOLD = FIBONACCI_89  # 89 (close to 90)
    BLESSED_THRESHOLD = FIBONACCI_55  # 55 (close to 80, needs adjustment)
    ACCEPTABLE_THRESHOLD = FIBONACCI_34  # 34 (close to 60, needs adjustment)
    CONCERNING_THRESHOLD = FIBONACCI_21  # 21 (close to 40, needs adjustment)

    # Violation penalties (aligned with Fibonacci)
    CRITICAL_VIOLATION_PENALTY = FIBONACCI_13  # 13 (close to 20)
    HIGH_VIOLATION_PENALTY = FIBONACCI_8  # 8 (close to 10)
    MEDIUM_VIOLATION_PENALTY = FIBONACCI_5  # 5


class ScoreTransformation:
    """
    🧬 T (Transformation) Primitive for AGRO Scoring

    Pure functions that transform analysis results into scores and severity levels.
    No state, no side effects - only sacred mathematical transformations.
    """

    @staticmethod
    def calculate_agro_score(pain_result: Dict[str, Any]) -> int:
        """
        Calculate AGRO (Aggressive Collaborative Evaluation) score

        Args:
            pain_result: Result from PAIN analysis containing score and violations

        Returns:
            int: AGRO score (0-100)
        """
        if not pain_result.get("analysis_successful", False):
            return 0

        pain_score = pain_result.get("pain_score", 0)
        violations = pain_result.get("violations", [])

        # Base score from PAIN analysis
        agro_score = pain_score

        # Apply violation penalties
        agro_score -= ScoreTransformation._calculate_violation_penalties(violations)

        # Ensure score stays within bounds
        return max(
            AgroScoringConstants.MIN_SCORE,
            min(AgroScoringConstants.MAX_SCORE, agro_score),
        )

    @staticmethod
    def _calculate_violation_penalties(violations: List[Dict[str, Any]]) -> int:
        """Calculate total penalty points from violations"""
        total_penalty = 0

        for violation in violations:
            severity = violation.get("severity", "medium")

            if severity == "critical":
                total_penalty += AgroScoringConstants.CRITICAL_VIOLATION_PENALTY
            elif severity == "high":
                total_penalty += AgroScoringConstants.HIGH_VIOLATION_PENALTY
            elif severity == "medium":
                total_penalty += AgroScoringConstants.MEDIUM_VIOLATION_PENALTY

        return total_penalty

    @staticmethod
    def determine_severity(agro_score: int) -> AgroSeverity:
        """
        Determine severity level based on AGRO score

        Args:
            agro_score: AGRO score (0-100)

        Returns:
            AgroSeverity: Corresponding severity level
        """
        if agro_score >= AgroScoringConstants.DIVINE_THRESHOLD:
            return AgroSeverity.DIVINE
        elif agro_score >= AgroScoringConstants.BLESSED_THRESHOLD:
            return AgroSeverity.BLESSED
        elif agro_score >= AgroScoringConstants.ACCEPTABLE_THRESHOLD:
            return AgroSeverity.ACCEPTABLE
        elif agro_score >= AgroScoringConstants.CONCERNING_THRESHOLD:
            return AgroSeverity.CONCERNING
        else:
            return AgroSeverity.CRITICAL

    @staticmethod
    def calculate_divine_blessing_eligibility(
        agro_score: int, violations: List[Dict[str, Any]]
    ) -> bool:
        """
        Determine if code is eligible for divine blessing

        Args:
            agro_score: AGRO score (0-100)
            violations: List of code violations

        Returns:
            bool: True if eligible for divine blessing
        """
        # Must have acceptable score or higher
        if agro_score < AgroScoringConstants.ACCEPTABLE_THRESHOLD:
            return False

        # No critical violations allowed for divine blessing
        critical_violations = [v for v in violations if v.get("severity") == "critical"]
        if critical_violations:
            return False

        return True

    @staticmethod
    def calculate_pain_score(
        violations: List[Dict[str, Any]], total_lines: int = FIBONACCI_89
    ) -> int:  # Aligned with Fibonacci
        """
        Calculate PAIN (Production Analysis and Issue Notification) score

        Args:
            violations: List of code violations
            total_lines: Total lines of code analyzed

        Returns:
            int: PAIN score (0-100, higher is better)
        """
        if total_lines == 0:
            return 0

        # Start with perfect score
        pain_score = 100

        # Deduct points based on violation density
        total_violations = len(violations)
        violation_density = (total_violations / total_lines) * 100

        # Apply density penalty (max 50 points)
        density_penalty = min(
            FIBONACCI_55, int(violation_density * FIBONACCI_8)
        )  # Aligned with Fibonacci
        pain_score -= density_penalty

        # Apply severity-based penalties
        severity_penalty = ScoreTransformation._calculate_violation_penalties(
            violations
        )
        pain_score -= severity_penalty

        return max(0, pain_score)

    @staticmethod
    def generate_score_insights(
        agro_score: int, pain_score: int, violations: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate sacred insights based on scoring analysis

        Args:
            agro_score: AGRO score
            pain_score: PAIN score
            violations: List of violations

        Returns:
            List[str]: Sacred insights about the code quality
        """
        insights = []

        # Score-based insights
        if agro_score >= AgroScoringConstants.DIVINE_THRESHOLD:
            insights.append("Code demonstrates divine excellence and sacred patterns")
        elif agro_score >= AgroScoringConstants.BLESSED_THRESHOLD:
            insights.append(
                "Code shows blessed quality with minor areas for improvement"
            )
        elif agro_score >= AgroScoringConstants.ACCEPTABLE_THRESHOLD:
            insights.append("Code meets acceptable standards with room for enhancement")
        else:
            insights.append(
                "Code requires significant improvement for production readiness"
            )

        # Violation-based insights
        critical_count = len([v for v in violations if v.get("severity") == "critical"])
        if critical_count > 0:
            insights.append(
                f"Critical violations detected: {critical_count} issues require immediate attention"
            )

        # Pain vs AGRO comparison
        score_diff = abs(agro_score - pain_score)
        if score_diff > 20:
            insights.append(
                "Significant difference between PAIN and AGRO scores indicates complex quality issues"
            )

        return insights
