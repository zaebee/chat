"""
Pollen Protocol: Event System for Hive Communication

This module implements the Pollen Protocol from the Hive Constitution,
which standardizes inter-system communication for AI-human collaboration.

The Pollen Protocol requires:
- Unique event ID
- Clear past-tense event type
- Version number
- Timestamp
- Aggregate ID
- Specific event payload
"""

import uuid
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Awaitable
from datetime import datetime
from enum import Enum

from .linguistic_validator import LinguisticValidator, ValidationResult


class EventVersion(str, Enum):
    """Supported event protocol versions."""

    V1_0 = "1.0"
    V1_1 = "1.1"  # Future version with enhanced metadata


@dataclass
class PollenEvent:
    """
    A standardized event following the Pollen Protocol.

    All inter-system communication should use this format to ensure
    compatibility and observability across the entire Hive ecosystem.
    """

    # Required fields per Pollen Protocol
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""  # Past-tense verb describing what happened
    version: str = EventVersion.V1_0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    aggregate_id: str = "default"
    payload: Dict[str, Any] = field(default_factory=dict)

    # Optional metadata for enhanced observability
    source_component: str = ""
    correlation_id: str = ""
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate the event structure using comprehensive linguistic analysis."""
        if not self.event_type:
            raise ValueError("event_type is required and must be a past-tense verb")

        # Use advanced linguistic validation
        validator = LinguisticValidator()
        result = validator.validate_past_tense(self.event_type)

        if not result.is_valid:
            error_msg = f"Invalid event_type '{self.event_type}': {result.reason}"
            if result.suggestions:
                error_msg += f". Suggestions: {', '.join(result.suggestions)}"

            # For development/testing, show warning. In production, might want to raise error
            if result.confidence == 0.0:  # Completely invalid
                print(f"WARNING: {error_msg}")
            else:
                raise ValueError(error_msg)
        elif result.confidence < 0.8:
            # Low confidence - show warning but allow
            print(f"LOW CONFIDENCE: event_type '{self.event_type}' detected as {result.detected_tense} "
                  f"(confidence: {result.confidence:.2f})")

        # Additional style validation
        style_result = validator.validate_event_name_style(self.event_type)
        if not style_result.is_valid and style_result.confidence < 0.7:
            print(f"STYLE WARNING: {style_result.reason}")
            if style_result.suggestions:
                print(f"  Suggestions: {', '.join(style_result.suggestions)}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "version": self.version,
            "timestamp": self.timestamp,
            "aggregate_id": self.aggregate_id,
            "payload": self.payload,
            "source_component": self.source_component,
            "correlation_id": self.correlation_id,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollenEvent":
        """Create PollenEvent from dictionary."""
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data["event_type"],
            version=data.get("version", EventVersion.V1_0),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            aggregate_id=data.get("aggregate_id", "default"),
            payload=data.get("payload", {}),
            source_component=data.get("source_component", ""),
            correlation_id=data.get("correlation_id", ""),
            tags=data.get("tags", []),
        )

    def add_tag(self, tag: str):
        """Add a tag to this event."""
        if tag not in self.tags:
            self.tags.append(tag)

    def set_correlation(self, correlation_id: str):
        """Set correlation ID for event tracing."""
        self.correlation_id = correlation_id

    def is_valid(self) -> bool:
        """Check if event follows Pollen Protocol requirements."""
        required_fields = [
            self.event_id,
            self.event_type,
            self.version,
            self.timestamp,
            self.aggregate_id,
        ]
        return all(field for field in required_fields)


class EventSubscription:
    """Represents a subscription to events matching certain criteria."""

    def __init__(
        self,
        event_types: List[str] = None,
        aggregate_ids: List[str] = None,
        tags: List[str] = None,
        callback: Callable[[PollenEvent], Awaitable[None]] = None,
    ):
        self.event_types = event_types or []
        self.aggregate_ids = aggregate_ids or []
        self.tags = tags or []
        self.callback = callback
        self.subscription_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.message_count = 0

    def matches(self, event: PollenEvent) -> bool:
        """Check if this subscription matches the given event."""
        # Match event types (empty list means match all)
        if self.event_types and event.event_type not in self.event_types:
            return False

        # Match aggregate IDs (empty list means match all)
        if self.aggregate_ids and event.aggregate_id not in self.aggregate_ids:
            return False

        # Match tags (empty list means match all)
        if self.tags and not any(tag in event.tags for tag in self.tags):
            return False

        return True

    async def notify(self, event: PollenEvent):
        """Notify this subscription of a matching event."""
        if self.callback and self.matches(event):
            try:
                await self.callback(event)
                self.message_count += 1
            except Exception as e:
                print(f"Error in subscription callback: {e}")


class HiveEventBus:
    """
    Central event bus implementing the Pollen Protocol.

    This is the nervous system of the Hive, enabling all components
    to communicate through standardized events.
    """

    def __init__(self):
        self.subscriptions: List[EventSubscription] = []
        self.event_history: List[PollenEvent] = []
        self.max_history_size = 1000  # Limit memory usage
        self.total_events_processed = 0
        self.processing_errors = 0

    async def publish(self, event: PollenEvent) -> bool:
        """
        Publish an event to all matching subscribers.

        Returns True if event was successfully published.
        """
        try:
            if not event.is_valid():
                raise ValueError(f"Invalid event: {event}")

            # Add to history
            self.event_history.append(event)
            if len(self.event_history) > self.max_history_size:
                self.event_history.pop(0)  # Remove oldest event

            # Notify all matching subscriptions
            notification_tasks = []
            for subscription in self.subscriptions:
                if subscription.matches(event):
                    notification_tasks.append(subscription.notify(event))

            # Execute all notifications concurrently
            if notification_tasks:
                await asyncio.gather(*notification_tasks, return_exceptions=True)

            self.total_events_processed += 1
            return True

        except Exception as e:
            self.processing_errors += 1
            print(f"Error publishing event: {e}")
            return False

    def subscribe(self, subscription: EventSubscription) -> str:
        """
        Add a new subscription to the event bus.

        Returns the subscription ID for later unsubscription.
        """
        self.subscriptions.append(subscription)
        return subscription.subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription by ID."""
        for i, subscription in enumerate(self.subscriptions):
            if subscription.subscription_id == subscription_id:
                del self.subscriptions[i]
                return True
        return False

    def get_events_by_type(
        self, event_type: str, limit: int = 100
    ) -> List[PollenEvent]:
        """Get recent events of a specific type."""
        matching_events = [
            event for event in self.event_history if event.event_type == event_type
        ]
        return matching_events[-limit:]

    def get_events_by_aggregate(
        self, aggregate_id: str, limit: int = 100
    ) -> List[PollenEvent]:
        """Get recent events for a specific aggregate."""
        matching_events = [
            event for event in self.event_history if event.aggregate_id == aggregate_id
        ]
        return matching_events[-limit:]

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        return {
            "component": "HiveEventBus",
            "type": "EventBus",
            "subscriptions_count": len(self.subscriptions),
            "history_size": len(self.event_history),
            "total_events_processed": self.total_events_processed,
            "processing_errors": self.processing_errors,
            "error_rate": self.processing_errors / max(1, self.total_events_processed),
            "recent_event_types": list(
                set(event.event_type for event in self.event_history[-50:])
            )
            if self.event_history
            else [],
            "timestamp": datetime.now().isoformat(),
            "health": "active"
            if self.processing_errors / max(1, self.total_events_processed) < 0.05
            else "degraded",
        }

    async def health_check(self) -> bool:
        """Check if event bus is healthy."""
        # Event bus is healthy if error rate is low
        error_rate = self.processing_errors / max(1, self.total_events_processed)
        return error_rate < 0.05

    # Convenience methods for common event types

    async def publish_user_event(
        self, action: str, user_id: str, user_data: Dict[str, Any] = None
    ):
        """Publish a user-related event."""
        event = PollenEvent(
            event_type=f"user_{action}",
            aggregate_id=f"user:{user_id}",
            payload=user_data or {},
            source_component="user_management",
            tags=["user", action],
        )
        return await self.publish(event)

    async def publish_message_event(
        self, action: str, message_id: str, message_data: Dict[str, Any] = None
    ):
        """Publish a message-related event."""
        event = PollenEvent(
            event_type=f"message_{action}",
            aggregate_id=f"message:{message_id}",
            payload=message_data or {},
            source_component="chat_system",
            tags=["message", action],
        )
        return await self.publish(event)

    async def publish_system_event(
        self, action: str, system_data: Dict[str, Any] = None
    ):
        """Publish a system-level event."""
        event = PollenEvent(
            event_type=f"system_{action}",
            aggregate_id="system",
            payload=system_data or {},
            source_component="hive_core",
            tags=["system", action],
        )
        return await self.publish(event)

    async def publish_teammate_event(
        self, action: str, teammate_id: str, teammate_data: Dict[str, Any] = None
    ):
        """Publish an AI teammate-related event."""
        event = PollenEvent(
            event_type=f"teammate_{action}",
            aggregate_id=f"teammate:{teammate_id}",
            payload=teammate_data or {},
            source_component="teammate_management",
            tags=["teammate", "ai", action],
        )
        return await self.publish(event)
