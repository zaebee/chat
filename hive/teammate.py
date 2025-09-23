"""
HiveTeammate: Standardized Interface for AI Teammates

This module defines the interface that all AI teammates must implement
to participate in the Hive ecosystem as first-class citizens.

Following the Constitution's principle of Human-AI Symbiosis, this ensures
that AI agents can collaborate effectively with humans and each other.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import uuid

from .events import PollenEvent, HiveEventBus
from .status_mixin import StatusMixin


class TeammateCapability(str, Enum):
    """Standard capabilities that teammates can possess."""

    CODE_ANALYSIS = "code_analysis"
    CODE_GENERATION = "code_generation"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEBUGGING = "debugging"
    REFACTORING = "refactoring"
    ARCHITECTURE_REVIEW = "architecture_review"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    UI_UX_DESIGN = "ui_ux_design"
    DATA_ANALYSIS = "data_analysis"
    CONVERSATION = "conversation"
    LEARNING_SUPPORT = "learning_support"
    PROJECT_MANAGEMENT = "project_management"


class TeammateStatus(str, Enum):
    """Possible status states for teammates."""

    INITIALIZING = "initializing"
    ACTIVE = "active"
    BUSY = "busy"
    IDLE = "idle"
    OFFLINE = "offline"
    ERROR = "error"


class DevelopmentStage(str, Enum):
    """Metamorphosis stages for development lifecycle."""

    EGG = "egg"  # Initialization
    LARVA = "larva"  # Development
    PUPA = "pupa"  # Build/containerization
    ADULT = "adult"  # Deployment


@dataclass
class TeammateProfile:
    """Profile information for a Hive teammate."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: str = ""  # e.g., "claude", "mistral", "gpt-4", "human"
    capabilities: List[TeammateCapability] = field(default_factory=list)
    preferred_tasks: List[str] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)
    communication_protocols: List[str] = field(default_factory=list)
    max_concurrent_tasks: int = 1
    response_time_estimate: float = 5.0  # Average response time in seconds
    reliability_score: float = 1.0  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capabilities": [cap.value for cap in self.capabilities],
            "preferred_tasks": self.preferred_tasks,
            "specializations": self.specializations,
            "communication_protocols": self.communication_protocols,
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "response_time_estimate": self.response_time_estimate,
            "reliability_score": self.reliability_score,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class TaskRequest:
    """A request for a teammate to perform a task."""

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str = ""
    description: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1-10, higher is more urgent
    estimated_duration: float = 0.0  # Estimated duration in seconds
    deadline: Optional[datetime] = None
    requester_id: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TaskResult:
    """Result of a completed task."""

    task_id: str = ""
    success: bool = False
    result_data: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""
    execution_time: float = 0.0
    confidence_score: float = 1.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=datetime.now)


