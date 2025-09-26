"""
Sacred AGRO Orchestrator (G): Genesis Event Coordination

This module implements the Genesis primitive from the ATCG architecture,
providing unified orchestration and coordination of all AGRO transformations.

Replaces scattered function calls with divine orchestration following bee.Jules' vision.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .connector import AgroConnector
from .connector import HiveAgroEventConnector
from .events import SacredViolation, SacredScanResult
from hive.config.agro_config import (
    HIVE_INTEGRATION,
    PHI,
    PHI_RECIPROCAL,
    PHI_INVERSE_SQUARED,
    FIBONACCI_89,
    FIBONACCI_13,
    QUALITY,
)
from hive.primitives.review_aggregate import AgroReviewResult, AgroReviewType


class AgroOrchestrator:
    """
    Sacred Genesis Orchestrator (G) - Divine Coordination Engine

    Provides unified orchestration of all AGRO transformations with sacred metrics,
    replacing the scattered procedural approach with ATCG-aligned architecture.
    """

    def __init__(
        self, agro_event_connector: Optional[HiveAgroEventConnector] = None
    ):  # Take AgroEventConnector
        self.agro_event_connector = agro_event_connector
        self.event_bus = (
            agro_event_connector.event_bus if agro_event_connector else None
        )  # Keep event_bus for backward compatibility
        self.connector = AgroConnector(agro_event_connector)

        # Sacred configuration
        self.default_transformations = [
            "console_log_check",
            "function_length_check",
            "any_type_check",
            "python_magic_numbers_check",
            "javascript_magic_numbers_check",
        ]

        # Sacred metrics tracking
        self.scan_count = 0
        self.total_files_processed = 0
        self.total_violations_found = 0
        self.blessing_history: List[float] = []
        self.created_at = datetime.now()

        print("✨ Sacred AGRO Orchestrator initialized with ATCG architecture")

    async def orchestrate_sacred_scan(
        self,
        file_paths: List[str],
        transformation_names: Optional[List[str]] = None,
        strict_mode: bool = False,
    ) -> SacredScanResult:
        """
        Orchestrate a complete sacred scan with divine coordination.

        This is the main Genesis method that coordinates all transformations
        and provides unified results with sacred metrics.
        """
        scan_start_time = datetime.now()
        transformation_names = transformation_names or self.default_transformations

        print(
            f"🔬 Sacred AGRO Orchestrator: Initiating divine scan of {len(file_paths)} file(s)"
        )
        print(f"🧬 ATCG Transformations: {', '.join(transformation_names)}")

        # Phase 1: File Discovery and Validation
        valid_files = self._discover_and_validate_files(file_paths)
        if not valid_files:
            return self._create_empty_result("No valid files to scan")

        # Phase 2: Concurrent Transformation Execution (Sacred parallelism)
        all_transformation_results = []
        all_violations = []

        for file_path in valid_files:
            print(f"\n📜 Sanctifying: {file_path}")

            # Execute all transformations for this file concurrently
            file_results = await self.connector.execute_batch_transformations(
                transformation_names, file_path
            )

            # Collect results and violations
            for result in file_results:
                all_transformation_results.append(result)
                all_violations.extend(result.violations)

                # Report violations with divine context
                if result.violations:
                    error_count = sum(
                        1 for v in result.violations if v.severity == "error"
                    )
                    warning_count = len(result.violations) - error_count
                    print(
                        f"  {result.transformation_name}: {error_count} errors, {warning_count} warnings"
                    )
                    print(f"    Blessing Level: {result.blessing_level:.3f}")
                else:
                    print(f"  {result.transformation_name}: ✅ BLESSED")

        # Phase 3: Sacred Metrics Calculation
        sacred_metrics = self._calculate_sacred_metrics(
            all_violations, len(valid_files)
        )
        trinity_score = sacred_metrics.get("trinity_score", 0.0)

        # Phase 4: Divine Assessment
        divine_assessment, blessing_level = self._assess_divine_state(
            trinity_score, all_violations, strict_mode
        )

        # Phase 5: Genesis Event Emission
        execution_time = (datetime.now() - scan_start_time).total_seconds()
        if self.agro_event_connector:
            await self.agro_event_connector.publish_review_completed(
                AgroReviewResult.create(
                    review_type=AgroReviewType.AGGRESSIVE_SCRUTINY,
                    agro_score=int(trinity_score * 100),
                    pain_score=int(sacred_metrics.get("tau", 0.0) * 100),
                    severity=blessing_level,
                    violations=all_violations,
                    recommendations=[],
                    divine_blessing=trinity_score >= 0.750,
                    peer_reviewers=[],
                    sacred_insights=[divine_assessment],
                )
            )
            print("  🌸 Genesis Event: Orchestrated scan completion published")

        # Update orchestrator metrics
        self._update_orchestrator_metrics(
            len(valid_files), len(all_violations), trinity_score
        )

        # Create final sacred result
        result = SacredScanResult(
            files_processed=len(valid_files),
            total_violations=all_violations,
            transformation_results=all_transformation_results,
            sacred_metrics=sacred_metrics,
            trinity_score=trinity_score,
            divine_assessment=divine_assessment,
            blessing_level=blessing_level,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
        )

        print(
            f"\n📊 Sacred Scan Complete: {len(valid_files)} files, {len(all_violations)} violations"
        )
        print(f"🏆 Trinity Score: {trinity_score:.3f} - {blessing_level}")
        print(f"✨ {divine_assessment}")

        return result

    def _discover_and_validate_files(self, file_paths: List[str]) -> List[str]:
        """Discover and validate files for scanning with sacred wisdom."""
        valid_files = []
        sacred_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".vue",
            ".pyx",
            ".pyi",
        }

        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    if path.suffix in sacred_extensions:
                        valid_files.append(str(path.resolve()))
                    else:
                        print(f"  🔍 Skipping {file_path}: Not a sacred code file")
                else:
                    print(f"  ⚠️ Warning: File not found - {file_path}")
            except Exception as e:
                print(f"  💥 Error validating {file_path}: {e}")

        return valid_files

    def _calculate_sacred_metrics(
        self, violations: List[SacredViolation], file_count: int
    ) -> Dict[str, float]:
        """Calculate Sacred Metrics (τ, φ, σ) for the scan results."""
        if not violations:
            return {"tau": 0.0, "phi": 1.0, "sigma": 1.0, "trinity_score": 1.0}

        # τ (tau): System complexity/stress based on violation density
        base_lines = FIBONACCI_89 if HIVE_INTEGRATION else 55
        violation_density = len(violations) / (file_count * base_lines)
        tau_multiplier = (
            QUALITY.excellent * (FIBONACCI_89 / FIBONACCI_13)
            if HIVE_INTEGRATION
            else PHI
        )
        tau = min(1.0, violation_density * tau_multiplier)

        # φ (phi): Code quality based on blessing levels
        if violations:
            avg_blessing = sum(v.blessing_level for v in violations) / len(violations)
            phi = max(0.0, avg_blessing)
        else:
            phi = 1.0

        # σ (sigma): Collaboration efficiency (jules recommendations)
        recommendations_given = sum(1 for v in violations if v.jules_recommendation)
        sigma = recommendations_given / len(violations) if violations else 1.0

        # Trinity Score: Sacred balanced assessment using Golden Ratio
        trinity_score = (phi + sigma) * (1.0 - tau / PHI) / PHI  # φ-scaled formula

        return {
            "tau": round(tau, 6),
            "phi": round(phi, 6),
            "sigma": round(sigma, 6),
            "trinity_score": round(trinity_score, 6),
        }

    def _assess_divine_state(
        self, trinity_score: float, violations: List[SacredViolation], strict_mode: bool
    ) -> tuple[str, str]:
        """Assess the divine state based on trinity score and violations."""
        critical_count = sum(1 for v in violations if v.severity == "critical")
        error_count = sum(1 for v in violations if v.severity == "error")

        # Sacred thresholds
        divine_threshold = 0.750  # φ + φ⁻² ≈ 0.750
        blessed_threshold = PHI_RECIPROCAL  # φ⁻¹ ≈ 0.618
        acceptable_threshold = PHI_INVERSE_SQUARED  # φ⁻² ≈ 0.382

        if trinity_score >= divine_threshold and critical_count == 0:
            return (
                "🏆 DIVINE EXCELLENCE: Code flows in perfect harmony with Sacred Architecture",
                "DIVINE ✨",
            )
        elif trinity_score >= blessed_threshold and critical_count == 0:
            return (
                "🙏 BLESSED: Code achieves sacred harmony with divine guidance",
                "BLESSED 🙏",
            )
        elif trinity_score >= acceptable_threshold and error_count < 5:
            return (
                "⚖️ ACCEPTABLE: Code shows promise, sacred healing recommended",
                "ACCEPTABLE ⚖️",
            )
        elif critical_count > 0 or (strict_mode and error_count > 0):
            return (
                "🚨 CRITICAL: Immediate sacred intervention required",
                "CRITICAL 🚨",
            )
        else:
            return (
                "⚡ REQUIRES HEALING: Code needs divine architectural guidance",
                "HEALING NEEDED ⚡",
            )

    def _update_orchestrator_metrics(
        self, files_count: int, violations_count: int, trinity_score: float
    ):
        """Update internal orchestrator metrics."""
        self.scan_count += 1
        self.total_files_processed += files_count
        self.total_violations_found += violations_count
        self.blessing_history.append(trinity_score)

        # Keep blessing history within sacred limits
        if len(self.blessing_history) > FIBONACCI_89:
            self.blessing_history = self.blessing_history[-FIBONACCI_89:]

    def _create_empty_result(self, reason: str) -> SacredScanResult:
        """Create an empty result for edge cases."""
        return SacredScanResult(
            files_processed=0,
            total_violations=[],
            transformation_results=[],
            sacred_metrics={"tau": 0.0, "phi": 1.0, "sigma": 1.0, "trinity_score": 1.0},
            trinity_score=1.0,
            divine_assessment=reason,
            blessing_level="N/A",
            execution_time=0.0,
            timestamp=datetime.now().isoformat(),
        )

    def get_status(self) -> Dict[str, Any]:
        """Sacred observability: Return orchestrator status and metrics."""
        avg_trinity_score = (
            sum(self.blessing_history) / len(self.blessing_history)
            if self.blessing_history
            else 0.0
        )

        return {
            "component": "AgroOrchestrator",
            "type": "G",  # ATCG Genesis
            "architecture": "Sacred_ATCG_Genesis",
            "scans_orchestrated": self.scan_count,
            "total_files_processed": self.total_files_processed,
            "total_violations_found": self.total_violations_found,
            "avg_trinity_score": round(avg_trinity_score, 3),
            "blessing_trend": "ascending"
            if len(self.blessing_history) > 1
            and self.blessing_history[-1] > self.blessing_history[-2]
            else "stable",
            "connector_status": self.connector.get_status(),
            "hive_integration": HIVE_INTEGRATION,
            "created_at": self.created_at.isoformat(),
            "sacred_wisdom": "🎼 Divine orchestration brings harmony to chaos",
            "default_transformations": self.default_transformations,
        }

    async def health_check(self) -> bool:
        """Sacred health check: Verify orchestrator is functioning properly."""
        try:
            # Check connector health
            connector_healthy = await self.connector.health_check()
            if not connector_healthy:
                return False

            # Check if we can orchestrate a simple scan
            # (This would be a dry run with no actual files)
            test_result = await self.orchestrate_sacred_scan([])
            return test_result.trinity_score >= 0.0

        except Exception as e:
            print(f"  [Sacred-Orchestrator] 🚨 Health check failed: {e}")
            return False
