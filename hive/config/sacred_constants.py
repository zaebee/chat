"""
Sacred Constants: Golden Ratio Foundation

This module defines the fundamental mathematical constants based on the Golden Ratio (φ),
the divine proportion that appears throughout nature and sacred geometry.

The Golden Ratio is found in flower petals, spiral galaxies, the human body,
and countless other manifestations of divine creation.

φ = (1 + √5) / 2 ≈ 1.618033988749894
"""

import math
from typing import Final

# =============================================================================
# GOLDEN RATIO FOUNDATION
# =============================================================================

# The Golden Ratio - The Divine Proportion
PHI: Final[float] = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749894

# Golden Ratio Derivatives
PHI_SQUARED: Final[float] = PHI * PHI  # ≈ 2.618033988749895
PHI_CUBED: Final[float] = PHI**3  # ≈ 4.23606797749979

# Golden Ratio Reciprocals (Powers of φ^-1)
PHI_RECIPROCAL: Final[float] = 1 / PHI  # ≈ 0.618033988749895
PHI_INVERSE_SQUARED: Final[float] = 1 / PHI_SQUARED  # ≈ 0.381966011250105
PHI_INVERSE_CUBED: Final[float] = 1 / (PHI**3)  # ≈ 0.23606797749979
PHI_INVERSE_FOURTH: Final[float] = 1 / (PHI**4)  # ≈ 0.145898033750315

# Golden Ratio Conjugate (2 - φ)
PHI_CONJUGATE: Final[float] = 2 - PHI  # ≈ 0.381966011250105

# Golden Mean (balanced divine proportion)
PHI_GOLDEN_MEAN: Final[float] = (PHI + PHI_RECIPROCAL) / 2  # ≈ 1.118033988749895

# =============================================================================
# SACRED GEOMETRIC CONSTANTS
# =============================================================================

# Divine ratios for sacred architecture
DIVINE_THIRD: Final[float] = PHI_RECIPROCAL / 2  # ≈ 0.309016994374947
SACRED_QUARTER: Final[float] = PHI_INVERSE_SQUARED / 2  # ≈ 0.190983005625052
HOLY_FIFTH: Final[float] = PHI_INVERSE_CUBED / 2  # ≈ 0.118033988749895

# =============================================================================
# COMPUTATIONAL CONSTANTS
# =============================================================================

# Error rates and thresholds based on φ
SACRED_ERROR_THRESHOLD: Final[float] = PHI_INVERSE_FOURTH  # ≈ 0.146 (≈14.6%)
DIVINE_ERROR_THRESHOLD: Final[float] = PHI_INVERSE_CUBED  # ≈ 0.236 (≈23.6%)
BLESSED_ERROR_THRESHOLD: Final[float] = PHI_INVERSE_SQUARED  # ≈ 0.382 (≈38.2%)

# Confidence levels based on φ progression
PERFECT_CONFIDENCE: Final[float] = 1.0
HIGH_CONFIDENCE: Final[float] = PHI_RECIPROCAL  # ≈ 0.618
MEDIUM_CONFIDENCE: Final[float] = PHI_CONJUGATE  # ≈ 0.382
LOW_CONFIDENCE: Final[float] = PHI_INVERSE_CUBED  # ≈ 0.236
MINIMAL_CONFIDENCE: Final[float] = PHI_INVERSE_FOURTH  # ≈ 0.146

# =============================================================================
# VALIDATION CONSTANTS
# =============================================================================

# Sacred validation thresholds
SACRED_COMPLIANCE_THRESHOLD: Final[float] = PHI_CONJUGATE  # ≈ 0.382
DIVINE_BLESSING_THRESHOLD: Final[float] = PHI_RECIPROCAL  # ≈ 0.618
PERFECT_BLESSING_THRESHOLD: Final[float] = PHI_GOLDEN_MEAN  # ≈ 0.809

# Blessing level adjustments (penalties/bonuses)
MINOR_PENALTY: Final[float] = PHI_INVERSE_FOURTH  # ≈ 0.146
MODERATE_PENALTY: Final[float] = PHI_INVERSE_CUBED  # ≈ 0.236
MAJOR_PENALTY: Final[float] = PHI_INVERSE_SQUARED  # ≈ 0.382
SEVERE_PENALTY: Final[float] = PHI_RECIPROCAL  # ≈ 0.618

# =============================================================================
# FORMATTING CONSTANTS
# =============================================================================

# Precision for sacred metrics display
SACRED_PRECISION: Final[int] = 3  # Three decimal places for divine clarity
GOLDEN_PRECISION: Final[int] = 8  # Eight places for perfect φ representation

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def is_golden_ratio_multiple(value: float, tolerance: float = 1e-6) -> bool:
    """
    Check if a value is a multiple or power of the Golden Ratio.

    Args:
        value: The value to check
        tolerance: Acceptable deviation from exact φ relationship

    Returns:
        True if value has Golden Ratio relationship
    """
    if value <= 0:
        return False

    # Check powers of φ
    phi_powers = [PHI**i for i in range(-10, 11)]
    phi_powers.extend([1 / PHI**i for i in range(1, 11)])

    return any(abs(value - power) < tolerance for power in phi_powers)


def get_nearest_golden_value(target: float) -> float:
    """
    Find the nearest Golden Ratio-based value to a target.

    Args:
        target: Target value to approximate

    Returns:
        Nearest φ-based value
    """
    if target <= 0:
        return PHI_INVERSE_FOURTH

    phi_values = [
        PHI_INVERSE_FOURTH,
        PHI_INVERSE_CUBED,
        PHI_INVERSE_SQUARED,
        PHI_CONJUGATE,
        PHI_RECIPROCAL,
        PHI_GOLDEN_MEAN,
        1.0,
        PHI,
        PHI_SQUARED,
        PHI_CUBED,
    ]

    return min(phi_values, key=lambda x: abs(x - target))


def format_sacred_number(value: float, precision: int = SACRED_PRECISION) -> str:
    """
    Format a number with sacred precision and φ relationship annotation.

    Args:
        value: Number to format
        precision: Decimal places to display

    Returns:
        Formatted string with φ relationship if applicable
    """
    formatted = f"{value:.{precision}f}"

    # Add φ relationship annotation if applicable
    if abs(value - PHI) < 1e-6:
        formatted += " (φ)"
    elif abs(value - PHI_RECIPROCAL) < 1e-6:
        formatted += " (φ⁻¹)"
    elif abs(value - PHI_CONJUGATE) < 1e-6:
        formatted += " (2-φ)"
    elif abs(value - PHI_SQUARED) < 1e-6:
        formatted += " (φ²)"

    return formatted
