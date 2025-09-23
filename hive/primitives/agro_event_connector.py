"""
🐝⚡ AgroEventConnector (C Primitive) ⚡🐝

Connector primitive for AGRO event coordination and communication.
Handles protocol translation and event bus integration for review system.

Sacred Principle: "Connectors translate between protocols and coordinate communication"
"""

from typing import Dict, List, Any, Optional, Callable, Awaitable
from dataclasses import dataclass
from datetime import datetime
import asyncio
import uuid
from enum import Enum

from ..events import PollenEvent, HiveEventBus
from .review_aggregate import AgroReviewResult, BeeToPeerSession


class AgroEventType(str, Enum):
    """Types of AGRO events in the Pollen Protocol"""
    
    # Review lifecycle events (past tense per Pollen Protocol)
    REVIEW_INITIATED = "agro_review_initiated"
    REVIEW_COMPLETED = "agro_review_completed"
    REVIEW_FAILED = "agro_review_failed"
    
    # Collaboration events
    SESSION_STARTED = "peer_session_started"
    SESSION_ENDED = "peer_session_ended"
    PEER_JOINED = "peer_joined_session"
    PEER_LEFT = "peer_left_session"
    
    # Quality events
    DIVINE_BLESSING_GRANTED = "divine_blessing_granted"
    CRITICAL_VIOLATION_DETECTED = "critical_violation_detected"
    IMPROVEMENT_SUGGESTED = "improvement_suggested"
    
    # System events
    AGRO_SYSTEM_READY = "agro_system_ready"
    CIRCUIT_BREAKER_OPENED = "circuit_breaker_opened"
    MEMORY_THRESHOLD_REACHED = "memory_threshold_reached"


