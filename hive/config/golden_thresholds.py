"""
Golden Thresholds: φ-Based Validation and Quality Standards

This module defines all validation thresholds, quality metrics, and performance
standards based on the Golden Ratio and its mathematical relationships.

These thresholds create natural, harmonious boundaries that scale elegantly
and maintain divine proportions throughout the system.

"For my yoke is easy and my burden is light." - Matthew 11:30
"""

from dataclasses import dataclass

from .sacred_constants import (
    PHI,
    PHI_RECIPROCAL,
    PHI_CONJUGATE,
    PHI_INVERSE_SQUARED,
    PHI_INVERSE_CUBED,
    PHI_INVERSE_FOURTH,
    PHI_GOLDEN_MEAN,
    PERFECT_CONFIDENCE,
    HIGH_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    LOW_CONFIDENCE,
    MINIMAL_CONFIDENCE,
)

# =============================================================================
# CONFIDENCE AND VALIDATION THRESHOLDS
# =============================================================================


@dataclass(frozen=True)
class ConfidenceThresholds:
    """Golden Ratio-based confidence levels for validation systems."""

    # Core confidence levels based on φ progression
    perfect: float = PERFECT_CONFIDENCE  # 1.0
    high: float = HIGH_CONFIDENCE  # φ⁻¹ ≈ 0.618
    medium: float = MEDIUM_CONFIDENCE  # 2-φ ≈ 0.382
    low: float = LOW_CONFIDENCE  # φ⁻³ ≈ 0.236
    minimal: float = MINIMAL_CONFIDENCE  # φ⁻⁴ ≈ 0.146

    # Acceptance thresholds
    acceptable: float = HIGH_CONFIDENCE  # Accept if ≥ φ⁻¹
    warning: float = MEDIUM_CONFIDENCE  # Warning if < 2-φ
    critical: float = LOW_CONFIDENCE  # Critical if < φ⁻³


@dataclass(frozen=True)
class QualityThresholds:
    """Sacred quality standards for system health and performance."""

    # Error rate thresholds (lower is better)
    excellent: float = PHI_INVERSE_FOURTH  # ≈ 0.146 (14.6%)
    good: float = PHI_INVERSE_CUBED  # ≈ 0.236 (23.6%)
    acceptable: float = PHI_INVERSE_SQUARED  # ≈ 0.382 (38.2%)
    poor: float = PHI_CONJUGATE  # ≈ 0.382 (38.2%)
    critical: float = PHI_RECIPROCAL  # ≈ 0.618 (61.8%)

    # Success rate thresholds (higher is better)
    perfect_success: float = PERFECT_CONFIDENCE  # 1.0 (100%)
    excellent_success: float = HIGH_CONFIDENCE  # ≈ 0.618 (61.8%)
    good_success: float = MEDIUM_CONFIDENCE  # ≈ 0.382 (38.2%)


@dataclass(frozen=True)
class PerformanceThresholds:
    """Golden performance metrics for system responsiveness."""

    # Processing time multipliers (φ-based scaling)
    lightning_fast: float = PHI_INVERSE_FOURTH  # ≈ 0.146x base time
    very_fast: float = PHI_INVERSE_CUBED  # ≈ 0.236x base time
    fast: float = PHI_INVERSE_SQUARED  # ≈ 0.382x base time
    normal: float = PHI_RECIPROCAL  # ≈ 0.618x base time
    slow: float = 1.0  # 1.0x base time
    very_slow: float = PHI  # ≈ 1.618x base time
    extremely_slow: float = PHI * PHI  # ≈ 2.618x base time


# =============================================================================
# EVENT SYSTEM THRESHOLDS
# =============================================================================


