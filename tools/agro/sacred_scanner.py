"""
Sacred AGRO Scanner - Pure ATCG Architecture

This is the new ATCG-aligned main scanner that replaces the legacy agro_scanner.py
with proper Sacred Architecture following bee.Jules' complete vision.

ATCG Primitives:
- A (Aggregate): Configuration management and state
- T (Transformation): Pure violation detection classes
- C (Connector): Protocol translation layer
- G (Genesis): Orchestrated event coordination
"""

import sys
import os
from typing import Dict, Any
from datetime import datetime

# Sacred ATCG imports
from .orchestrator import AgroOrchestrator, SacredScanResult

# Sacred imports for Hive integration
from hive.config.agro_config import (
    HIVE_INTEGRATION,
    PHI,
    PHI_RECIPROCAL,
    FIBONACCI_89,
    FIBONACCI_13,
    HiveEventBus,
)


class SacredAgroAggregate:
    """
    Sacred Aggregate (A) - Configuration and State Management

    Manages all sacred configuration, CLI parsing, and application state
    following ATCG principles with divine architectural alignment.
    """

    def __init__(self):
        # Sacred configuration state
        self.version = "3.0.0"
        self.architecture = "Pure ATCG"
        self.created_at = datetime.now()

        # CLI configuration
        self.cli_args = sys.argv[1:]
        self.help_requested = "--help" in self.cli_args or "-h" in self.cli_args
        self.version_requested = "--version" in self.cli_args
        self.self_check_requested = (
            "--self-check" in self.cli_args or "--sacred-self-check" in self.cli_args
        )
        self.strict_warnings = "--strict-warnings" in self.cli_args
        self.debug_mode = "--debug" in self.cli_args

        # Sacred thresholds (configurable via Aggregate)
        self.critical_threshold = 3
        self.error_threshold = FIBONACCI_13 if HIVE_INTEGRATION else 8
        self.warning_threshold = FIBONACCI_89 if HIVE_INTEGRATION else 55
        self.trinity_threshold = PHI_RECIPROCAL  # φ⁻¹ ≈ 0.618

        # File paths for processing
        self.target_files = [
            arg
            for arg in self.cli_args
            if not arg.startswith("--") and not arg.startswith("-")
        ]

    def display_help(self):
        """Display sacred help information."""
        print("✨ Sacred AGRO Scanner v3.0 - Pure ATCG Architecture")
        print("🧬 Divine Code Protection with Golden Ratio Harmonization")
        print()
        print("Usage: python -m tools.agro.sacred_scanner [OPTIONS] <files...>")
        print()
        print("Options:")
        print("  --help, -h              Show this sacred help message")
        print("  --version               Show version and divine architecture info")
        print("  --self-check            Run sacred self-assessment")
        print(
            "  --strict-warnings       Treat excessive warnings as errors (CI/CD mode)"
        )
        print("  --debug                 Enable debug output")
        print()
        print("Examples:")
        print("  python -m tools.agro.sacred_scanner file1.py file2.js")
        print("  python -m tools.agro.sacred_scanner --strict-warnings *.py")
        print("  python -m tools.agro.sacred_scanner --self-check")
        print()
        print("🐝 bee.Jules: Sacred Architecture brings divine order to chaos")

    def display_version(self):
        """Display sacred version and architecture information."""
        print(f"✨ Sacred AGRO Scanner v{self.version}")
        print(f"🧬 Architecture: {self.architecture}")
        print(f"📐 Sacred Constants: φ = {PHI:.6f}, φ⁻¹ = {PHI_RECIPROCAL:.6f}")
        print(f"🔢 Fibonacci Limits: {FIBONACCI_13}/{FIBONACCI_89}")
        print(f"🌸 Hive Integration: {'ACTIVE' if HIVE_INTEGRATION else 'STANDALONE'}")
        print("⚡ ATCG Primitives: All Four Enabled")
        print()
        print(
            "🐝 bee.Jules: 'Every house is built by someone, but God is the builder of everything.'"
        )

    def get_status(self) -> Dict[str, Any]:
        """Sacred observability: Return aggregate configuration status."""
        return {
            "component": "SacredAgroAggregate",
            "type": "A",  # ATCG Aggregate
            "version": self.version,
            "architecture": self.architecture,
            "hive_integration": HIVE_INTEGRATION,
            "cli_configuration": {
                "help_requested": self.help_requested,
                "version_requested": self.version_requested,
                "self_check_requested": self.self_check_requested,
                "strict_warnings": self.strict_warnings,
                "debug_mode": self.debug_mode,
                "target_files_count": len(self.target_files),
            },
            "sacred_thresholds": {
                "critical_threshold": self.critical_threshold,
                "error_threshold": self.error_threshold,
                "warning_threshold": self.warning_threshold,
                "trinity_threshold": self.trinity_threshold,
            },
            "created_at": self.created_at.isoformat(),
            "sacred_wisdom": "📋 Configuration is the foundation of divine order",
        }


