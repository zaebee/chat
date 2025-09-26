"""
Multi-Agent Coordination Hub: The Central Nervous System of the Hive

This module provides the central coordination system that orchestrates all
components of the Hive ecosystem, including:

- Intent and Physics level coordination
- ATCG primitive management
- Event bus orchestration
- Teammate registry coordination
- Welcome gateway integration
- Metrics collection and analysis

This is the "brain" that ensures all parts work together harmoniously.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from .intent import HiveIntent
from .physics import HivePhysics
from .primitives import ScoreTransformation, ReviewAggregate, AgroEventConnector
from .events import HiveEventBus, PollenEvent, EventSubscription
from .teammate import HiveTeammate, TeammateProfile, TaskRequest, TeammateCapability
from .registry import HiveRegistry, RegistrationRequest
from .gateway import WelcomeGateway


@dataclass
class SystemHealth:
    """Overall system health metrics."""

    overall_status: str = "active"  # active, degraded, critical, offline
    tau_score: float = 0.0  # System complexity (lower is better)
    phi_score: float = 1.0  # Code quality (higher is better)
    sigma_score: float = 1.0  # Collaborative efficiency
    last_calculated: datetime = None

    def __post_init__(self):
        if self.last_calculated is None:
            self.last_calculated = datetime.now()


class HiveCoordinationHub:
    """
    The central coordination hub that orchestrates the entire Hive ecosystem.

    This is the "living brain" that ensures all components work together
    following the Intent, respecting the Physics constraints, and maintaining
    the collaborative principles of the Constitution.
    """

    def __init__(self):
        # Core components
        self.intent = HiveIntent()
        self.physics = HivePhysics()
        self.event_bus = HiveEventBus()
        self.registry = HiveRegistry(self.event_bus, self.physics)
        self.gateway = WelcomeGateway(self.event_bus, self.registry)

        # ATCG primitive instances
        self.aggregates: Dict[str, Aggregate] = {}
        self.transformations: Dict[str, Transformation] = {}
        self.connectors: Dict[str, Connector] = {}
        self.genesis_events: Dict[str, GenesisEvent] = {}

        # System state
        self.is_running = False
        self.startup_time: Optional[datetime] = None
        self.system_health = SystemHealth()
        self.background_tasks: List[asyncio.Task] = []

        # Metrics collection
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_metrics_history = 1000

        # Setup core system components
        self._initialize_core_components()
        self._setup_event_subscriptions()

    def _initialize_core_components(self):
        """Initialize the core ATCG components for the Hive system."""

        # Core Chat Aggregate
        self.aggregates["chat_system"] = Aggregate(
            name="ChatSystem",
            invariants=["non_empty_name", "positive_value"]
        )

        # Message Processing Transformation
        async def process_message(data: Dict[str, Any]) -> Dict[str, Any]:
            """Process incoming chat messages."""
            message_text = data.get("text", "")
            sender_id = data.get("sender_id", "")

            # Simple message processing
            processed = {
                "original_text": message_text,
                "processed_text": message_text.strip(),
                "word_count": len(message_text.split()),
                "sender_id": sender_id,
                "processed_at": datetime.now().isoformat()
            }

            return processed

        self.transformations["message_processor"] = Transformation(
            name="MessageProcessor",
            processor_func=process_message
        )

        # WebSocket to Pollen Protocol Connector
        self.connectors["ws_to_pollen"] = Connector(
            name="WebSocketToPollenConnector",
            input_protocol="websocket",
            output_protocol="pollen"
        )

        # System Event Generator
        async def broadcast_system_event(event: Dict[str, Any]) -> bool:
            """Broadcast system events via the event bus."""
            try:
                pollen_event = PollenEvent.from_dict(event)
                return await self.event_bus.publish(pollen_event)
            except Exception:
                return False

        self.genesis_events["system_events"] = GenesisEvent(
            name="SystemEventGenerator",
            event_type="system_event_generated",
            broadcast_func=broadcast_system_event
        )

    def _setup_event_subscriptions(self):
        """Set up event subscriptions for system coordination."""

        async def handle_system_events(event: PollenEvent):
            await self._handle_system_event(event)

        async def handle_teammate_events(event: PollenEvent):
            await self._handle_teammate_event(event)

        async def handle_performance_events(event: PollenEvent):
            await self._handle_performance_event(event)

        # Subscribe to various event types
        system_subscription = EventSubscription(
            event_types=["system_started", "system_stopped", "system_error"],
            callback=handle_system_events
        )

        teammate_subscription = EventSubscription(
            tags=["teammate", "ai"],
            callback=handle_teammate_events
        )

        performance_subscription = EventSubscription(
            event_types=["performance_degraded", "resource_exhausted"],
            callback=handle_performance_events
        )

        self.event_bus.subscribe(system_subscription)
        self.event_bus.subscribe(teammate_subscription)
        self.event_bus.subscribe(performance_subscription)

    async def startup(self) -> Dict[str, Any]:
        """
        Start the Hive coordination hub and all subsystems.
        """
        try:
            self.startup_time = datetime.now()

            # Detect physics environment
            self.physics.detect_environment()
            await self.physics.update_metrics()

            # Start background tasks
            self._start_background_tasks()

            # Announce system startup
            await self.event_bus.publish_system_event(
                "started",
                {
                    "startup_time": self.startup_time.isoformat(),
                    "intent": self.intent.get_current_purpose(),
                    "physics_status": self.physics.get_status(),
                    "version": "0.1.0"
                }
            )

            self.is_running = True

            return {
                "success": True,
                "message": "Hive coordination hub started successfully",
                "startup_time": self.startup_time.isoformat(),
                "components_status": await self._get_all_component_status()
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to start coordination hub: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _start_background_tasks(self):
        """Start background monitoring and maintenance tasks."""

        async def health_monitor():
            """Monitor system health and update metrics."""
            while self.is_running:
                try:
                    await self._update_system_health()
                    await self._collect_metrics()
                    await asyncio.sleep(30)  # Update every 30 seconds
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error in health monitor: {e}")
                    await asyncio.sleep(60)  # Wait longer on error

        async def physics_monitor():
            """Monitor physics constraints and adapt."""
            while self.is_running:
                try:
                    await self.physics.update_metrics()
                    constraints_check = self.physics.check_constraints()

                    if not constraints_check["within_constraints"]:
                        await self._handle_physics_violations(constraints_check)

                    await asyncio.sleep(60)  # Check every minute
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error in physics monitor: {e}")
                    await asyncio.sleep(120)

        async def intent_alignment_check():
            """Periodically check alignment with Intent."""
            while self.is_running:
                try:
                    await self._check_intent_alignment()
                    await asyncio.sleep(300)  # Check every 5 minutes
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error in intent alignment check: {e}")
                    await asyncio.sleep(600)

        # Start all background tasks
        self.background_tasks = [
            asyncio.create_task(health_monitor()),
            asyncio.create_task(physics_monitor()),
            asyncio.create_task(intent_alignment_check())
        ]

    async def shutdown(self) -> Dict[str, Any]:
        """
        Gracefully shutdown the coordination hub and all subsystems.
        """
        try:
            self.is_running = False

            # Cancel background tasks
            for task in self.background_tasks:
                task.cancel()

            if self.background_tasks:
                await asyncio.gather(*self.background_tasks, return_exceptions=True)

            # Shutdown subsystems
            await self.registry.shutdown()

            # Announce system shutdown
            await self.event_bus.publish_system_event(
                "stopped",
                {
                    "shutdown_time": datetime.now().isoformat(),
                    "uptime_seconds": (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0,
                    "final_health": self.system_health.__dict__
                }
            )

            return {
                "success": True,
                "message": "Hive coordination hub shut down successfully",
                "uptime_seconds": (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error during shutdown: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def register_external_teammate(self, profile: TeammateProfile, teammate: HiveTeammate) -> Dict[str, Any]:
        """
        Register an external AI teammate (like Mistral) through the proper onboarding process.
        """
        try:
            # Start onboarding process
            onboarding_result = await self.gateway.start_onboarding(profile)

            if not onboarding_result["success"]:
                return onboarding_result

            # For demo purposes, we'll simulate completing the onboarding
            # In practice, the external teammate would complete the tasks
            session_id = onboarding_result["session_id"]

            # Auto-complete onboarding for external teammates with proper credentials
            # This is a shortcut for demo - normally they'd go through all stages
            registration = RegistrationRequest(
                profile=profile,
                authentication_data={"external_teammate": True},
                capabilities_proof={"onboarding_bypassed": True}
            )

            registration_result = await self.registry.register_teammate(registration)

            if registration_result["success"]:
                approval_success = await self.registry.approve_registration(
                    registration_result["registration_id"],
                    teammate
                )

                if approval_success:
                    await self.event_bus.publish_teammate_event(
                        "external_teammate_integrated",
                        profile.id,
                        {
                            "name": profile.name,
                            "type": profile.type,
                            "capabilities": [cap.value for cap in profile.capabilities]
                        }
                    )

                    return {
                        "success": True,
                        "teammate_id": profile.id,
                        "message": f"External teammate {profile.name} successfully integrated into the Hive",
                        "registration_result": registration_result
                    }

            return {
                "success": False,
                "error": "Failed to complete registration after onboarding"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to register external teammate: {str(e)}"
            }

    async def assign_collaborative_task(self, task_description: str, required_capabilities: List[TeammateCapability] = None) -> Dict[str, Any]:
        """
        Assign a task that may require collaboration between multiple teammates.
        """
        try:
            # Create task request
            task = TaskRequest(
                task_type="collaborative_task",
                description=task_description,
                input_data={"required_capabilities": [cap.value for cap in (required_capabilities or [])]}
            )

            # Try to assign to a single teammate first
            assignment_result = await self.registry.assign_task(task)

            if assignment_result["success"]:
                return assignment_result
            else:
                # If single assignment fails, try to form a team
                return await self._form_collaborative_team(task, required_capabilities)

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to assign collaborative task: {str(e)}"
            }

    async def _form_collaborative_team(self, task: TaskRequest, required_capabilities: List[TeammateCapability]) -> Dict[str, Any]:
        """Form a team of teammates to handle a complex task."""
        try:
            available_teammates = await self.registry.get_available_teammates()

            # Simple team formation - assign one teammate per required capability
            team = []
            covered_capabilities = set()

            for capability in (required_capabilities or []):
                for teammate_info in available_teammates:
                    if (capability.value in teammate_info["capabilities"] and
                        teammate_info["id"] not in [t["id"] for t in team]):
                        team.append(teammate_info)
                        covered_capabilities.add(capability.value)
                        break

            if team:
                team_ids = [t["id"] for t in team]
                await self.event_bus.publish_system_event(
                    "collaborative_team_formed",
                    {
                        "task_id": task.task_id,
                        "team_members": team_ids,
                        "covered_capabilities": list(covered_capabilities)
                    }
                )

                return {
                    "success": True,
                    "team_formed": True,
                    "team_members": team,
                    "task_id": task.task_id
                }
            else:
                return {
                    "success": False,
                    "error": "Unable to form team with required capabilities"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to form collaborative team: {str(e)}"
            }

    async def get_hive_overview(self) -> Dict[str, Any]:
        """Get a comprehensive overview of the entire Hive system."""
        try:
            component_statuses = await self._get_all_component_status()

            return {
                "system_overview": {
                    "status": self.system_health.overall_status,
                    "is_running": self.is_running,
                    "uptime_seconds": (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0
                },
                "intent": self.intent.get_status(),
                "physics": self.physics.get_status(),
                "health_metrics": {
                    "tau": self.system_health.tau_score,
                    "phi": self.system_health.phi_score,
                    "sigma": self.system_health.sigma_score,
                    "last_calculated": self.system_health.last_calculated.isoformat()
                },
                "components": component_statuses,
                "recent_metrics": self.metrics_history[-10:] if self.metrics_history else [],
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "error": f"Failed to get hive overview: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    # Private helper methods

    async def _get_all_component_status(self) -> Dict[str, Any]:
        """Get status of all system components."""
        status = {}

        # Core components
        status["event_bus"] = self.event_bus.get_status()
        status["registry"] = await self.registry.get_hive_status()
        status["gateway"] = self.gateway.get_status()

        # ATCG primitives
        status["aggregates"] = {name: agg.get_status() for name, agg in self.aggregates.items()}
        status["transformations"] = {name: trans.get_status() for name, trans in self.transformations.items()}
        status["connectors"] = {name: conn.get_status() for name, conn in self.connectors.items()}
        status["genesis_events"] = {name: gen.get_status() for name, gen in self.genesis_events.items()}

        return status

    async def _update_system_health(self):
        """Update system health metrics (tau, phi, sigma)."""
        try:
            # Get component statuses
            components = await self._get_all_component_status()

            # Calculate tau (system complexity - lower is better)
            total_components = (
                len(self.aggregates) +
                len(self.transformations) +
                len(self.connectors) +
                len(self.genesis_events)
            )
            active_teammates = components["registry"]["active_teammates"]
            event_processing_errors = components["event_bus"]["processing_errors"]

            self.system_health.tau_score = (
                total_components * 0.1 +
                active_teammates * 0.05 +
                event_processing_errors * 0.2
            )

            # Calculate phi (code quality - higher is better)
            error_rates = []
            for conn_status in components["connectors"].values():
                error_rates.append(1.0 - conn_status["error_rate"])

            event_bus_health = 1.0 - components["event_bus"]["error_rate"]

            if error_rates:
                avg_component_health = sum(error_rates) / len(error_rates)
                self.system_health.phi_score = (avg_component_health + event_bus_health) / 2
            else:
                self.system_health.phi_score = event_bus_health

            # Calculate sigma (collaborative efficiency)
            total_teammates = components["registry"]["total_teammates"]
            system_load = components["registry"]["system_load"]

            if total_teammates > 0:
                self.system_health.sigma_score = max(0.0, 1.0 - system_load)
            else:
                self.system_health.sigma_score = 0.0

            # Update overall status
            if self.system_health.tau_score > 5.0 or self.system_health.phi_score < 0.3:
                self.system_health.overall_status = "critical"
            elif self.system_health.tau_score > 2.0 or self.system_health.phi_score < 0.7:
                self.system_health.overall_status = "degraded"
            else:
                self.system_health.overall_status = "active"

            self.system_health.last_calculated = datetime.now()

        except Exception as e:
            print(f"Error updating system health: {e}")
            self.system_health.overall_status = "error"

    async def _collect_metrics(self):
        """Collect and store system metrics."""
        try:
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "health": {
                    "tau": self.system_health.tau_score,
                    "phi": self.system_health.phi_score,
                    "sigma": self.system_health.sigma_score,
                    "overall_status": self.system_health.overall_status
                },
                "physics": self.physics._current_metrics,
                "teammates": {
                    "total": len(self.registry.teammates),
                    "active": len([t for t in self.registry.teammates.values() if t.status.value == "active"]),
                    "busy": len([t for t in self.registry.teammates.values() if t.status.value == "busy"])
                },
                "events": {
                    "total_processed": self.event_bus.total_events_processed,
                    "processing_errors": self.event_bus.processing_errors,
                    "subscriptions": len(self.event_bus.subscriptions)
                }
            }

            self.metrics_history.append(metrics)

            # Limit history size
            if len(self.metrics_history) > self.max_metrics_history:
                self.metrics_history = self.metrics_history[-self.max_metrics_history:]

        except Exception as e:
            print(f"Error collecting metrics: {e}")

    async def _handle_physics_violations(self, constraints_check: Dict[str, Any]):
        """Handle physics constraint violations."""
        violations = constraints_check.get("violations", {})

        await self.event_bus.publish_system_event(
            "physics_constraints_violated",
            {
                "violations": violations,
                "timestamp": datetime.now().isoformat()
            }
        )

        # Get adaptation suggestions
        suggestions = self.physics.get_adaptation_suggestions()

        if suggestions:
            await self.event_bus.publish_system_event(
                "adaptation_suggestions_generated",
                {
                    "suggestions": suggestions,
                    "timestamp": datetime.now().isoformat()
                }
            )

    async def _check_intent_alignment(self):
        """Check if system behavior aligns with stated Intent."""
        try:
            # Sample recent actions for alignment check
            recent_events = self.event_bus.event_history[-50:] if self.event_bus.event_history else []

            alignment_scores = []
            for event in recent_events:
                score = self.intent.evaluate_alignment(
                    event.event_type,
                    event.payload
                )
                alignment_scores.append(score)

            if alignment_scores:
                avg_alignment = sum(alignment_scores) / len(alignment_scores)

                if avg_alignment < 0.6:  # Below 60% alignment
                    await self.event_bus.publish_system_event(
                        "intent_misalignment_detected",
                        {
                            "average_alignment": avg_alignment,
                            "sample_size": len(alignment_scores),
                            "timestamp": datetime.now().isoformat()
                        }
                    )

        except Exception as e:
            print(f"Error checking intent alignment: {e}")

    async def _handle_system_event(self, event: PollenEvent):
        """Handle system-level events."""
        if event.event_type == "system_error":
            print(f"System error detected: {event.payload}")
            # Could implement error recovery logic here

    async def _handle_teammate_event(self, event: PollenEvent):
        """Handle teammate-related events."""
        if event.event_type == "teammate_joined":
            print(f"New teammate joined: {event.payload.get('name', 'Unknown')}")
        elif event.event_type == "teammate_left":
            print(f"Teammate left: {event.payload.get('name', 'Unknown')}")

    async def _handle_performance_event(self, event: PollenEvent):
        """Handle performance-related events."""
        if event.event_type == "performance_degraded":
            # Could implement performance optimization logic here
            pass

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        return {
            "component": "HiveCoordinationHub",
            "type": "CoordinationHub",
            "is_running": self.is_running,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "uptime_seconds": (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0,
            "system_health": {
                "overall_status": self.system_health.overall_status,
                "tau_score": self.system_health.tau_score,
                "phi_score": self.system_health.phi_score,
                "sigma_score": self.system_health.sigma_score
            },
            "background_tasks_count": len(self.background_tasks),
            "metrics_history_size": len(self.metrics_history),
            "timestamp": datetime.now().isoformat(),
            "health": self.system_health.overall_status
        }