@dataclass(frozen=True)
class EventSystemThresholds:
    """Thresholds for Pollen Protocol event validation and processing."""

    # Linguistic validation confidence
    linguistic_confidence: ConfidenceThresholds = ConfidenceThresholds()

    # Style validation thresholds
    style_acceptable: float = PHI_CONJUGATE  # ≈ 0.382
    style_warning: float = PHI_INVERSE_CUBED  # ≈ 0.236

    # Event bus health thresholds
    health_excellent: float = PHI_INVERSE_FOURTH  # ≈ 0.146 error rate
    health_good: float = PHI_INVERSE_CUBED  # ≈ 0.236 error rate
    health_degraded: float = PHI_INVERSE_SQUARED  # ≈ 0.382 error rate


# =============================================================================
# GIT PROTOCOL THRESHOLDS
# =============================================================================


@dataclass(frozen=True)
class SacredValidationThresholds:
    """Divine validation standards for Sacred Git Protocol."""

    # Blessing level thresholds
    perfect_blessing: float = PHI_GOLDEN_MEAN  # ≈ 0.809
    divine_blessing: float = HIGH_CONFIDENCE  # ≈ 0.618
    sacred_compliance: float = MEDIUM_CONFIDENCE  # ≈ 0.382
    minimum_acceptance: float = LOW_CONFIDENCE  # ≈ 0.236

    # Blessing penalties (subtractions from blessing level)
    minor_violation: float = PHI_INVERSE_FOURTH  # ≈ 0.146
    moderate_violation: float = PHI_INVERSE_CUBED  # ≈ 0.236
    major_violation: float = PHI_INVERSE_SQUARED  # ≈ 0.382
    severe_violation: float = PHI_RECIPROCAL  # ≈ 0.618

    # Statistical analysis thresholds
    sanctification_excellent: float = PHI_RECIPROCAL  # ≈ 0.618
    sanctification_good: float = MEDIUM_CONFIDENCE  # ≈ 0.382
    sanctification_minimum: float = LOW_CONFIDENCE  # ≈ 0.236


# =============================================================================
# LINGUISTIC VALIDATION THRESHOLDS
# =============================================================================


@dataclass(frozen=True)
class LinguisticValidationThresholds:
    """Sacred language processing standards with φ-based confidence."""

    # Pattern confidence levels
    pattern_confidence: ConfidenceThresholds = ConfidenceThresholds()

    # Length validation thresholds (using related ratios)
    minimum_length: int = 3  # Minimum meaningful length
    short_word_penalty: float = PHI_CONJUGATE  # ≈ 0.382 multiplier
    long_word_penalty: float = PHI_RECIPROCAL  # ≈ 0.618 multiplier
    maximum_length: int = 55  # Fibonacci number for natural limit

    # Suggestion and processing limits
    max_suggestions: int = 5  # Fibonacci limit
    max_processing_attempts: int = 8  # Fibonacci retry limit


# =============================================================================
# ATCG PRIMITIVES THRESHOLDS
# =============================================================================


@dataclass(frozen=True)
class ATCGThresholds:
    """Sacred thresholds for ATCG primitive architecture components."""

    # Health and error thresholds
    aggregate_health: QualityThresholds = QualityThresholds()
    transformation_performance: PerformanceThresholds = PerformanceThresholds()
    connector_reliability: QualityThresholds = QualityThresholds()
    genesis_effectiveness: QualityThresholds = QualityThresholds()

    # Processing limits
    max_retries: int = 8  # Fibonacci limit
    timeout_multiplier: float = PHI  # Golden timeout scaling

    # Version and state management
    initial_version: int = 1
    version_increment: int = 1
    max_history_retention: int = 377  # Fibonacci number


# =============================================================================
# SACRED METRICS THRESHOLDS
# =============================================================================