class HiveTeammate(StatusMixin, ABC):
    """
    Abstract base class for all Hive teammates.

    This interface ensures that all AI agents can participate as
    first-class citizens in the Hive ecosystem.
    """

    def __init__(self, profile: TeammateProfile, event_bus: HiveEventBus):
        self.profile = profile
        self.event_bus = event_bus
        self.status = TeammateStatus.INITIALIZING
        self.current_tasks: Dict[str, TaskRequest] = {}
        self.completed_tasks: List[str] = []
        self.last_activity: datetime = datetime.now()
        self.metrics: Dict[str, Any] = {
            "tasks_completed": 0,
            "average_execution_time": 0.0,
            "success_rate": 1.0,
            "errors_count": 0,
        }

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the teammate.

        This method is called when the teammate joins the Hive.
        Should return True if initialization was successful.
        """
        pass

    @abstractmethod
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """
        Execute a requested task.

        This is the core method that implements the teammate's functionality.
        """
        pass

    @abstractmethod
    async def get_capabilities(self) -> List[TeammateCapability]:
        """
        Return current capabilities of this teammate.

        Capabilities may change over time as the teammate learns and evolves.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Perform a health check.

        Should return True if the teammate is functioning properly.
        """
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """
        Gracefully shutdown the teammate.

        Should complete any ongoing tasks and clean up resources.
        """
        pass

    # Standard implementation methods

    async def announce_presence(self):
        """Announce this teammate's presence to the Hive."""
        await self.event_bus.publish_teammate_event(
            "joined",
            self.profile.id,
            {
                "name": self.profile.name,
                "type": self.profile.type,
                "capabilities": [cap.value for cap in self.profile.capabilities],
            },
        )

    async def announce_departure(self):
        """Announce this teammate's departure from the Hive."""
        await self.event_bus.publish_teammate_event(
            "left",
            self.profile.id,
            {"name": self.profile.name, "final_metrics": self.metrics},
        )

    async def start_task(self, task: TaskRequest) -> bool:
        """Start executing a task (internal coordination)."""
        if len(self.current_tasks) >= self.profile.max_concurrent_tasks:
            return False

        if self.status not in [TeammateStatus.ACTIVE, TeammateStatus.IDLE]:
            return False

        self.current_tasks[task.task_id] = task
        self.status = (
            TeammateStatus.BUSY if len(self.current_tasks) == 1 else TeammateStatus.BUSY
        )
        self.last_activity = datetime.now()

        # Announce task start
        await self.event_bus.publish_teammate_event(
            "task_started",
            self.profile.id,
            {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "description": task.description,
            },
        )

        return True

    async def complete_task(self, task_id: str, result: TaskResult) -> bool:
        """Complete a task and update metrics."""
        if task_id not in self.current_tasks:
            return False

        # Remove from current tasks
        task = self.current_tasks.pop(task_id)
        self.completed_tasks.append(task_id)

        # Update metrics
        self.metrics["tasks_completed"] += 1
        if result.success:
            current_avg = self.metrics["average_execution_time"]
            task_count = self.metrics["tasks_completed"]
            self.metrics["average_execution_time"] = (
                current_avg * (task_count - 1) + result.execution_time
            ) / task_count
        else:
            self.metrics["errors_count"] += 1

        self.metrics["success_rate"] = (
            self.metrics["tasks_completed"] - self.metrics["errors_count"]
        ) / max(1, self.metrics["tasks_completed"])

        # Update status
        self.status = (
            TeammateStatus.IDLE if not self.current_tasks else TeammateStatus.BUSY
        )
        self.last_activity = datetime.now()

        # Announce task completion
        await self.event_bus.publish_teammate_event(
            "task_completed",
            self.profile.id,
            {
                "task_id": task_id,
                "success": result.success,
                "execution_time": result.execution_time,
                "confidence_score": result.confidence_score,
            },
        )

        return True

    def can_handle_task(self, task_type: str) -> bool:
        """Check if this teammate can handle a specific task type."""
        # Check against capabilities
        task_type_lower = task_type.lower()
        for capability in self.profile.capabilities:
            if capability.value in task_type_lower:
                return True

        # Check against preferred tasks
        for preferred in self.profile.preferred_tasks:
            if preferred.lower() in task_type_lower:
                return True

        return False

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        # Override base status fields to use profile data
        base_status = {
            "id": self.profile.id,
            "name": self.profile.name,
            "created_at": self.profile.created_at.isoformat(),
            "timestamp": datetime.now().isoformat(),
            "metadata": self.profile.metadata,
        }

        specific_status = {
            "component": f"HiveTeammate:{self.profile.name}",
            "type": "Teammate",
            "teammate_type": self.profile.type,
            "status": self.status.value,
            "capabilities": [cap.value for cap in self.profile.capabilities],
            "current_tasks": len(self.current_tasks),
            "max_concurrent_tasks": self.profile.max_concurrent_tasks,
            "metrics": self.metrics,
            "last_activity": self.last_activity.isoformat(),
            "reliability_score": self.profile.reliability_score,
            "health": "active" if self.status != TeammateStatus.ERROR else "error",
        }

        base_status.update(specific_status)
        return base_status

    async def subscribe_to_events(self, event_types: List[str]):
        """Subscribe to specific event types from the event bus."""
        from .events import EventSubscription

        async def handle_event(event: PollenEvent):
            await self.on_event_received(event)

        subscription = EventSubscription(event_types=event_types, callback=handle_event)

        self.event_bus.subscribe(subscription)

    async def on_event_received(self, event: PollenEvent):
        """
        Handle an event received from the event bus.

        Override this method to implement event-driven behavior.
        """
        # Default implementation: log the event
        print(f"Teammate {self.profile.name} received event: {event.event_type}")

    def estimate_task_duration(self, task: TaskRequest) -> float:
        """Estimate how long a task will take to complete."""
        # Basic estimation based on task type and historical data
        base_time = self.profile.response_time_estimate

        # Adjust based on task complexity (simplified)
        complexity_multiplier = 1.0
        if "complex" in task.description.lower():
            complexity_multiplier = 2.0
        elif "simple" in task.description.lower():
            complexity_multiplier = 0.5

        # Use historical average if available
        if self.metrics["average_execution_time"] > 0:
            return self.metrics["average_execution_time"] * complexity_multiplier
        else:
            return base_time * complexity_multiplier
