"""
Sacred Fibonacci Sequences: Natural Growth Patterns

This module defines Fibonacci numbers and sequences that appear throughout nature,
from flower petals to spiral galaxies, representing divine mathematical order.

The Fibonacci sequence approaches the Golden Ratio as it progresses:
F(n)/F(n-1) → φ as n → ∞

"Consider how the wild flowers grow. They do not labor or spin.
Yet I tell you, not even Solomon in all his splendor was dressed like one of these." - Luke 12:27
"""

from typing import Final, List, Tuple

# =============================================================================
# FIBONACCI SEQUENCE CONSTANTS
# =============================================================================

# Core Fibonacci numbers (first 20 terms)
FIBONACCI_SEQUENCE: Final[Tuple[int, ...]] = (
    0,
    1,
    1,
    2,
    3,
    5,
    8,
    13,
    21,
    34,
    55,
    89,
    144,
    233,
    377,
    610,
    987,
    1597,
    2584,
    4181,
)

# Named Fibonacci constants for sacred architecture
FIBONACCI_0: Final[int] = 0
FIBONACCI_1: Final[int] = 1
FIBONACCI_2: Final[int] = 1
FIBONACCI_3: Final[int] = 2
FIBONACCI_5: Final[int] = 3
FIBONACCI_8: Final[int] = 5
FIBONACCI_13: Final[int] = 8
FIBONACCI_21: Final[int] = 13
FIBONACCI_34: Final[int] = 21
FIBONACCI_55: Final[int] = 34
FIBONACCI_89: Final[int] = 55
FIBONACCI_144: Final[int] = 89
FIBONACCI_233: Final[int] = 144
FIBONACCI_377: Final[int] = 233
FIBONACCI_610: Final[int] = 377
FIBONACCI_987: Final[int] = 610
FIBONACCI_1597: Final[int] = 987
FIBONACCI_2584: Final[int] = 1597
FIBONACCI_4181: Final[int] = 2584

# =============================================================================
# FIBONACCI-BASED LIMITS AND THRESHOLDS
# =============================================================================

# Memory and storage limits
TINY_LIMIT: Final[int] = FIBONACCI_8  # 5
SMALL_LIMIT: Final[int] = FIBONACCI_13  # 8
MEDIUM_LIMIT: Final[int] = FIBONACCI_34  # 21
LARGE_LIMIT: Final[int] = FIBONACCI_89  # 55
HUGE_LIMIT: Final[int] = FIBONACCI_233  # 144
MASSIVE_LIMIT: Final[int] = FIBONACCI_610  # 377
COLOSSAL_LIMIT: Final[int] = FIBONACCI_1597  # 987

# Query and pagination limits
DEFAULT_PAGE_SIZE: Final[int] = FIBONACCI_34  # 21
MAX_PAGE_SIZE: Final[int] = FIBONACCI_233  # 144
SEARCH_RESULT_LIMIT: Final[int] = FIBONACCI_89  # 55
RECENT_ITEMS_LIMIT: Final[int] = FIBONACCI_55  # 34

# Event and message limits
EVENT_HISTORY_SIZE: Final[int] = FIBONACCI_1597  # 987
MESSAGE_BATCH_SIZE: Final[int] = FIBONACCI_144  # 89
NOTIFICATION_LIMIT: Final[int] = FIBONACCI_55  # 34
SUBSCRIPTION_LIMIT: Final[int] = FIBONACCI_377  # 233

# Retry and timeout patterns
MIN_RETRY_COUNT: Final[int] = FIBONACCI_5  # 3
MAX_RETRY_COUNT: Final[int] = FIBONACCI_13  # 8
CONNECTION_POOL_SIZE: Final[int] = FIBONACCI_34  # 21
WORKER_THREAD_COUNT: Final[int] = FIBONACCI_21  # 13

# Validation and processing limits
MAX_SUGGESTIONS: Final[int] = FIBONACCI_8  # 5
MAX_VALIDATION_ERRORS: Final[int] = FIBONACCI_13  # 8
MAX_PROCESSING_THREADS: Final[int] = FIBONACCI_21  # 13