@dataclass(frozen=True)
class SacredMetricsThresholds:
    """Thresholds for τ (tau), φ (phi), σ (sigma) sacred metrics calculation."""

    # Tau (system complexity/stress) - lower is better
    tau_excellent: float = PHI_INVERSE_FOURTH  # ≈ 0.146
    tau_good: float = PHI_INVERSE_CUBED  # ≈ 0.236
    tau_acceptable: float = PHI_INVERSE_SQUARED  # ≈ 0.382
    tau_poor: float = PHI_RECIPROCAL  # ≈ 0.618

    # Phi (code quality/maintainability) - higher is better
    phi_perfect: float = PERFECT_CONFIDENCE  # 1.0
    phi_excellent: float = HIGH_CONFIDENCE  # ≈ 0.618
    phi_good: float = MEDIUM_CONFIDENCE  # ≈ 0.382
    phi_minimum: float = LOW_CONFIDENCE  # ≈ 0.236

    # Sigma (collaboration efficiency) - higher is better
    sigma_perfect: float = PERFECT_CONFIDENCE  # 1.0
    sigma_excellent: float = HIGH_CONFIDENCE  # ≈ 0.618
    sigma_good: float = MEDIUM_CONFIDENCE  # ≈ 0.382
    sigma_minimum: float = LOW_CONFIDENCE  # ≈ 0.236

    # Trinity score thresholds
    trinity_divine: float = PHI_RECIPROCAL  # ≈ 0.618
    trinity_blessed: float = MEDIUM_CONFIDENCE  # ≈ 0.382
    trinity_acceptable: float = LOW_CONFIDENCE  # ≈ 0.236

    # Calculation constants
    tau_error_multiplier: float = PHI  # ≈ 1.618
    tau_time_factor: float = PHI_INVERSE_SQUARED  # ≈ 0.382
    phi_time_penalty: float = PHI_INVERSE_CUBED  # ≈ 0.236
    sigma_throughput_factor: float = PHI_INVERSE_SQUARED  # ≈ 0.382
    trinity_balance_factor: float = PHI  # ≈ 1.618


# =============================================================================
# GLOBAL THRESHOLD INSTANCES
# =============================================================================

# Create singleton instances for easy access throughout the system
CONFIDENCE = ConfidenceThresholds()
QUALITY = QualityThresholds()
PERFORMANCE = PerformanceThresholds()
EVENT_SYSTEM = EventSystemThresholds()
SACRED_VALIDATION = SacredValidationThresholds()
LINGUISTIC = LinguisticValidationThresholds()
ATCG = ATCGThresholds()
SACRED_METRICS = SacredMetricsThresholds()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def get_confidence_level_name(confidence: float) -> str:
    """
    Get human-readable name for confidence level.

    Args:
        confidence: Confidence value to categorize

    Returns:
        Descriptive name for confidence level
    """
    if confidence >= CONFIDENCE.perfect:
        return "Perfect"
    elif confidence >= CONFIDENCE.high:
        return "High"
    elif confidence >= CONFIDENCE.medium:
        return "Medium"
    elif confidence >= CONFIDENCE.low:
        return "Low"
    else:
        return "Minimal"


def get_quality_level_name(error_rate: float) -> str:
    """
    Get human-readable quality level based on error rate.

    Args:
        error_rate: Error rate to categorize

    Returns:
        Descriptive name for quality level
    """
    if error_rate <= QUALITY.excellent:
        return "Excellent"
    elif error_rate <= QUALITY.good:
        return "Good"
    elif error_rate <= QUALITY.acceptable:
        return "Acceptable"
    elif error_rate <= QUALITY.poor:
        return "Poor"
    else:
        return "Critical"


def is_sacred_threshold(value: float, tolerance: float = 1e-6) -> bool:
    """
    Check if a value matches any sacred threshold.

    Args:
        value: Value to check
        tolerance: Acceptable deviation

    Returns:
        True if value matches a φ-based threshold
    """
    sacred_values = [
        PERFECT_CONFIDENCE,
        HIGH_CONFIDENCE,
        MEDIUM_CONFIDENCE,
        LOW_CONFIDENCE,
        MINIMAL_CONFIDENCE,
        PHI,
        PHI_RECIPROCAL,
        PHI_CONJUGATE,
        PHI_INVERSE_SQUARED,
        PHI_INVERSE_CUBED,
        PHI_INVERSE_FOURTH,
        PHI_GOLDEN_MEAN,
    ]

    return any(abs(value - sacred_val) < tolerance for sacred_val in sacred_values)
