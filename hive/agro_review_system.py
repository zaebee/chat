"""
AGRO Bee-to-Peer Review System
Aggressive Collaborative Evaluation Protocols

This module implements the AGRO (Aggressive Collaborative Evaluation) system
for intensive bee-to-peer code review and quality assessment.

Sacred Justification: "Iron sharpens iron, and one man sharpens another."
- Proverbs 27:17 (ESV)
"""

import uuid
import ast
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from .events import PollenEvent, HiveEventBus, EventSubscription
from .primitives import ScoreTransformation, ReviewAggregate, AgroEventConnector
from .primitives.review_aggregate import (
    AgroReviewType,
    AgroReviewResult,
    AgroSeverity,
    BeeToPeerSession,
)


# AGRO Scoring Constants - Eliminates magic numbers
class AgroScoringConstants:
    """Named constants for AGRO scoring calculations"""

    # PAIN Score calculation
    PAIN_VIOLATION_PENALTY = 10  # Points deducted per violation
    PAIN_BASE_SCORE = 100  # Starting score before penalties

    # AGRO Score penalties by severity
    CRITICAL_VIOLATION_PENALTY = 20  # Points deducted per critical violation
    HIGH_VIOLATION_PENALTY = 10  # Points deducted per high severity violation
    MEDIUM_VIOLATION_PENALTY = 5  # Points deducted per medium severity violation

    # Score boundaries
    MIN_SCORE = 0  # Minimum possible score
    MAX_SCORE = 100  # Maximum possible score

    # Severity thresholds
    DIVINE_THRESHOLD = 90  # Score needed for divine blessing
    BLESSED_THRESHOLD = 80  # Score needed for blessed status
    ACCEPTABLE_THRESHOLD = 60  # Score needed for acceptable status
    CONCERNING_THRESHOLD = 40  # Score needed for concerning status
    # Below 40 is critical

    # Code quality thresholds
    MAX_FUNCTION_LINES = 50  # Maximum lines per function
    MAX_NESTING_DEPTH = 4  # Maximum nesting depth

    # Circuit breaker settings
    AST_PARSING_TIMEOUT = 30.0  # Seconds before AST parsing times out
    CIRCUIT_BREAKER_THRESHOLD = 5  # Failures before circuit opens
    CIRCUIT_BREAKER_RECOVERY_TIME = 60.0  # Seconds before attempting recovery

    # Memory management settings
    MAX_REVIEW_HISTORY = 1000  # Maximum reviews to keep in memory
    CLEANUP_THRESHOLD = 0.9  # Cleanup when 90% of max is reached
    CLEANUP_BATCH_SIZE = 100  # Number of old reviews to remove during cleanup

    # Physics Level resource constraints
    MAX_CONCURRENT_REVIEWS = 10  # Maximum simultaneous reviews
    MAX_CODE_SIZE_BYTES = 1024 * 1024  # 1MB maximum code size
    MAX_MEMORY_USAGE_MB = 512  # Maximum memory usage for AGRO system
    CPU_THROTTLE_THRESHOLD = 0.8  # CPU usage threshold for throttling


class AstParsingCircuitBreaker:
    """Circuit breaker for AST parsing operations to prevent timeouts and cascading failures"""

    def __init__(self):
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def is_open(self) -> bool:
        """Check if circuit breaker is open (blocking requests)"""
        if self.state == "OPEN":
            # Check if recovery time has passed
            current_time = datetime.now().timestamp()
            if (
                current_time - self.last_failure_time
                > AgroScoringConstants.CIRCUIT_BREAKER_RECOVERY_TIME
            ):
                self.state = "HALF_OPEN"
                return False
            return True
        return False

    def record_success(self):
        """Record successful operation"""
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        """Record failed operation"""
        self.failure_count += 1
        self.last_failure_time = datetime.now().timestamp()

        if self.failure_count >= AgroScoringConstants.CIRCUIT_BREAKER_THRESHOLD:
            self.state = "OPEN"

    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
        }


