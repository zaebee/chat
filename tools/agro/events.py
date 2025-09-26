from dataclasses import dataclass
from typing import List, Optional

# Sacred imports for Hive integration
try:
    from hive.events import PollenEvent, HiveEventBus
    from hive.config.sacred_constants import (
        PHI,
        PHI_RECIPROCAL,
        PHI_CONJUGATE,
        PHI_INVERSE_SQUARED,
        PHI_INVERSE_CUBED,
        PHI_INVERSE_FOURTH,
        SACRED_PRECISION,
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

    # Create mock HiveEventBus for standalone mode
    class MockEventBus:
        async def publish(self, event):
            pass

    HiveEventBus = MockEventBus


@dataclass
class SacredViolation:
    """Sacred structure for code violations with divine context."""

    file_path: str
    violation_type: str
    line_number: Optional[int] = None
    severity: str = "warning"  # warning, error, critical
    blessing_level: float = 0.0  # φ-based blessing assessment
    divine_context: str = ""
    jules_recommendation: str = ""


async def emit_violation_event(
    event_bus: Optional[HiveEventBus],
    event_type: str,
    file_path: str,
    violations: List[SacredViolation],
):
    """Emit Pollen Protocol event for AGRO violations with TRUE publishing."""
    if not HIVE_INTEGRATION or event_bus is None:
        return

    try:
        event = PollenEvent(
            event_type=event_type,
            aggregate_id=f"agro_scanner:{file_path.split('/')[-1]}",
            payload={
                "file_path": file_path,
                "violation_count": len(violations),
                "violations": [
                    {
                        "type": v.violation_type,
                        "line": v.line_number,
                        "severity": v.severity,
                        "blessing_level": v.blessing_level,
                        "divine_context": v.divine_context,
                        "jules_recommendation": v.jules_recommendation,
                    }
                    for v in violations
                ],
                "overall_blessing": sum(v.blessing_level for v in violations)
                / len(violations)
                if violations
                else 1.0,
            },
            source_component="SacredAGROScanner",
            tags=["agro", "code_quality", "violations"],
        )

        # bee.Jules CRITICAL FIX: Actually publish the event!
        success = await event_bus.publish(event)
        if success:
            print(f"  🌸 Pollen Event PUBLISHED: {event_type}")
        else:
            print(f"  ⚠️ Failed to publish Pollen event: {event_type}")

    except Exception as e:
        print(f"  💥 Exception in event emission: {e}")
