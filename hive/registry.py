"""
HiveRegistry: Central Management for AI Teammates

This module provides the registry service that manages all AI teammates
in the Hive ecosystem, handling discovery, authentication, task delegation,
and health monitoring.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import uuid

from .teammate import (
    HiveTeammate,
    TeammateProfile,
    TaskRequest,
    TeammateStatus,
    TeammateCapability,
)
from .events import HiveEventBus, PollenEvent, EventSubscription
from .physics import HivePhysics


@dataclass
class RegistrationRequest:
    """Request to register a new teammate in the Hive."""

    profile: TeammateProfile
    authentication_data: Dict[str, Any]
    capabilities_proof: Dict[str, Any] = None  # Evidence of claimed capabilities
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class TaskAssignment:
    """Assignment of a task to a specific teammate."""

    assignment_id: str
    task: TaskRequest
    assigned_to: str  # teammate_id
    assigned_at: datetime
    expected_completion: datetime
    status: str = "assigned"  # assigned, in_progress, completed, failed


class HiveRegistry:
    """
    Central registry for managing AI teammates in the Hive ecosystem.

    This service handles:
    - Teammate discovery and registration
    - Authentication and capability verification
    - Task delegation and load balancing
    - Health monitoring and failover
    - Performance metrics and optimization
    """

    def __init__(self, event_bus: HiveEventBus, physics: HivePhysics):
        self.event_bus = event_bus
        self.physics = physics
        self.teammates: Dict[str, HiveTeammate] = {}
        self.pending_registrations: Dict[str, RegistrationRequest] = {}
        self.task_assignments: Dict[str, TaskAssignment] = {}
        self.capability_index: Dict[TeammateCapability, List[str]] = {}
        self.load_balancer_metrics: Dict[str, Dict[str, float]] = {}
        self.health_check_interval = 60  # seconds
        self.last_health_check = datetime.now()

        # Subscribe to relevant events
        self._setup_event_subscriptions()

        # Start background tasks
        self._health_check_task = None
        self._start_background_tasks()

    def _setup_event_subscriptions(self):
        """Set up event subscriptions for registry management."""

        async def handle_teammate_events(event: PollenEvent):
            await self._handle_teammate_event(event)

        teammate_subscription = EventSubscription(
            event_types=["teammate_joined", "teammate_left", "teammate_task_completed"],
            callback=handle_teammate_events,
        )

        self.event_bus.subscribe(teammate_subscription)

    def _start_background_tasks(self):
        """Start background tasks for health monitoring."""
        self._health_check_task = asyncio.create_task(self._health_check_loop())

    async def _health_check_loop(self):
        """Background task that periodically checks teammate health."""
        while True:
            try:
                await asyncio.sleep(self.health_check_interval)
                await self._perform_health_checks()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in health check loop: {e}")

    async def register_teammate(
        self, registration: RegistrationRequest
    ) -> Dict[str, Any]:
        """
        Register a new teammate in the Hive.

        Returns registration result with status and teammate_id if successful.
        """
        try:
            # Validate registration request
            validation_result = await self._validate_registration(registration)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["reason"],
                    "timestamp": datetime.now().isoformat(),
                }

            # Check physics constraints
            if not self.physics.can_accept_new_connection():
                return {
                    "success": False,
                    "error": "System at capacity - cannot accept new teammates",
                    "timestamp": datetime.now().isoformat(),
                }

            # Store pending registration
            registration_id = str(uuid.uuid4())
            self.pending_registrations[registration_id] = registration

            # Announce registration event
            await self.event_bus.publish_teammate_event(
                "registration_requested",
                registration.profile.id,
                {
                    "registration_id": registration_id,
                    "name": registration.profile.name,
                    "type": registration.profile.type,
                    "capabilities": [
                        cap.value for cap in registration.profile.capabilities
                    ],
                },
            )

            return {
                "success": True,
                "registration_id": registration_id,
                "teammate_id": registration.profile.id,
                "status": "pending_approval",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Registration failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            }

    async def approve_registration(
        self, registration_id: str, teammate: HiveTeammate
    ) -> bool:
        """
        Approve a pending registration and activate the teammate.
        """
        if registration_id not in self.pending_registrations:
            return False

        try:
            registration = self.pending_registrations.pop(registration_id)

            # Initialize the teammate
            init_success = await teammate.initialize()
            if not init_success:
                return False

            # Add to active teammates
            self.teammates[teammate.profile.id] = teammate
            teammate.status = TeammateStatus.ACTIVE

            # Update capability index
            await self._update_capability_index(teammate)

            # Initialize load balancer metrics
            self.load_balancer_metrics[teammate.profile.id] = {
                "current_load": 0.0,
                "average_response_time": teammate.profile.response_time_estimate,
                "success_rate": 1.0,
                "last_task_completion": datetime.now().timestamp(),
            }

            # Announce successful registration
            await self.event_bus.publish_teammate_event(
                "registration_approved",
                teammate.profile.id,
                {
                    "name": teammate.profile.name,
                    "capabilities": [
                        cap.value for cap in teammate.profile.capabilities
                    ],
                },
            )

            await teammate.announce_presence()

            return True

        except Exception as e:
            print(f"Error approving registration: {e}")
            return False

    async def unregister_teammate(self, teammate_id: str) -> bool:
        """
        Unregister a teammate from the Hive.
        """
        if teammate_id not in self.teammates:
            return False

        try:
            teammate = self.teammates[teammate_id]

            # Graceful shutdown
            await teammate.shutdown()
            await teammate.announce_departure()

            # Remove from active teammates
            del self.teammates[teammate_id]

            # Update capability index
            await self._remove_from_capability_index(teammate)

            # Clean up metrics
            if teammate_id in self.load_balancer_metrics:
                del self.load_balancer_metrics[teammate_id]

            # Clean up assignments
            self._cleanup_assignments(teammate_id)

            await self.event_bus.publish_teammate_event(
                "unregistered", teammate_id, {"reason": "manual_unregistration"}
            )

            return True

        except Exception as e:
            print(f"Error unregistering teammate: {e}")
            return False

    async def assign_task(
        self, task: TaskRequest, preferred_teammate_id: str = None
    ) -> Dict[str, Any]:
        """
        Assign a task to the most suitable teammate.

        If preferred_teammate_id is specified, attempts to assign to that teammate.
        Otherwise, uses intelligent load balancing to select the best teammate.
        """
        try:
            # Find suitable teammate
            if preferred_teammate_id and preferred_teammate_id in self.teammates:
                chosen_teammate = self.teammates[preferred_teammate_id]
                if not chosen_teammate.can_handle_task(task.task_type):
                    return {
                        "success": False,
                        "error": "Preferred teammate cannot handle this task type",
                    }
            else:
                chosen_teammate = await self._select_best_teammate(task)

            if not chosen_teammate:
                return {
                    "success": False,
                    "error": "No available teammates can handle this task",
                }

            # Check if teammate can accept the task
            if not await chosen_teammate.start_task(task):
                return {"success": False, "error": "Teammate is busy or unavailable"}

            # Create assignment record
            assignment = TaskAssignment(
                assignment_id=str(uuid.uuid4()),
                task=task,
                assigned_to=chosen_teammate.profile.id,
                assigned_at=datetime.now(),
                expected_completion=datetime.now()
                + timedelta(seconds=chosen_teammate.estimate_task_duration(task)),
            )

            self.task_assignments[assignment.assignment_id] = assignment

            # Update load balancer metrics
            self._update_load_metrics(chosen_teammate.profile.id, task)

            return {
                "success": True,
                "assignment_id": assignment.assignment_id,
                "assigned_to": chosen_teammate.profile.id,
                "teammate_name": chosen_teammate.profile.name,
                "estimated_completion": assignment.expected_completion.isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": f"Task assignment failed: {str(e)}"}

    async def get_available_teammates(
        self, capability: TeammateCapability = None
    ) -> List[Dict[str, Any]]:
        """
        Get list of available teammates, optionally filtered by capability.
        """
        available = []

        for teammate in self.teammates.values():
            if teammate.status in [TeammateStatus.ACTIVE, TeammateStatus.IDLE]:
                if capability is None or capability in teammate.profile.capabilities:
                    available.append(
                        {
                            "id": teammate.profile.id,
                            "name": teammate.profile.name,
                            "type": teammate.profile.type,
                            "status": teammate.status.value,
                            "capabilities": [
                                cap.value for cap in teammate.profile.capabilities
                            ],
                            "current_tasks": len(teammate.current_tasks),
                            "max_tasks": teammate.profile.max_concurrent_tasks,
                            "availability": 1.0
                            - (
                                len(teammate.current_tasks)
                                / teammate.profile.max_concurrent_tasks
                            ),
                        }
                    )

        return sorted(available, key=lambda x: x["availability"], reverse=True)

    async def get_hive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the entire Hive."""
        total_teammates = len(self.teammates)
        active_teammates = len(
            [t for t in self.teammates.values() if t.status == TeammateStatus.ACTIVE]
        )
        busy_teammates = len(
            [t for t in self.teammates.values() if t.status == TeammateStatus.BUSY]
        )

        capability_distribution = {}
        for capability in TeammateCapability:
            count = len(self.capability_index.get(capability, []))
            if count > 0:
                capability_distribution[capability.value] = count

        return {
            "component": "HiveRegistry",
            "type": "Registry",
            "total_teammates": total_teammates,
            "active_teammates": active_teammates,
            "busy_teammates": busy_teammates,
            "idle_teammates": total_teammates - active_teammates - busy_teammates,
            "capability_distribution": capability_distribution,
            "active_assignments": len(
                [
                    a
                    for a in self.task_assignments.values()
                    if a.status in ["assigned", "in_progress"]
                ]
            ),
            "completed_assignments": len(
                [a for a in self.task_assignments.values() if a.status == "completed"]
            ),
            "system_load": busy_teammates / max(1, total_teammates),
            "physics_status": self.physics.get_status(),
            "last_health_check": self.last_health_check.isoformat(),
            "timestamp": datetime.now().isoformat(),
            "health": "active" if total_teammates > 0 else "no_teammates",
        }

    # Private helper methods

    async def _validate_registration(
        self, registration: RegistrationRequest
    ) -> Dict[str, Any]:
        """Validate a registration request."""
        profile = registration.profile

        # Basic validation
        if not profile.name or not profile.type:
            return {"valid": False, "reason": "Missing required profile fields"}

        if profile.id in self.teammates:
            return {"valid": False, "reason": "Teammate ID already exists"}

        # Capability validation (simplified)
        if not profile.capabilities:
            return {"valid": False, "reason": "No capabilities specified"}

        return {"valid": True}

    async def _update_capability_index(self, teammate: HiveTeammate):
        """Update the capability index with a new teammate."""
        for capability in teammate.profile.capabilities:
            if capability not in self.capability_index:
                self.capability_index[capability] = []
            if teammate.profile.id not in self.capability_index[capability]:
                self.capability_index[capability].append(teammate.profile.id)

    async def _remove_from_capability_index(self, teammate: HiveTeammate):
        """Remove a teammate from the capability index."""
        for capability in teammate.profile.capabilities:
            if capability in self.capability_index:
                if teammate.profile.id in self.capability_index[capability]:
                    self.capability_index[capability].remove(teammate.profile.id)

    async def _select_best_teammate(self, task: TaskRequest) -> Optional[HiveTeammate]:
        """Select the best teammate for a task using intelligent load balancing."""
        candidates = []

        # Find teammates who can handle this task
        for teammate in self.teammates.values():
            if (
                teammate.status in [TeammateStatus.ACTIVE, TeammateStatus.IDLE]
                and teammate.can_handle_task(task.task_type)
                and len(teammate.current_tasks) < teammate.profile.max_concurrent_tasks
            ):
                candidates.append(teammate)

        if not candidates:
            return None

        # Score candidates based on multiple factors
        best_teammate = None
        best_score = -1

        for teammate in candidates:
            metrics = self.load_balancer_metrics.get(teammate.profile.id, {})

            # Calculate composite score
            availability = 1.0 - (
                len(teammate.current_tasks) / teammate.profile.max_concurrent_tasks
            )
            reliability = teammate.profile.reliability_score
            success_rate = metrics.get("success_rate", 1.0)
            load_factor = 1.0 - metrics.get("current_load", 0.0)

            # Weighted score calculation
            score = (
                availability * 0.3
                + reliability * 0.3
                + success_rate * 0.25
                + load_factor * 0.15
            )

            if score > best_score:
                best_score = score
                best_teammate = teammate

        return best_teammate

    def _update_load_metrics(self, teammate_id: str, task: TaskRequest):
        """Update load balancer metrics for a teammate."""
        if teammate_id not in self.load_balancer_metrics:
            self.load_balancer_metrics[teammate_id] = {
                "current_load": 0.0,
                "average_response_time": 5.0,
                "success_rate": 1.0,
                "last_task_completion": datetime.now().timestamp(),
            }

        metrics = self.load_balancer_metrics[teammate_id]
        teammate = self.teammates[teammate_id]

        # Update current load
        metrics["current_load"] = (
            len(teammate.current_tasks) / teammate.profile.max_concurrent_tasks
        )

    def _cleanup_assignments(self, teammate_id: str):
        """Clean up assignments for a removed teammate."""
        to_remove = []
        for assignment_id, assignment in self.task_assignments.items():
            if assignment.assigned_to == teammate_id:
                to_remove.append(assignment_id)

        for assignment_id in to_remove:
            del self.task_assignments[assignment_id]

    async def _perform_health_checks(self):
        """Perform health checks on all teammates."""
        self.last_health_check = datetime.now()

        for teammate_id, teammate in list(self.teammates.items()):
            try:
                is_healthy = await teammate.health_check()
                if not is_healthy:
                    teammate.status = TeammateStatus.ERROR
                    await self.event_bus.publish_teammate_event(
                        "health_check_failed",
                        teammate_id,
                        {"timestamp": datetime.now().isoformat()},
                    )
            except Exception as e:
                teammate.status = TeammateStatus.ERROR
                print(f"Health check failed for teammate {teammate_id}: {e}")

    async def _handle_teammate_event(self, event: PollenEvent):
        """Handle teammate-related events."""
        if event.event_type == "teammate_task_completed":
            # Update metrics based on task completion
            teammate_id = event.aggregate_id.split(":")[-1]
            if teammate_id in self.load_balancer_metrics:
                payload = event.payload
                metrics = self.load_balancer_metrics[teammate_id]

                # Update success rate
                if payload.get("success"):
                    current_rate = metrics["success_rate"]
                    metrics["success_rate"] = min(1.0, current_rate * 0.95 + 0.05)
                else:
                    current_rate = metrics["success_rate"]
                    metrics["success_rate"] = max(0.0, current_rate * 0.95)

                metrics["last_task_completion"] = datetime.now().timestamp()

    async def shutdown(self):
        """Shutdown the registry and all managed teammates."""
        # Cancel background tasks
        if self._health_check_task:
            self._health_check_task.cancel()

        # Shutdown all teammates
        for teammate in self.teammates.values():
            try:
                await teammate.shutdown()
            except Exception as e:
                print(f"Error shutting down teammate: {e}")

        self.teammates.clear()
