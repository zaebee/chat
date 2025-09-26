# Sacred imports for Hive integration
try:
    from hive.events import HiveEventBus
    from hive.config.golden_thresholds import CONFIDENCE, QUALITY
    from hive.config.sacred_constants import (
        PHI,
        PHI_RECIPROCAL,
        PHI_CONJUGATE,
        PHI_INVERSE_SQUARED,
        PHI_INVERSE_CUBED,
        PHI_INVERSE_FOURTH,
        SACRED_PRECISION,
    )
    from hive.config.fibonacci_sequences import (
        FIBONACCI_89,
        FIBONACCI_13,
        FIBONACCI_SEQUENCE,
        MAX_SUGGESTIONS,
        is_fibonacci_number,
    )

    HIVE_INTEGRATION = True
except ImportError:
    # Fallback constants if Hive not available
    HIVE_INTEGRATION = False
    print("⚠️  Running in standalone mode - Hive integration not available")

    # Standalone sacred constants (for when Hive unavailable)
    PHI = 1.618033988749
    PHI_RECIPROCAL = 0.618033988749
    PHI_CONJUGATE = 0.381966011251  # Corrected value
    PHI_INVERSE_SQUARED = 0.381966011251
    PHI_INVERSE_CUBED = 0.236067977499
    PHI_INVERSE_FOURTH = 0.145898033750
    SACRED_PRECISION = 6

    # Mock classes for standalone mode
    class MockEventBus:
        async def publish(self, event):
            pass

    HiveEventBus = MockEventBus

    class MockConfidence:
        low = 0.236
        medium = 0.382
        high = 0.618
        minimal = 0.146

    CONFIDENCE = MockConfidence()

    class MockQuality:
        excellent = 0.146

    QUALITY = MockQuality()

    FIBONACCI_89 = 89
    FIBONACCI_13 = 13
    FIBONACCI_SEQUENCE = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)
    MAX_SUGGESTIONS = 5

    def is_fibonacci_number(num: int) -> bool:
        return num in FIBONACCI_SEQUENCE