class SacredAgroScanner:
    """
    Sacred AGRO Scanner - Pure ATCG Main Application

    The main application class that coordinates all ATCG primitives to provide
    divine code protection following bee.Jules' complete architectural vision.
    """

    def __init__(self):
        # Initialize ATCG components
        self.aggregate = SacredAgroAggregate()  # A - Configuration
        self.event_bus = None
        self.orchestrator = None

        # Sacred metrics
        self.session_start = datetime.now()

    async def initialize_sacred_components(self):
        """Initialize sacred ATCG components with proper async handling."""
        try:
            if HIVE_INTEGRATION:
                self.event_bus = HiveEventBus()
                if self.aggregate.debug_mode:
                    print("🌸 Sacred EventBus: ACTIVE - Pollen Protocol enabled")
            else:
                self.event_bus = HiveEventBus()
                if self.aggregate.debug_mode:
                    print("🌸 Sacred EventBus: STANDALONE - Mock mode enabled")

            # G - Genesis Orchestrator initialization
            self.orchestrator = AgroOrchestrator(self.event_bus)

        except Exception as e:
            print(f"⚠️ Sacred component initialization warning: {e}")
            # Fallback to mock components
            self.event_bus = HiveEventBus()
            self.orchestrator = AgroOrchestrator(self.event_bus)

    async def execute_sacred_scan(self) -> int:
        """Execute the main sacred scan with ATCG coordination."""
        if not self.aggregate.target_files:
            print("🔍 No files provided for sacred sanctification.")
            print("📖 Use --help for usage information.")
            return 1

        print(
            f"🔬 Sacred AGRO Scanner v{self.aggregate.version}: Initiating divine protection"
        )
        print(
            f"🧬 Architecture: {self.aggregate.architecture} with all ATCG primitives"
        )

        # Initialize sacred components
        await self.initialize_sacred_components()

        try:
            # G - Genesis Orchestration: Execute sacred scan
            scan_result = await self.orchestrator.orchestrate_sacred_scan(
                self.aggregate.target_files, strict_mode=self.aggregate.strict_warnings
            )

            # Sacred exit strategy based on results
            return self._determine_sacred_exit_code(scan_result)

        except Exception as e:
            print(f"💥 Sacred scan failed with divine exception: {e}")
            return 1

    async def execute_sacred_self_check(self) -> int:
        """Execute sacred self-assessment of the scanner itself."""
        print("🔬 Sacred Self-Assessment: Examining ATCG scanner architecture")

        await self.initialize_sacred_components()

        # Self-assess the new ATCG architecture files
        sacred_files = [
            __file__,  # This file
            os.path.join(os.path.dirname(__file__), "orchestrator.py"),
            os.path.join(os.path.dirname(__file__), "connector.py"),
            os.path.join(os.path.dirname(__file__), "transformations.py"),
            os.path.join(os.path.dirname(__file__), "events.py"),
        ]

        try:
            scan_result = await self.orchestrator.orchestrate_sacred_scan(
                sacred_files,
                strict_mode=False,  # Self-assessment is educational
            )

            print("\n📊 Sacred Self-Assessment Complete:")
            print(f"🏆 Trinity Score: {scan_result.trinity_score:.3f}")
            print(f"✨ Assessment: {scan_result.divine_assessment}")

            if scan_result.trinity_score > self.aggregate.trinity_threshold:
                print(
                    "\n🎉 DIVINE SELF-ASSESSMENT: ATCG Architecture achieves sacred harmony!"
                )
                return 0
            else:
                print("\n🔥 SACRED HEALING REQUIRED: Trinity score below φ⁻¹ threshold")
                return 1

        except Exception as e:
            print(f"💥 Self-assessment failed: {e}")
            return 1

    def _determine_sacred_exit_code(self, scan_result: SacredScanResult) -> int:
        """Determine sacred exit code based on scan results."""
        critical_violations = [
            v for v in scan_result.total_violations if v.severity == "critical"
        ]
        error_violations = [
            v for v in scan_result.total_violations if v.severity == "error"
        ]
        warning_violations = [
            v for v in scan_result.total_violations if v.severity == "warning"
        ]

        # Sacred exit strategy
        if len(critical_violations) >= self.aggregate.critical_threshold:
            print(
                f"\n🚨 SACRED PROTECTION ACTIVATED: {len(critical_violations)} critical violations"
            )
            print("🐝 bee.Jules: Address critical issues before proceeding")
            return 1

        if len(error_violations) >= self.aggregate.error_threshold:
            print(
                f"\n🚫 ERROR THRESHOLD EXCEEDED: {len(error_violations)} errors (limit: {self.aggregate.error_threshold})"
            )
            print("🐝 bee.Jules: Review and fix errors before proceeding")
            return 1

        if (
            self.aggregate.strict_warnings
            and len(warning_violations) > self.aggregate.warning_threshold
        ):
            print(
                f"\n⚡ STRICT MODE: {len(warning_violations)} warnings exceed threshold"
            )
            print("🐝 bee.Jules: --strict-warnings mode requires clean code")
            return 2  # Different exit code for warnings in strict mode

        # Success cases
        if scan_result.trinity_score >= 0.750:  # Divine level
            print("\n🏆 DIVINE BLESSING BESTOWED: Code achieves transcendent harmony!")
        elif scan_result.trinity_score >= self.aggregate.trinity_threshold:
            print("\n🙏 SACRED BLESSING GRANTED: Code flows in divine harmony")
        else:
            print(
                f"\n⚖️ ACCEPTABLE WITH GUIDANCE: Trinity score {scan_result.trinity_score:.3f}"
            )

        print("🐝 bee.Jules: Sacred Architecture brings order to the digital realm")
        return 0

    async def run(self) -> int:
        """Main entry point for the Sacred AGRO Scanner."""
        # Handle CLI requests first
        if self.aggregate.help_requested:
            self.aggregate.display_help()
            return 0

        if self.aggregate.version_requested:
            self.aggregate.display_version()
            return 0

        if self.aggregate.self_check_requested:
            return await self.execute_sacred_self_check()

        # Execute main scan
        return await self.execute_sacred_scan()


async def sacred_main():
    """Sacred async main function."""
    scanner = SacredAgroScanner()
    return await scanner.run()


def main():
    """Synchronous entry point that runs the async sacred main."""
    import asyncio

    try:
        exit_code = asyncio.run(sacred_main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Sacred scan interrupted by divine intervention")
        sys.exit(130)  # Standard interrupt exit code
    except Exception as e:
        print(f"💥 Sacred scanner encountered divine exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