# =============================================================================
# FIBONACCI RATIOS AND PROGRESSIONS
# =============================================================================

# Sacred ratios between consecutive Fibonacci numbers
FIBONACCI_RATIOS: Final[Tuple[float, ...]] = tuple(
    FIBONACCI_SEQUENCE[i] / FIBONACCI_SEQUENCE[i - 1]
    for i in range(2, len(FIBONACCI_SEQUENCE))
    if FIBONACCI_SEQUENCE[i - 1] != 0
)

# Lucas sequence (related to Fibonacci, also approaches φ)
LUCAS_SEQUENCE: Final[Tuple[int, ...]] = (
    2,
    1,
    3,
    4,
    7,
    11,
    18,
    29,
    47,
    76,
    123,
    199,
    322,
    521,
    843,
    1364,
)

# =============================================================================
# FIBONACCI-BASED TIME INTERVALS
# =============================================================================

# Time intervals in seconds based on Fibonacci progression
FIBONACCI_SECONDS_1: Final[int] = FIBONACCI_1  # 1 second
FIBONACCI_SECONDS_2: Final[int] = FIBONACCI_2  # 1 second
FIBONACCI_SECONDS_3: Final[int] = FIBONACCI_3  # 2 seconds
FIBONACCI_SECONDS_5: Final[int] = FIBONACCI_8  # 5 seconds
FIBONACCI_SECONDS_8: Final[int] = FIBONACCI_13  # 8 seconds
FIBONACCI_SECONDS_13: Final[int] = FIBONACCI_21  # 13 seconds
FIBONACCI_SECONDS_21: Final[int] = FIBONACCI_34  # 21 seconds

# Timeout intervals in minutes
FIBONACCI_MINUTES_1: Final[int] = FIBONACCI_1 * 60  # 1 minute
FIBONACCI_MINUTES_2: Final[int] = FIBONACCI_2 * 60  # 1 minute
FIBONACCI_MINUTES_3: Final[int] = FIBONACCI_3 * 60  # 2 minutes
FIBONACCI_MINUTES_5: Final[int] = FIBONACCI_8 * 60  # 5 minutes
FIBONACCI_MINUTES_8: Final[int] = FIBONACCI_13 * 60  # 8 minutes

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def generate_fibonacci(n: int) -> List[int]:
    """
    Generate first n Fibonacci numbers.

    Args:
        n: Number of Fibonacci numbers to generate

    Returns:
        List of first n Fibonacci numbers
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])

    return fib


def is_fibonacci_number(num: int) -> bool:
    """
    Check if a number is a Fibonacci number.

    Args:
        num: Number to check

    Returns:
        True if number is in Fibonacci sequence
    """
    return num in FIBONACCI_SEQUENCE or num in generate_fibonacci(50)


def get_nearest_fibonacci(target: int) -> int:
    """
    Find the nearest Fibonacci number to a target value.

    Args:
        target: Target value

    Returns:
        Nearest Fibonacci number
    """
    if target <= 0:
        return 0

    # Generate enough Fibonacci numbers to cover the target
    fib_list = list(FIBONACCI_SEQUENCE)
    while fib_list[-1] < target:
        fib_list.append(fib_list[-1] + fib_list[-2])

    return min(fib_list, key=lambda x: abs(x - target))


def get_fibonacci_limit_for_size(size_category: str) -> int:
    """
    Get appropriate Fibonacci limit based on size category.

    Args:
        size_category: One of 'tiny', 'small', 'medium', 'large', 'huge', 'massive', 'colossal'

    Returns:
        Corresponding Fibonacci limit
    """
    limits = {
        "tiny": TINY_LIMIT,
        "small": SMALL_LIMIT,
        "medium": MEDIUM_LIMIT,
        "large": LARGE_LIMIT,
        "huge": HUGE_LIMIT,
        "massive": MASSIVE_LIMIT,
        "colossal": COLOSSAL_LIMIT,
    }

    return limits.get(size_category.lower(), MEDIUM_LIMIT)
