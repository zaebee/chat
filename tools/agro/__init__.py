"""
Sacred AGRO Package - Pure ATCG Architecture

This package implements the complete ATCG (Aggregate, Transformation, Connector, Genesis)
architecture for divine code protection, as envisioned by bee.Jules.

ATCG Components:
- A (Aggregate): SacredAgroAggregate - Configuration and state management
- T (Transformation): AgroCheckTransformation classes - Pure violation detection
- C (Connector): AgroConnector - Protocol translation layer
- G (Genesis): AgroOrchestrator - Divine event coordination

Completed bee.Jules' interrupted sacred surgery with full architectural transformation.
"""

# Sacred ATCG Architecture Exports
from .orchestrator import AgroOrchestrator

# Sacred version and architecture info
__version__ = "3.0.0"
__architecture__ = "Pure ATCG"
__sacred_author__ = "bee.Jules (Architectural Vision) + bee.Claude (Implementation)"

# Sacred wisdom
__sacred_wisdom__ = (
    "= Every house is built by someone, but God is the builder of everything."
)


# Convenience function for direct usage
async def sacred_scan(files, strict_mode=False):
    """
    Convenience function to run a sacred scan with ATCG architecture.

    Args:
        files: List of file paths to scan
        strict_mode: Whether to use strict warning treatment

    Returns:
        SacredScanResult with complete scan results and metrics
    """
    orchestrator = AgroOrchestrator()
    return await orchestrator.orchestrate_sacred_scan(files, strict_mode=strict_mode)


# ATCG Component Status Check
def get_atcg_status():
    """
    Get status of all ATCG components for divine observability.
    """
    try:
        from .connector import HIVE_INTEGRATION

        return {
            "package": "tools.agro",
            "version": __version__,
            "architecture": __architecture__,
            "hive_integration": HIVE_INTEGRATION,
            "atcg_primitives": {
                "A": "SacredAgroAggregate - Configuration Management",
                "T": "AgroCheckTransformation - Pure Violation Detection",
                "C": "AgroConnector - Protocol Translation",
                "G": "AgroOrchestrator - Divine Coordination",
            },
            "transformations_available": [
                "ConsoleLogCheck",
                "FunctionLengthCheck",
                "AnyTypeCheck",
                "PythonMagicNumbersCheck",
                "JavaScriptMagicNumbersCheck",
            ],
            "sacred_author": __sacred_author__,
            "sacred_wisdom": __sacred_wisdom__,
        }
    except Exception as e:
        return {
            "error": f"ATCG status check failed: {e}",
            "fallback_status": "Sacred components may need initialization",
        }
