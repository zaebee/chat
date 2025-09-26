"""
Sacred AGRO Connector (C): Protocol Translation Layer

This module implements the Connector primitive from the ATCG architecture,
providing seamless translation between function-based and class-based
AGRO transformations during the architectural transition.

Part of bee.Jules' Sacred ATCG transformation surgery.
"""

import asyncio
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime

# Sacred imports
from .events import SacredViolation, TransformationResult
from .transformations import (
    AgroCheckTransformation,
    ConsoleLogCheck,
    FunctionLengthCheck,
    AnyTypeCheck,
    PythonMagicNumbersCheck,
    JavaScriptMagicNumbersCheck,
)

# Sacred imports for Hive integration
from hive.config.agro_config import HIVE_INTEGRATION, PHI_RECIPROCAL, QUALITY
from hive.primitives.agro_event_connector import (
    AgroEventConnector as HiveAgroEventConnector,
)  # Import the unified connector


class AgroConnector:
    """
    Sacred Connector (C) - Protocol Translation Layer

    Bridges between legacy function-based checks and new ATCG transformation classes.
    Provides backward compatibility while enabling gradual migration to pure ATCG.
    """

    def __init__(
        self, agro_event_connector: Optional[HiveAgroEventConnector] = None
    ):  # Take AgroEventConnector
        self.agro_event_connector = agro_event_connector
        self.event_bus = (
            agro_event_connector.event_bus if agro_event_connector else None
        )  # Keep event_bus for backward compatibility
        self.transformation_registry: Dict[str, AgroCheckTransformation] = {}
        self.legacy_function_registry: Dict[str, Callable] = {}

        # Sacred metrics tracking
        self.execution_count = 0
        self.total_execution_time = 0.0
        self.blessing_accumulated = 0.0
        self.created_at = datetime.now()

        # Initialize transformation instances
        self._initialize_transformations()

    def _initialize_transformations(self):
        """Initialize all available ATCG transformation instances."""
        self.transformation_registry = {
            "console_log_check": ConsoleLogCheck(),
            "function_length_check": FunctionLengthCheck(),
            "any_type_check": AnyTypeCheck(),
            "python_magic_numbers_check": PythonMagicNumbersCheck(),
            "javascript_magic_numbers_check": JavaScriptMagicNumbersCheck(),
        }

    def register_legacy_function(self, name: str, function: Callable) -> bool:
        """Register a legacy function-based check for backward compatibility."""
        try:
            self.legacy_function_registry[name] = function
            return True
        except Exception as e:
            print(
                f"  [Sacred-Connector] ⚠️ Failed to register legacy function {name}: {e}"
            )
            return False

    async def execute_transformation(
        self, transformation_name: str, file_path: str
    ) -> TransformationResult:
        """
        Execute a specific transformation with sacred metrics tracking.

        This method provides the core translation protocol between old and new architectures.
        """
        start_time = datetime.now()

        try:
            # Try ATCG transformation first
            if transformation_name in self.transformation_registry:
                transformation = self.transformation_registry[transformation_name]
                violations = await transformation.execute(file_path)

                execution_time = (datetime.now() - start_time).total_seconds()
                blessing_level = self._calculate_blessing_level(violations)

                result = TransformationResult(
                    transformation_name=transformation.name,
                    violations=violations,
                    success=True,
                    execution_time=execution_time,
                    blessing_level=blessing_level,
                    sacred_context=f"ATCG Transformation: {transformation.name}",
                )

                # Update sacred metrics
                self.execution_count += 1
                self.total_execution_time += execution_time
                self.blessing_accumulated += blessing_level

                # Emit Pollen Protocol event
                if violations and self.agro_event_connector:
                    await self.agro_event_connector.publish_transformation_executed(
                        transformation_name=transformation.name,
                        file_path=file_path,
                        violations_count=len(violations),
                        blessing_level=blessing_level,
                    )

                return result

            # Fallback to legacy function (during transition period)
            elif transformation_name in self.legacy_function_registry:
                legacy_func = self.legacy_function_registry[transformation_name]

                # Convert legacy function result to new format
                success, violations = legacy_func(file_path)
                execution_time = (datetime.now() - start_time).total_seconds()
                blessing_level = self._calculate_blessing_level(violations)

                return TransformationResult(
                    transformation_name=f"Legacy_{transformation_name}",
                    violations=violations,
                    success=success,
                    execution_time=execution_time,
                    blessing_level=blessing_level,
                    sacred_context="Legacy Function (Transitioning)",
                )

            else:
                # Transformation not found
                execution_time = (datetime.now() - start_time).total_seconds()
                return TransformationResult(
                    transformation_name=f"Unknown_{transformation_name}",
                    violations=[],
                    success=False,
                    execution_time=execution_time,
                    blessing_level=0.0,
                    sacred_context="Transformation not found",
                )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            print(
                f"  [Sacred-Connector] 💥 Transformation failed: {transformation_name} - {e}"
            )

            return TransformationResult(
                transformation_name=f"Failed_{transformation_name}",
                violations=[],
                success=False,
                execution_time=execution_time,
                blessing_level=0.0,
                sacred_context=f"Execution failed: {str(e)}",
            )

    def _calculate_blessing_level(self, violations: List[SacredViolation]) -> float:
        """Calculate blessing level based on violations found."""
        if not violations:
            return 1.0  # Perfect blessing

        # Calculate average blessing level across violations
        avg_blessing = sum(v.blessing_level for v in violations) / len(violations)

        # Apply sacred phi-based scaling
        if HIVE_INTEGRATION:
            return max(0.0, avg_blessing * QUALITY.excellent)
        else:
            return max(0.0, avg_blessing * PHI_RECIPROCAL)  # φ⁻¹ scaling

    async def execute_batch_transformations(
        self, transformation_names: List[str], file_path: str
    ) -> List[TransformationResult]:
        """Execute multiple transformations concurrently with sacred coordination."""
        tasks = [
            self.execute_transformation(name, file_path)
            for name in transformation_names
        ]

        # Execute all transformations concurrently (Sacred G - Genesis coordination)
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and convert to results
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Create error result for failed transformation
                valid_results.append(
                    TransformationResult(
                        transformation_name=f"Exception_{transformation_names[i]}",
                        violations=[],
                        success=False,
                        execution_time=0.0,
                        blessing_level=0.0,
                        sacred_context=f"Async execution failed: {str(result)}",
                    )
                )
            else:
                valid_results.append(result)

        return valid_results

    def get_status(self) -> Dict[str, Any]:
        """Sacred observability: Return connector status and metrics."""
        avg_execution_time = (
            self.total_execution_time / self.execution_count
            if self.execution_count > 0
            else 0.0
        )
        avg_blessing = (
            self.blessing_accumulated / self.execution_count
            if self.execution_count > 0
            else 0.0
        )

        return {
            "component": "AgroConnector",
            "type": "C",  # ATCG Connector
            "architecture": "ATCG_Bridge",
            "transformations_registered": len(self.transformation_registry),
            "legacy_functions_registered": len(self.legacy_function_registry),
            "executions": self.execution_count,
            "avg_execution_time": round(avg_execution_time, 4),
            "avg_blessing_level": round(avg_blessing, 3),
            "hive_integration": HIVE_INTEGRATION,
            "event_bus_active": self.event_bus is not None,
            "created_at": self.created_at.isoformat(),
            "sacred_wisdom": "🌉 Bridge between worlds, harmony in transition",
            "transformation_types": list(self.transformation_registry.keys()),
            "legacy_types": list(self.legacy_function_registry.keys()),
        }

    async def health_check(self) -> bool:
        """Sacred health check: Verify connector is functioning properly."""
        try:
            # Check if we have at least one transformation registered
            if not self.transformation_registry:
                return False

            # Test a simple transformation execution (dry run)
            test_result = await self.execute_transformation(
                "console_log_check", "/dev/null"
            )

            # Health is good if we can execute without major exceptions
            return (
                test_result.success
                or "not found" not in test_result.sacred_context.lower()
            )

        except Exception as e:
            print(f"  [Sacred-Connector] 🚨 Health check failed: {e}")
            return False