@dataclass
class AgroEventPayload:
    """Standardized payload for AGRO events"""
    review_id: Optional[str] = None
    session_id: Optional[str] = None
    agro_score: Optional[int] = None
    pain_score: Optional[int] = None
    severity: Optional[str] = None
    violations_count: Optional[int] = None
    divine_blessing: Optional[bool] = None
    participants: Optional[List[str]] = None
    target: Optional[str] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgroEventConnector:
    """
    🔗 C (Connector) Primitive for AGRO Event Coordination
    
    Translates between AGRO review system and Hive event protocols.
    Coordinates communication and ensures proper event flow.
    """
    
    def __init__(self, event_bus: Optional[HiveEventBus] = None):
        """
        Initialize AGRO event connector
        
        Args:
            event_bus: Hive event bus for system-wide communication
        """
        self.event_bus = event_bus
        self.event_handlers: Dict[AgroEventType, List[Callable]] = {}
        self.event_history: List[PollenEvent] = []
        self.max_history_size = 1000
        
        # Event statistics
        self.events_published = 0
        self.events_handled = 0
        self.failed_events = 0
    
    def register_handler(self, 
                        event_type: AgroEventType, 
                        handler: Callable[[PollenEvent], Awaitable[None]]) -> None:
        """
        Register an event handler for specific AGRO event type
        
        Args:
            event_type: Type of AGRO event to handle
            handler: Async function to handle the event
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
    
    async def publish_review_initiated(self, 
                                     review_id: str,
                                     review_type: str,
                                     target: str,
                                     initiator: str) -> None:
        """Publish event when AGRO review is initiated"""
        payload = AgroEventPayload(
            review_id=review_id,
            target=target,
            message=f"AGRO {review_type} review initiated by {initiator}",
            metadata={
                'review_type': review_type,
                'initiator': initiator
            }
        )
        
        await self._publish_event(AgroEventType.REVIEW_INITIATED, payload)
    
    async def publish_review_completed(self, result: AgroReviewResult) -> None:
        """Publish event when AGRO review is completed"""
        payload = AgroEventPayload(
            review_id=result.review_id,
            agro_score=result.agro_score,
            pain_score=result.pain_score,
            severity=result.severity,
            violations_count=len(result.violations),
            divine_blessing=result.divine_blessing,
            message=f"AGRO review completed with {result.severity} severity",
            metadata={
                'review_type': result.review_type.value,
                'recommendations_count': len(result.recommendations),
                'peer_reviewers': result.peer_reviewers,
                'sacred_insights': result.sacred_insights
            }
        )
        
        await self._publish_event(AgroEventType.REVIEW_COMPLETED, payload)
        
        # Publish additional events based on results
        if result.divine_blessing:
            await self.publish_divine_blessing_granted(result)
        
        critical_violations = [v for v in result.violations 
                             if v.get('severity') == 'critical']
        if critical_violations:
            await self.publish_critical_violations_detected(result, critical_violations)
    
    async def publish_review_failed(self, 
                                  review_id: str,
                                  error_message: str,
                                  error_type: str = "unknown") -> None:
        """Publish event when AGRO review fails"""
        payload = AgroEventPayload(
            review_id=review_id,
            message=f"AGRO review failed: {error_message}",
            metadata={
                'error_type': error_type,
                'error_message': error_message
            }
        )
        
        await self._publish_event(AgroEventType.REVIEW_FAILED, payload)
    
    async def publish_session_started(self, session: BeeToPeerSession) -> None:
        """Publish event when collaborative session starts"""
        payload = AgroEventPayload(
            session_id=session.session_id,
            participants=session.participants,
            target=session.review_target,
            message=f"Peer collaboration session started with {len(session.participants)} participants",
            metadata={
                'session_type': session.session_type,
                'start_time': session.start_time
            }
        )
        
        await self._publish_event(AgroEventType.SESSION_STARTED, payload)
    
    async def publish_session_ended(self, session: BeeToPeerSession) -> None:
        """Publish event when collaborative session ends"""
        payload = AgroEventPayload(
            session_id=session.session_id,
            participants=session.participants,
            message=f"Peer collaboration session ended",
            metadata={
                'session_type': session.session_type,
                'start_time': session.start_time,
                'end_time': session.end_time,
                'collaboration_score': session.collaboration_score,
                'sacred_alignment': session.sacred_alignment
            }
        )
        
        await self._publish_event(AgroEventType.SESSION_ENDED, payload)
    
    async def publish_divine_blessing_granted(self, result: AgroReviewResult) -> None:
        """Publish event when divine blessing is granted"""
        payload = AgroEventPayload(
            review_id=result.review_id,
            agro_score=result.agro_score,
            divine_blessing=True,
            message=f"Divine blessing granted for {result.review_type.value} review",
            metadata={
                'sacred_insights': result.sacred_insights,
                'peer_reviewers': result.peer_reviewers
            }
        )
        
        await self._publish_event(AgroEventType.DIVINE_BLESSING_GRANTED, payload)
    
    async def publish_critical_violations_detected(self, 
                                                 result: AgroReviewResult,
                                                 violations: List[Dict[str, Any]]) -> None:
        """Publish event when critical violations are detected"""
        payload = AgroEventPayload(
            review_id=result.review_id,
            violations_count=len(violations),
            message=f"Critical violations detected: {len(violations)} issues require immediate attention",
            metadata={
                'violations': violations,
                'review_type': result.review_type.value
            }
        )
        
        await self._publish_event(AgroEventType.CRITICAL_VIOLATION_DETECTED, payload)
    
    async def publish_system_ready(self) -> None:
        """Publish event when AGRO system is ready"""
        payload = AgroEventPayload(
            message="AGRO bee-to-peer review system is ready for sacred collaboration",
            metadata={
                'system_version': '1.0.0',
                'capabilities': [
                    'pain_analysis',
                    'peer_collaboration', 
                    'aggressive_scrutiny',
                    'sacred_protocol_validation',
                    'divine_blessing_assessment'
                ]
            }
        )
        
        await self._publish_event(AgroEventType.AGRO_SYSTEM_READY, payload)
    
    async def publish_circuit_breaker_opened(self, 
                                           component: str,
                                           reason: str) -> None:
        """Publish event when circuit breaker opens"""
        payload = AgroEventPayload(
            message=f"Circuit breaker opened for {component}: {reason}",
            metadata={
                'component': component,
                'reason': reason,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        await self._publish_event(AgroEventType.CIRCUIT_BREAKER_OPENED, payload)
    
    async def _publish_event(self, 
                           event_type: AgroEventType, 
                           payload: AgroEventPayload) -> None:
        """
        Internal method to publish events to the Hive event bus
        
        Args:
            event_type: Type of AGRO event
            payload: Event payload data
        """
        try:
            # Create Pollen Protocol event
            event = PollenEvent(
                event_type=event_type.value,
                source_component="agro_review_system",
                payload=payload.__dict__,
                timestamp=datetime.utcnow().isoformat(),
                event_id=f"agro_{uuid.uuid4().hex[:8]}"
            )
            
            # Add to local history
            self.event_history.append(event)
            if len(self.event_history) > self.max_history_size:
                self.event_history.pop(0)
            
            # Publish to event bus if available
            if self.event_bus:
                await self.event_bus.publish(event)
            
            # Handle locally registered handlers
            await self._handle_event_locally(event_type, event)
            
            self.events_published += 1
            
        except Exception as e:
            self.failed_events += 1
            # Log error but don't raise to prevent breaking the review process
            print(f"Failed to publish AGRO event {event_type}: {e}")
    
    async def _handle_event_locally(self, 
                                  event_type: AgroEventType, 
                                  event: PollenEvent) -> None:
        """Handle events with locally registered handlers"""
        handlers = self.event_handlers.get(event_type, [])
        
        for handler in handlers:
            try:
                await handler(event)
                self.events_handled += 1
            except Exception as e:
                self.failed_events += 1
                print(f"Event handler failed for {event_type}: {e}")
    
    def get_event_history(self, 
                         event_type: Optional[AgroEventType] = None,
                         limit: Optional[int] = None) -> List[PollenEvent]:
        """
        Get event history with optional filtering
        
        Args:
            event_type: Filter by specific event type
            limit: Maximum number of events to return
            
        Returns:
            List[PollenEvent]: Filtered event history
        """
        events = self.event_history
        
        if event_type:
            events = [e for e in events if e.event_type == event_type.value]
        
        if limit:
            events = events[-limit:]
        
        return events
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get event connector statistics"""
        return {
            'events_published': self.events_published,
            'events_handled': self.events_handled,
            'failed_events': self.failed_events,
            'history_size': len(self.event_history),
            'registered_handlers': {
                event_type.value: len(handlers) 
                for event_type, handlers in self.event_handlers.items()
            },
            'event_bus_connected': self.event_bus is not None
        }
    
    def clear_history(self) -> int:
        """Clear event history and reset statistics"""
        cleared_count = len(self.event_history)
        self.event_history.clear()
        
        # Reset statistics
        self.events_published = 0
        self.events_handled = 0
        self.failed_events = 0
        
        return cleared_count