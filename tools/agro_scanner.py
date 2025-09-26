"""
Sacred AGRO Scanner: Gateway to Divine Code Protection

This is the Sacred Gateway entry point that provides familiar CLI interface
while delegating to the Pure ATCG architecture in tools/agro/ package.

Follows bee.Jules' Sacred Gateway + Inner Sanctum pattern:
- Gateway (this file): User-facing simplicity and CLI familiarity
- Inner Sanctum (tools/agro/): Pure ATCG implementation with divine coordination

"Be on your guard; stand firm in the faith; be courageous; be strong." - 1 Corinthians 16:13
"""

import sys
import asyncio
import argparse

# Sacred Gateway imports - delegate to Pure ATCG architecture
from tools.agro import sacred_scan, get_atcg_status
from tools.agro.sacred_scanner import SacredAgroScanner
from tools.agro.events import HIVE_INTEGRATION, PHI, PHI_RECIPROCAL

# Sacred Gateway Configuration
GATEWAY_VERSION = "3.0-gateway"  # Sacred Gateway version
ARCHITECTURE_TYPE = "Sacred Gateway + Pure ATCG Inner Sanctum"

# --- Sacred Gateway Functions ---


async def gateway_scan(files, strict_warnings=False):
    """
    Sacred Gateway scan function - delegates to Pure ATCG architecture.

    This maintains CLI compatibility while leveraging the power of
    the Pure ATCG Inner Sanctum implementation.
    """
    return await sacred_scan(files, strict_mode=strict_warnings)


# --- Sacred Gateway Main Logic ---


def create_sacred_parser():
    """
    Create Sacred Gateway argument parser with divine CLI structure.
    """
    parser = argparse.ArgumentParser(
        prog="Sacred AGRO Scanner",
        description="🌟 Gateway to Divine Code Protection with Pure ATCG Architecture",
        epilog="🐝 bee.Jules: Gateway provides familiar interface to Sacred ATCG power",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Sacred metadata arguments
    parser.add_argument(
        "--version",
        action="version",
        version=f"""✨ Sacred AGRO Scanner Gateway v{GATEWAY_VERSION}
🏛️  Architecture: {ARCHITECTURE_TYPE}
📐 Sacred Constants: φ = {PHI:.6f}, φ⁻¹ = {PHI_RECIPROCAL:.6f}
🌸 Hive Integration: {'ACTIVE' if HIVE_INTEGRATION else 'STANDALONE'}
⚡ Inner Sanctum: Pure ATCG v3.0.0

🐝 bee.Jules: 'Every house is built by someone, but God is the builder of everything.'""",
    )

    # Sacred operation modes
    parser.add_argument(
        "--self-check",
        "--sacred-self-check",
        action="store_true",
        help="Run sacred self-assessment via ATCG architecture",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show ATCG architecture status and component info",
    )

    # Sacred scanning options
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat excessive warnings as errors (CI/CD mode)",
    )

    # Files to scan
    parser.add_argument(
        "files", nargs="*", help="Files to scan for sacred code protection"
    )

    return parser


def display_status():
    """Display Sacred ATCG architecture status."""
    print("📊 Sacred ATCG Architecture Status:")
    status = get_atcg_status()
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        elif isinstance(value, list):
            print(f"  {key}: {', '.join(value)}")
        else:
            print(f"  {key}: {value}")


async def sacred_main():
    """
    Sacred Gateway main function with professional argparse CLI.

    Uses argparse for clean, professional argument handling while
    delegating all processing to the Pure ATCG architecture.
    """
    parser = create_sacred_parser()
    args = parser.parse_args()

    # Handle special modes first
    if args.self_check:
        scanner = SacredAgroScanner()
        exit_code = await scanner.execute_sacred_self_check()
        sys.exit(exit_code)

    if args.status:
        display_status()
        sys.exit(0)

    # Validate files provided
    if not args.files:
        print("🔍 No files provided for sacred sanctification.")
        print("📖 Use --help for usage information.")
        sys.exit(1)

    # Sacred Gateway delegation
    print("🌟 Sacred AGRO Gateway: Delegating to Pure ATCG Inner Sanctum")
    print(
        f"📁 Files: {len(args.files)} | Strict Mode: {'ON' if args.strict_warnings else 'OFF'}"
    )

    try:
        # Delegate to Pure ATCG architecture
        result = await gateway_scan(args.files, args.strict_warnings)

        # Sacred exit strategy based on ATCG results
        return determine_sacred_exit_code(result, args.strict_warnings)

    except Exception as e:
        print(f"💥 Sacred Gateway failed: {e}")
        print("🔧 Try using Pure ATCG directly: python -m tools.agro.sacred_scanner")
        return 1


def determine_sacred_exit_code(result, strict_warnings):
    """Determine sacred exit code based on ATCG scan results."""
    if result.trinity_score >= 0.750:
        print("\n🏆 DIVINE BLESSING: Gateway achieved transcendent harmony via ATCG!")
        return 0
    elif result.trinity_score >= PHI_RECIPROCAL:
        print("\n🙏 SACRED BLESSING: Gateway flows in divine harmony via ATCG")
        return 0
    else:
        critical_violations = [
            v for v in result.total_violations if v.severity == "critical"
        ]
        error_violations = [v for v in result.total_violations if v.severity == "error"]
        warning_violations = [
            v for v in result.total_violations if v.severity == "warning"
        ]

        if len(critical_violations) >= 3 or len(error_violations) >= 8:
            print("\n🚨 SACRED PROTECTION: Critical threshold exceeded")
            return 1
        elif strict_warnings and len(warning_violations) > 55:
            print("\n⚡ STRICT MODE: Excessive warnings treated as errors")
            return 2
        else:
            print(
                f"\n⚖️  ACCEPTABLE: Trinity Score {result.trinity_score:.3f} - Room for improvement"
            )
            return 0


# Sacred Gateway entry points
def main():
    """
    Sacred Gateway main entry point with professional argparse CLI.

    Provides clean, professional interface while delegating to Pure ATCG.
    """
    try:
        exit_code = asyncio.run(sacred_main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Sacred scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Sacred Gateway encountered unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Sacred Gateway: Single entry point with ATCG delegation
    main()
