"""
ATCG Primitives: The Building Blocks of the Hive

This module implements the four fundamental primitives from the Beekeeper's Grimoire:
- A (Aggregate): Structural organization and state management
- T (Transformation): Processing and enzymatic functions
- C (Connector): Communication, sensing, and translation
- G (Genesis Event): Generative actions and broadcasting

These primitives form the DNA of the Living Application.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable, Awaitable
from datetime import datetime
import uuid

from .config.golden_thresholds import ATCG, QUALITY


@dataclass
class HiveComponent(ABC):
    """Base class for all Hive components following the Legibility principle."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return structured status for observability."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Perform health check and return status."""
        pass


class Aggregate(HiveComponent):
    """
    A (Aggregate): Structural organization and state management.

    Aggregates maintain consistency boundaries and encapsulate business logic.
    They are the structural "proteins" that maintain the shape and integrity
    of the system.
    """

    def __init__(self, name: str, invariants: Optional[List[str]] = None):
        super().__init__(name=name)
        self.invariants = invariants or []
        self.state: Dict[str, Any] = {}
        self.version = ATCG.initial_version
        self.event_history: List[Dict[str, Any]] = []

    def apply_event(self, event: Dict[str, Any]) -> bool:
        """
        Apply an event to this aggregate, maintaining invariants.

        Returns True if event was successfully applied.
        """
        # Validate invariants before applying
        if not self._validate_invariants(event):
            return False

        # Apply the event
        self.state.update(event.get("data", {}))
        self.version += ATCG.version_increment
        self.event_history.append(
            {**event, "applied_at": datetime.now().isoformat(), "version": self.version}
        )

        # Keep event history within sacred limits
        if len(self.event_history) > ATCG.max_history_retention:  # Fibonacci 377
            self.event_history = self.event_history[-ATCG.max_history_retention :]

        return True

    def _validate_invariants(self, event: Dict[str, Any]) -> bool:
        """Validate that applying this event won't violate invariants."""
        # Simplified invariant checking
        # In a real system, this would be more sophisticated
        for invariant in self.invariants:
            if invariant == "non_empty_name" and not event.get("data", {}).get("name"):
                return False
            if (
                invariant == "positive_value"
                and event.get("data", {}).get("value", 0) < 0
            ):
                return False

        return True

    def get_current_state(self) -> Dict[str, Any]:
        """Get the current state of the aggregate."""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "state": self.state,
            "last_modified": self.event_history[-1]["applied_at"]
            if self.event_history
            else self.created_at.isoformat(),
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "component": f"Aggregate:{self.name}",
            "type": "A",
            "id": self.id,
            "version": self.version,
            "invariants": self.invariants,
            "state_size": len(self.state),
            "event_count": len(self.event_history),
            "last_event": self.event_history[-1]["applied_at"]
            if self.event_history
            else None,
            "timestamp": datetime.now().isoformat(),
            "health": "active",
        }

    async def health_check(self) -> bool:
        """Check if aggregate is healthy (all invariants satisfied)."""
        # In a real system, this would validate current state against all invariants
        return len(self.invariants) == 0 or all(
            invariant in ["non_empty_name", "positive_value"]
            for invariant in self.invariants
        )