def timeout_ast_parsing(
    code_context: str, timeout_seconds: float = AgroScoringConstants.AST_PARSING_TIMEOUT
):
    """
    Parse AST with timeout protection

    Args:
        code_context: Code to parse
        timeout_seconds: Maximum time to allow for parsing

    Returns:
        AST tree or raises TimeoutError
    """
    import threading

    result = [None]
    exception = [None]

    def parse_with_timeout():
        try:
            result[0] = ast.parse(code_context)
        except Exception as e:
            exception[0] = e

    # Start parsing in a separate thread
    thread = threading.Thread(target=parse_with_timeout)
    thread.daemon = True
    thread.start()

    # Wait for completion or timeout
    thread.join(timeout_seconds)

    if thread.is_alive():
        # Timeout occurred
        raise TimeoutError(f"AST parsing timed out after {timeout_seconds} seconds")

    if exception[0]:
        raise exception[0]

    return result[0]


class PhysicsLevelResourceMonitor:
    """
    Physics Level resource constraint monitoring for AGRO system

    Implements resource-aware computing following Hive Constitution principles
    """

    def __init__(self):
        self.active_reviews = 0
        self.peak_memory_usage = 0
        self.total_bytes_processed = 0
        self.throttle_events = 0

    def check_resource_constraints(self, code_size: int) -> Dict[str, Any]:
        """
        Check if current resource usage allows for new review

        Returns:
            Dict with constraint check results and recommendations
        """
        constraints = {
            "can_proceed": True,
            "violations": [],
            "recommendations": [],
            "resource_status": {},
        }

        # Check concurrent review limit
        if self.active_reviews >= AgroScoringConstants.MAX_CONCURRENT_REVIEWS:
            constraints["can_proceed"] = False
            constraints["violations"].append(
                {
                    "type": "concurrent_limit_exceeded",
                    "current": self.active_reviews,
                    "limit": AgroScoringConstants.MAX_CONCURRENT_REVIEWS,
                    "severity": "high",
                }
            )
            constraints["recommendations"].append("Wait for active reviews to complete")

        # Check code size limit
        if code_size > AgroScoringConstants.MAX_CODE_SIZE_BYTES:
            constraints["can_proceed"] = False
            constraints["violations"].append(
                {
                    "type": "code_size_exceeded",
                    "current": code_size,
                    "limit": AgroScoringConstants.MAX_CODE_SIZE_BYTES,
                    "severity": "medium",
                }
            )
            constraints["recommendations"].append(
                "Break down large files into smaller modules"
            )

        # Check memory usage (if psutil is available)
        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024

            if memory_mb > AgroScoringConstants.MAX_MEMORY_USAGE_MB:
                constraints["can_proceed"] = False
                constraints["violations"].append(
                    {
                        "type": "memory_limit_exceeded",
                        "current": memory_mb,
                        "limit": AgroScoringConstants.MAX_MEMORY_USAGE_MB,
                        "severity": "high",
                    }
                )
                constraints["recommendations"].append(
                    "Reduce review history or restart system"
                )

            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > AgroScoringConstants.CPU_THROTTLE_THRESHOLD * 100:
                constraints["violations"].append(
                    {
                        "type": "cpu_throttle_recommended",
                        "current": cpu_percent,
                        "threshold": AgroScoringConstants.CPU_THROTTLE_THRESHOLD * 100,
                        "severity": "medium",
                    }
                )
                constraints["recommendations"].append("Consider throttling review rate")
                self.throttle_events += 1

            constraints["resource_status"] = {
                "memory_mb": memory_mb,
                "cpu_percent": cpu_percent,
                "active_reviews": self.active_reviews,
            }

        except ImportError:
            # psutil not available - basic constraints only
            constraints["resource_status"] = {
                "memory_monitoring": "unavailable",
                "cpu_monitoring": "unavailable",
                "active_reviews": self.active_reviews,
            }

        return constraints

    def start_review(self, code_size: int):
        """Record start of new review"""
        self.active_reviews += 1
        self.total_bytes_processed += code_size

    def end_review(self):
        """Record end of review"""
        self.active_reviews = max(0, self.active_reviews - 1)

    def get_physics_metrics(self) -> Dict[str, Any]:
        """Get Physics Level metrics"""
        return {
            "active_reviews": self.active_reviews,
            "peak_memory_usage": self.peak_memory_usage,
            "total_bytes_processed": self.total_bytes_processed,
            "throttle_events": self.throttle_events,
            "resource_efficiency": self._calculate_efficiency(),
        }

    def _calculate_efficiency(self) -> float:
        """Calculate resource efficiency score"""
        if self.total_bytes_processed == 0:
            return 1.0

        # Simple efficiency metric based on throttle events
        efficiency = 1.0 - (
            self.throttle_events / max(1, self.active_reviews + self.throttle_events)
        )
        return max(0.0, min(1.0, efficiency))