class Transformation(HiveComponent):
    """
    T (Transformation): Processing and enzymatic functions.

    Transformations are stateless processors that convert inputs to outputs.
    They are the "enzymes" that catalyze changes in the system.
    """

    def __init__(
        self,
        name: str,
        processor_func: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]],
    ):
        super().__init__(name=name)
        self.processor_func = processor_func
        self.execution_count = 0
        self.total_execution_time = 0.0
        self.last_execution: Optional[datetime] = None

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the transformation on input data.

        Transformations must be idempotent and side-effect free.
        """
        start_time = datetime.now()

        try:
            result = await self.processor_func(input_data)

            # Update execution metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.execution_count += 1
            self.total_execution_time += execution_time
            self.last_execution = datetime.now()

            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "timestamp": self.last_execution.isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat(),
            }

    def get_average_execution_time(self) -> float:
        """Get average execution time for this transformation."""
        if self.execution_count == 0:
            return 0.0
        return self.total_execution_time / self.execution_count

    def get_status(self) -> Dict[str, Any]:
        return {
            "component": f"Transformation:{self.name}",
            "type": "T",
            "id": self.id,
            "execution_count": self.execution_count,
            "avg_execution_time": self.get_average_execution_time(),
            "last_execution": self.last_execution.isoformat()
            if self.last_execution
            else None,
            "timestamp": datetime.now().isoformat(),
            "health": "active",
        }

    async def health_check(self) -> bool:
        """Check if transformation is healthy (can execute successfully)."""
        try:
            # Simple health check with empty input
            result = await self.execute({})
            return result.get("success", False) or "error" not in result
        except Exception:
            return False


class Connector(HiveComponent):
    """
    C (Connector): Communication, sensing, and translation.

    Connectors handle protocol translation, data format conversion,
    and communication between different parts of the system.
    They are the "nervous system" that enables coordination.
    """

    def __init__(self, name: str, input_protocol: str, output_protocol: str):
        super().__init__(name=name)
        self.input_protocol = input_protocol
        self.output_protocol = output_protocol
        self.message_count = 0
        self.translation_errors = 0
        self.last_message: Optional[datetime] = None

    async def translate(
        self, message: Dict[str, Any], source_protocol: str, target_protocol: str
    ) -> Dict[str, Any]:
        """
        Translate a message from one protocol to another.

        This is where protocol-specific translation logic would be implemented.
        """
        try:
            # Simplified translation logic
            # In a real system, this would handle complex protocol conversions

            if source_protocol == "websocket" and target_protocol == "pollen":
                # Convert WebSocket message to Pollen Protocol
                return {
                    "event_id": str(uuid.uuid4()),
                    "event_type": message.get("type", "unknown_event"),
                    "version": "1.0",
                    "timestamp": datetime.now().isoformat(),
                    "aggregate_id": message.get("aggregate_id", "default"),
                    "payload": message.get("data", {}),
                }

            elif source_protocol == "pollen" and target_protocol == "websocket":
                # Convert Pollen Protocol to WebSocket message
                return {
                    "type": message.get("event_type", "message"),
                    "data": message.get("payload", {}),
                    "timestamp": message.get("timestamp"),
                }

            else:
                # Default pass-through
                return message

        except Exception as e:
            self.translation_errors += 1
            raise Exception(f"Translation failed: {str(e)}")

    async def send_message(
        self, message: Dict[str, Any], target_protocol: Optional[str] = None
    ) -> bool:
        """
        Send a message through this connector, translating if necessary.
        """
        try:
            target_protocol = target_protocol or self.output_protocol

            if self.input_protocol != target_protocol:
                message = await self.translate(
                    message, self.input_protocol, target_protocol
                )

            self.message_count += 1
            self.last_message = datetime.now()

            # In a real implementation, this would actually send the message
            return True

        except Exception:
            return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "component": f"Connector:{self.name}",
            "type": "C",
            "id": self.id,
            "input_protocol": self.input_protocol,
            "output_protocol": self.output_protocol,
            "message_count": self.message_count,
            "translation_errors": self.translation_errors,
            "error_rate": self.translation_errors / max(1, self.message_count),
            "last_message": self.last_message.isoformat()
            if self.last_message
            else None,
            "timestamp": datetime.now().isoformat(),
            "health": "active"
            if self.translation_errors / max(1, self.message_count) < QUALITY.excellent
            else "degraded",
        }

    async def health_check(self) -> bool:
        """Check if connector is healthy (low error rate)."""
        error_rate = self.translation_errors / max(1, self.message_count)
        return error_rate < QUALITY.excellent  # Sacred φ⁻⁴ ≈ 0.146 error rate


class GenesisEvent(HiveComponent):
    """
    G (Genesis Event): Generative actions and broadcasting.

    Genesis Events are the "DNA replication" mechanism that creates new
    instances, broadcasts information, and triggers system-wide changes.
    They are the generative force that enables growth and reproduction.
    """

    def __init__(
        self,
        name: str,
        event_type: str,
        broadcast_func: Optional[Callable[[Dict[str, Any]], Awaitable[bool]]] = None,
    ):
        super().__init__(name=name)
        self.event_type = event_type
        self.broadcast_func = broadcast_func
        self.generation_count = 0
        self.broadcast_count = 0
        self.last_generation: Optional[datetime] = None

    async def generate(
        self, template_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a new event based on template data.

        This creates new instances or triggers new processes.
        """
        template_data = template_data or {}

        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": self.event_type,
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "generator_id": self.id,
            "generation_sequence": self.generation_count + 1,
            "payload": template_data,
        }

        self.generation_count += 1
        self.last_generation = datetime.now()

        return event

    async def broadcast(self, event: Dict[str, Any]) -> bool:
        """
        Broadcast an event to all interested parties.

        This is the mechanism for system-wide communication.
        """
        try:
            if self.broadcast_func is not None:
                success = await self.broadcast_func(event)
                if success:
                    self.broadcast_count += 1
                return success
            else:
                # Default behavior: just log the broadcast
                self.broadcast_count += 1
                return True

        except Exception:
            return False

    async def replicate(
        self, target_environment: str, template_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new instance of something in a target environment.

        This is the "reproduction" mechanism for creating new specialized forms.
        """
        replication_event = await self.generate(
            {
                "action": "replicate",
                "target_environment": target_environment,
                "template": template_data or {},
                "parent_id": self.id,
            }
        )

        # Broadcast the replication event
        await self.broadcast(replication_event)

        return replication_event

    def get_status(self) -> Dict[str, Any]:
        return {
            "component": f"GenesisEvent:{self.name}",
            "type": "G",
            "id": self.id,
            "event_type": self.event_type,
            "generation_count": self.generation_count,
            "broadcast_count": self.broadcast_count,
            "last_generation": self.last_generation.isoformat()
            if self.last_generation
            else None,
            "timestamp": datetime.now().isoformat(),
            "health": "active",
        }

    async def health_check(self) -> bool:
        """Check if genesis event generator is healthy."""
        # Genesis events are healthy if they can generate new events
        try:
            test_event = await self.generate({"test": True})
            return "event_id" in test_event
        except Exception:
            return False