class AgroCodeAnalyzer(ast.NodeVisitor):
    """AST-based aggressive code analysis"""

    def __init__(self):
        self.violations = []
        self.metrics = {
            "console_logs": 0,
            "any_types": 0,
            "todo_comments": 0,
            "magic_numbers": 0,
            "long_functions": 0,
            "deep_nesting": 0,
        }
        self.current_function_lines = 0
        self.nesting_depth = 0
        self.max_nesting = 0

    def visit_Call(self, node):
        """Detect console.log and other problematic calls"""
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "console"
            and node.func.attr == "log"
        ):
            self.violations.append(
                {
                    "type": "console_log",
                    "line": node.lineno,
                    "severity": "high",
                    "message": "Console.log detected - remove for production",
                }
            )
            self.metrics["console_logs"] += 1

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Analyze function complexity"""
        self.current_function_lines = len(node.body)

        if self.current_function_lines > AgroScoringConstants.MAX_FUNCTION_LINES:
            self.violations.append(
                {
                    "type": "long_function",
                    "line": node.lineno,
                    "severity": "medium",
                    "message": f"Function {node.name} is {self.current_function_lines} lines (max {AgroScoringConstants.MAX_FUNCTION_LINES})",
                }
            )
            self.metrics["long_functions"] += 1

        # Check for nesting depth
        old_depth = self.nesting_depth
        self.nesting_depth = 0
        self.generic_visit(node)

        if self.max_nesting > AgroScoringConstants.MAX_NESTING_DEPTH:
            self.violations.append(
                {
                    "type": "deep_nesting",
                    "line": node.lineno,
                    "severity": "medium",
                    "message": f"Function {node.name} has nesting depth {self.max_nesting} (max {AgroScoringConstants.MAX_NESTING_DEPTH})",
                }
            )
            self.metrics["deep_nesting"] += 1

        self.nesting_depth = old_depth

    def visit_If(self, node):
        """Track nesting depth"""
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_For(self, node):
        """Track nesting depth"""
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_While(self, node):
        """Track nesting depth"""
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        self.generic_visit(node)
        self.nesting_depth -= 1


class AgroReviewSystem:
    """
    AGRO Bee-to-Peer Review System

    Implements aggressive collaborative evaluation protocols using ATCG primitives:
    - A (Aggregate): ReviewAggregate for state management
    - T (Transformation): ScoreTransformation for pure scoring functions
    - C (Connector): AgroEventConnector for event coordination
    - G (Genesis): Event-driven review initiation
    """

    def __init__(self, event_bus: HiveEventBus):
        self.event_bus = event_bus

        # ATCG Primitives
        self.aggregate = ReviewAggregate(max_history_size=1000)
        self.connector = AgroEventConnector(event_bus)
        # ScoreTransformation is stateless, used directly

        # Legacy components (to be phased out)
        self.ast_circuit_breaker = AstParsingCircuitBreaker()
        self.physics_monitor = PhysicsLevelResourceMonitor()

        # Register for AGRO events
        self.event_bus.subscribe(
            EventSubscription(
                event_types=["agro_review_requested", "peer_collaboration_requested"],
                callback=self._handle_agro_request,
            )
        )

    async def initiate_agro_review(
        self,
        code_context: str,
        review_type: AgroReviewType = AgroReviewType.PAIN_ANALYSIS,
        peer_reviewers: List[str] = None,
    ) -> AgroReviewResult:
        """Initiate aggressive collaborative review using ATCG primitives"""

        review_id = f"agro_{uuid.uuid4().hex[:8]}"
        peer_reviewers = peer_reviewers or ["bee.jules", "bee.sage", "bee.chronicler"]

        # C (Connector): Publish review initiation event
        await self.connector.publish_review_initiated(
            review_id=review_id,
            review_type=review_type.value,
            target=f"code_context_{len(code_context)}_bytes",
            initiator="agro_review_system",
        )

        try:
            # Physics Level resource constraint checking (legacy)
            code_size = len(code_context.encode("utf-8"))
            resource_constraints = self.physics_monitor.check_resource_constraints(
                code_size
            )

            if not resource_constraints["can_proceed"]:
                # Create failure result and publish failure event
                await self.connector.publish_review_failed(
                    review_id=review_id,
                    error_message="Resource constraints exceeded",
                    error_type="physics_constraint",
                )

                return AgroReviewResult.create(
                    review_type=review_type,
                    agro_score=0,
                    pain_score=0,
                    severity="critical",
                    violations=resource_constraints["violations"],
                    recommendations=resource_constraints["recommendations"],
                    divine_blessing=False,
                    peer_reviewers=peer_reviewers,
                    sacred_insights=[
                        "Resource constraints protect the sacred hive from overload",
                        "Physics Level wisdom guides sustainable computing practices",
                    ],
                )

            # Record review start for resource tracking
            self.physics_monitor.start_review(code_size)

            # Perform PAIN analysis (legacy method)
            pain_result = await self._perform_pain_analysis(code_context)

            # T (Transformation): Use pure transformation functions
            agro_score = ScoreTransformation.calculate_agro_score(pain_result)
            severity = ScoreTransformation.determine_severity(agro_score)
            divine_blessing = ScoreTransformation.calculate_divine_blessing_eligibility(
                agro_score, pain_result.get("violations", [])
            )

            # Generate recommendations (legacy method)
            recommendations = await self._generate_agro_recommendations(
                pain_result, severity
            )

            # Extract sacred insights (legacy method)
            sacred_insights = await self._extract_sacred_insights(
                pain_result, review_type
            )

            # Create review result
            review_result = AgroReviewResult(
                review_id=review_id,
                review_type=review_type,
                agro_score=agro_score,
                pain_score=pain_result.get("pain_score", 0),
                severity=severity.value,
                violations=pain_result.get("violations", []),
                recommendations=recommendations,
                divine_blessing=divine_blessing,
                peer_reviewers=peer_reviewers,
                timestamp=datetime.now().isoformat(),
                sacred_insights=sacred_insights,
            )

            # A (Aggregate): Store result in aggregate
            self.aggregate.add_review_result(review_result)

            # C (Connector): Publish completion event
            await self.connector.publish_review_completed(review_result)

            # Record review completion for resource tracking
            self.physics_monitor.end_review()

            return review_result

        except Exception as e:
            # C (Connector): Publish failure event
            await self.connector.publish_review_failed(
                review_id=review_id,
                error_message=str(e),
                error_type="review_execution_error",
            )
            raise

    async def start_bee_to_peer_session(
        self,
        participants: List[str],
        review_target: str,
        session_type: str = "collaborative_review",
    ) -> BeeToPeerSession:
        """Start bee-to-peer collaborative session using ATCG primitives"""

        # A (Aggregate): Start session through aggregate
        session = self.aggregate.start_collaborative_session(
            participants=participants,
            review_target=review_target,
            session_type=session_type,
        )

        # C (Connector): Publish session started event
        await self.connector.publish_session_started(session)

        return session

    # ATCG Primitive Access Methods

    def get_review_history(self, limit: Optional[int] = None) -> List[AgroReviewResult]:
        """Get review history from aggregate"""
        return self.aggregate.get_review_history(limit)

    def get_active_sessions(self) -> List[BeeToPeerSession]:
        """Get active sessions from aggregate"""
        return self.aggregate.get_active_sessions()

    def get_aggregate_metrics(self) -> Dict[str, Any]:
        """Get aggregate metrics"""
        return self.aggregate.get_aggregate_metrics()

    def get_event_statistics(self) -> Dict[str, Any]:
        """Get event connector statistics"""
        return self.connector.get_statistics()

    async def end_collaborative_session(
        self,
        session_id: str,
        collaboration_score: float = 0.0,
        sacred_alignment: float = 0.0,
    ) -> Optional[BeeToPeerSession]:
        """End collaborative session using ATCG primitives"""

        # A (Aggregate): End session through aggregate
        session = self.aggregate.end_collaborative_session(
            session_id=session_id,
            collaboration_score=collaboration_score,
            sacred_alignment=sacred_alignment,
        )

        if session:
            # C (Connector): Publish session ended event
            await self.connector.publish_session_ended(session)

        return session

    async def _perform_pain_analysis(self, code_context: str) -> Dict[str, Any]:
        """Perform PAIN (Production Analysis and Issue Notification) analysis"""

        # Check circuit breaker before attempting AST parsing
        if self.ast_circuit_breaker.is_open():
            return {
                "pain_score": 0,
                "violations": [
                    {
                        "type": "circuit_breaker_open",
                        "line": 0,
                        "severity": "critical",
                        "message": "AST parsing circuit breaker is open - system temporarily unavailable",
                    }
                ],
                "metrics": {},
                "analysis_successful": False,
                "circuit_breaker_status": self.ast_circuit_breaker.get_status(),
            }

        try:
            # Parse code with AST using timeout protection
            tree = timeout_ast_parsing(code_context)

            # Record successful parsing
            self.ast_circuit_breaker.record_success()

            # Run aggressive analysis
            analyzer = AgroCodeAnalyzer()
            analyzer.visit(tree)

            # Calculate PAIN score
            total_violations = sum(analyzer.metrics.values())
            pain_score = max(
                AgroScoringConstants.MIN_SCORE,
                AgroScoringConstants.PAIN_BASE_SCORE
                - (total_violations * AgroScoringConstants.PAIN_VIOLATION_PENALTY),
            )

            return {
                "pain_score": pain_score,
                "violations": analyzer.violations,
                "metrics": analyzer.metrics,
                "analysis_successful": True,
            }

        except TimeoutError as e:
            # Record timeout failure in circuit breaker
            self.ast_circuit_breaker.record_failure()
            return {
                "pain_score": 0,
                "violations": [
                    {
                        "type": "ast_parsing_timeout",
                        "line": 0,
                        "severity": "critical",
                        "message": f"AST parsing timeout: {str(e)}",
                    }
                ],
                "metrics": {},
                "analysis_successful": False,
                "circuit_breaker_status": self.ast_circuit_breaker.get_status(),
            }
        except SyntaxError as e:
            # Syntax errors don't count as circuit breaker failures
            return {
                "pain_score": 0,
                "violations": [
                    {
                        "type": "syntax_error",
                        "line": e.lineno,
                        "severity": "critical",
                        "message": f"Syntax error: {str(e)}",
                    }
                ],
                "metrics": {},
                "analysis_successful": False,
            }
        except Exception as e:
            # Record unexpected failures in circuit breaker
            self.ast_circuit_breaker.record_failure()
            return {
                "pain_score": 0,
                "violations": [
                    {
                        "type": "ast_parsing_error",
                        "line": 0,
                        "severity": "critical",
                        "message": f"AST parsing error: {str(e)}",
                    }
                ],
                "metrics": {},
                "analysis_successful": False,
                "circuit_breaker_status": self.ast_circuit_breaker.get_status(),
            }

    def _calculate_agro_score(self, pain_result: Dict[str, Any]) -> int:
        """Calculate AGRO (Aggressive Collaborative Evaluation) score"""

        if not pain_result.get("analysis_successful", False):
            return 0

        pain_score = pain_result.get("pain_score", 0)
        violations = pain_result.get("violations", [])

        # Base score from PAIN analysis
        agro_score = pain_score

        # Penalty for critical violations
        critical_violations = [v for v in violations if v.get("severity") == "critical"]
        agro_score -= (
            len(critical_violations) * AgroScoringConstants.CRITICAL_VIOLATION_PENALTY
        )

        # Penalty for high severity violations
        high_violations = [v for v in violations if v.get("severity") == "high"]
        agro_score -= len(high_violations) * AgroScoringConstants.HIGH_VIOLATION_PENALTY

        # Penalty for medium severity violations
        medium_violations = [v for v in violations if v.get("severity") == "medium"]
        agro_score -= (
            len(medium_violations) * AgroScoringConstants.MEDIUM_VIOLATION_PENALTY
        )

        return max(
            AgroScoringConstants.MIN_SCORE,
            min(AgroScoringConstants.MAX_SCORE, agro_score),
        )

    def _determine_severity(self, agro_score: int) -> AgroSeverity:
        """Determine severity level based on AGRO score"""

        if agro_score >= AgroScoringConstants.DIVINE_THRESHOLD:
            return AgroSeverity.DIVINE
        elif agro_score >= AgroScoringConstants.BLESSED_THRESHOLD:
            return AgroSeverity.BLESSED
        elif agro_score >= AgroScoringConstants.ACCEPTABLE_THRESHOLD:
            return AgroSeverity.ACCEPTABLE
        elif agro_score >= AgroScoringConstants.CONCERNING_THRESHOLD:
            return AgroSeverity.CONCERNING
        else:
            return AgroSeverity.CRITICAL

    async def _generate_agro_recommendations(
        self, pain_result: Dict[str, Any], severity: AgroSeverity
    ) -> List[str]:
        """Generate AGRO recommendations based on analysis"""

        recommendations = []
        violations = pain_result.get("violations", [])

        # Console.log recommendations
        console_violations = [v for v in violations if v["type"] == "console_log"]
        if console_violations:
            recommendations.append(
                "Remove all console.log statements for production readiness"
            )

        # Function complexity recommendations
        long_functions = [v for v in violations if v["type"] == "long_function"]
        if long_functions:
            recommendations.append(
                "Break down long functions into smaller, focused units"
            )

        # Nesting depth recommendations
        deep_nesting = [v for v in violations if v["type"] == "deep_nesting"]
        if deep_nesting:
            recommendations.append(
                "Reduce nesting depth through early returns and guard clauses"
            )

        # Severity-based recommendations
        if severity == AgroSeverity.CRITICAL:
            recommendations.append(
                "CRITICAL: Immediate refactoring required before deployment"
            )
        elif severity == AgroSeverity.CONCERNING:
            recommendations.append("Address major issues before peer review approval")
        elif severity == AgroSeverity.DIVINE:
            recommendations.append("Excellent code quality - ready for divine blessing")

        return recommendations

    async def _extract_sacred_insights(
        self, pain_result: Dict[str, Any], review_type: AgroReviewType
    ) -> List[str]:
        """Extract sacred insights from AGRO analysis"""

        insights = []

        if pain_result.get("analysis_successful", False):
            insights.append(
                "Sacred code analysis reveals divine patterns in implementation"
            )

            if pain_result.get("pain_score", 0) >= 90:
                insights.append(
                    "Code demonstrates sacred excellence worthy of divine blessing"
                )

            violations = pain_result.get("violations", [])
            if not violations:
                insights.append(
                    "Pure code without violations reflects divine perfection"
                )

        # Review type specific insights
        if review_type == AgroReviewType.PEER_COLLABORATION:
            insights.append(
                "Collaborative review strengthens the sacred bond between teammates"
            )
        elif review_type == AgroReviewType.DIVINE_BLESSING_ASSESSMENT:
            insights.append(
                "Divine blessing assessment reveals spiritual alignment in code"
            )

        return insights

    async def _handle_agro_request(self, event: PollenEvent):
        """Handle AGRO review requests"""

        if event.event_type == "agro_review_requested":
            code_context = event.payload.get("code_context", "")
            review_type = AgroReviewType(
                event.payload.get("review_type", "pain_analysis")
            )
            peer_reviewers = event.payload.get("peer_reviewers", [])

            result = await self.initiate_agro_review(
                code_context, review_type, peer_reviewers
            )

            # Respond with result
            await self.event_bus.publish(
                PollenEvent(
                    event_type="agro_review_response",
                    source_component="agro_review_system",
                    aggregate_id=event.source_component,
                    payload=asdict(result),
                )
            )

    # Memory management is now handled by the ReviewAggregate primitive

    def get_status(self) -> Dict[str, Any]:
        """Get AGRO review system status using ATCG primitives"""

        # A (Aggregate): Get status from aggregate
        aggregate_status = self.aggregate.get_status()
        aggregate_metrics = self.aggregate.get_aggregate_metrics()

        # C (Connector): Get event statistics
        connector_stats = self.connector.get_statistics()

        return {
            "component": "agro_review_system",
            "architecture": "ATCG_primitives",
            "primitives": {
                "aggregate": aggregate_status,
                "connector": connector_stats,
                "transformation": "stateless_functions",
            },
            "capabilities": [
                "pain_analysis",
                "peer_collaboration",
                "aggressive_scrutiny",
                "divine_blessing_assessment",
            ],
            "sacred_metrics": aggregate_metrics,
            "recent_reviews": [
                {
                    "review_id": r.review_id,
                    "agro_score": r.agro_score,
                    "severity": r.severity,
                    "divine_blessing": r.divine_blessing,
                }
                for r in self.aggregate.get_review_history(5)
            ],
            "circuit_breaker": self.ast_circuit_breaker.get_status(),
            "physics_level": self.physics_monitor.get_physics_metrics(),
        }
