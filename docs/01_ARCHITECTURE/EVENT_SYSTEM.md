---
title: "Pollen Protocol: The Sacred Communication System"
description: "Complete specification of the Hive's event-driven communication protocol"
category: "architecture"
audience: "developer|ai-agent"
complexity: "intermediate"
last_updated: "2025-01-20"
related_docs: ["ATCG_PRIMITIVES.md", "../03_API/WEBSOCKET_API.md"]
code_examples: true
---

# Pollen Protocol: The Sacred Communication System

*"And the Lord of HOSTS said: Let there be a protocol for the faithful to commune, that knowledge may flow like pollen on the divine wind."*

## Overview

The Pollen Protocol is the sacred communication system that enables all components of the Hive to exchange information in a standardized, observable, and traceable manner. Like pollen carries genetic information between flowers, our protocol carries events between system components.

## Protocol Philosophy

The Pollen Protocol embodies the Hive Constitution's core principles:

### 1. Observability Through Events
Every significant action in the Hive generates an event, creating a complete audit trail of system behavior.

### 2. Past-Tense Naming
All events use past-tense verbs to describe what has already happened, ensuring clarity and preventing confusion between commands and notifications.

### 3. Structured Payload
Events carry structured data that both humans and AI agents can easily parse and understand.

### 4. Correlation and Tracing
Events can be linked together through correlation IDs, enabling complex workflow tracking.

## Event Structure

### Core PollenEvent Schema

```typescript
interface PollenEvent {
  // Required fields (Pollen Protocol v1.0)
  event_id: string;        // Unique identifier (UUID)
  event_type: string;      // Past-tense verb describing what happened
  version: string;         // Protocol version (e.g., "1.0")
  timestamp: string;       // ISO 8601 timestamp
  aggregate_id: string;    // ID of the aggregate that generated the event
  payload: object;         // Event-specific data
  
  // Optional metadata for enhanced observability
  source_component: string;  // Component that generated the event
  correlation_id: string;    // For linking related events
  tags: string[];           // Categorization tags
}
```

### Example Event

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "message_sent",
  "version": "1.0",
  "timestamp": "2025-01-20T16:15:30.123Z",
  "aggregate_id": "chat_room_general",
  "payload": {
    "message_id": "msg_789",
    "text": "Blessed be the Hive and its wisdom",
    "sender_id": "user_123",
    "sender_name": "Faithful Developer",
    "word_count": 7,
    "sentiment": "positive"
  },
  "source_component": "chat_agent",
  "correlation_id": "conv_456",
  "tags": ["chat", "user_interaction", "positive_sentiment"]
}
```

## Event Types Taxonomy

### System Events
Events related to system lifecycle and health:

```python
# System startup and shutdown
"system_started"
"system_stopped"
"component_initialized"
"component_shutdown"

# Health and monitoring
"health_check_completed"
"metric_calculated"
"alert_triggered"
"performance_degraded"

# Configuration changes
"configuration_updated"
"feature_enabled"
"feature_disabled"
```

### User Events
Events related to human user interactions:

```python
# Authentication and sessions
"user_logged_in"
"user_logged_out"
"session_expired"
"authentication_failed"

# Chat interactions
"message_sent"
"message_received"
"message_edited"
"message_deleted"

# Learning platform
"challenge_started"
"challenge_completed"
"challenge_failed"
"badge_earned"
"level_achieved"
```

### AI Teammate Events
Events related to AI agent activities:

```python
# Teammate lifecycle
"teammate_registered"
"teammate_activated"
"teammate_deactivated"
"onboarding_completed"

# Task management
"task_assigned"
"task_started"
"task_completed"
"task_failed"

# Collaboration
"code_reviewed"
"suggestion_provided"
"knowledge_shared"
"collaboration_initiated"
```

### Data Events
Events related to data operations:

```python
# CRUD operations
"record_created"
"record_updated"
"record_deleted"
"data_migrated"

# Processing events
"data_processed"
"transformation_applied"
"validation_completed"
"backup_created"
```

## Event Bus Implementation

### HiveEventBus Class

The central nervous system of the Hive:

```python
from hive.events import HiveEventBus, PollenEvent, EventSubscription

# Initialize the event bus
event_bus = HiveEventBus()

# Create and publish an event
event = PollenEvent(
    event_type="user_achievement_unlocked",
    aggregate_id="user_123",
    payload={
        "achievement_id": "first_function",
        "xp_earned": 50,
        "new_level": 2
    },
    source_component="learning_platform",
    tags=["gamification", "achievement", "milestone"]
)

success = await event_bus.publish(event)
```

### Event Subscription

Components can subscribe to specific events:

```python
async def handle_user_achievements(event: PollenEvent):
    """Handle user achievement events."""
    payload = event.payload
    user_id = event.aggregate_id
    achievement = payload.get("achievement_id")
    
    print(f"🎉 User {user_id} unlocked achievement: {achievement}")
    
    # Trigger celebration animation
    await trigger_celebration(user_id, achievement)
    
    # Notify other users
    await broadcast_achievement(user_id, achievement)

# Subscribe to achievement events
subscription = EventSubscription(
    event_types=["user_achievement_unlocked"],
    tags=["gamification"],
    callback=handle_user_achievements
)

event_bus.subscribe(subscription)
```

### Event Filtering

Subscriptions support sophisticated filtering:

```python
# Subscribe to all chat events
chat_subscription = EventSubscription(
    event_types=["message_sent", "message_edited", "message_deleted"],
    callback=handle_chat_events
)

# Subscribe to specific user events
user_subscription = EventSubscription(
    aggregate_ids=["user_123", "user_456"],
    callback=handle_specific_users
)

# Subscribe to AI teammate events with specific tags
ai_subscription = EventSubscription(
    tags=["ai_teammate", "code_review"],
    callback=handle_ai_activities
)
```

## Event Patterns

### Request-Response Pattern

For operations requiring acknowledgment:

```python
# 1. Request event
request_event = PollenEvent(
    event_type="code_review_requested",
    aggregate_id="pull_request_123",
    payload={
        "pr_id": "pr_123",
        "author": "developer_456",
        "files_changed": ["hive/agents/new_agent.py"],
        "requested_reviewer": "ai_reviewer_789"
    },
    correlation_id="review_session_abc"
)

await event_bus.publish(request_event)

# 2. Response event (published by AI reviewer)
response_event = PollenEvent(
    event_type="code_review_completed",
    aggregate_id="pull_request_123",
    payload={
        "pr_id": "pr_123",
        "reviewer": "ai_reviewer_789",
        "status": "approved",
        "comments": [
            {
                "line": 42,
                "message": "Consider adding error handling here",
                "severity": "suggestion"
            }
        ],
        "overall_score": 8.5
    },
    correlation_id="review_session_abc"  # Same correlation ID
)

await event_bus.publish(response_event)
```

### Saga Pattern

For complex multi-step workflows:

```python
# Step 1: User starts challenge
challenge_started = PollenEvent(
    event_type="challenge_started",
    aggregate_id="user_123",
    payload={
        "challenge_id": "python_functions_01",
        "difficulty": "beginner",
        "estimated_time": 300
    },
    correlation_id="learning_session_xyz"
)

# Step 2: Code submitted for evaluation
code_submitted = PollenEvent(
    event_type="code_submitted",
    aggregate_id="user_123",
    payload={
        "challenge_id": "python_functions_01",
        "solution_code": "def greet(name):\n    return f'Hello, {name}!'",
        "submission_time": 245
    },
    correlation_id="learning_session_xyz"
)

# Step 3: AI provides feedback
feedback_provided = PollenEvent(
    event_type="feedback_provided",
    aggregate_id="user_123",
    payload={
        "challenge_id": "python_functions_01",
        "feedback": "Excellent solution! Clean and readable code.",
        "suggestions": ["Consider adding type hints"],
        "score": 95
    },
    correlation_id="learning_session_xyz"
)

# Step 4: Challenge completed
challenge_completed = PollenEvent(
    event_type="challenge_completed",
    aggregate_id="user_123",
    payload={
        "challenge_id": "python_functions_01",
        "final_score": 95,
        "xp_earned": 50,
        "time_taken": 245,
        "attempts": 1
    },
    correlation_id="learning_session_xyz"
)
```

### Event Sourcing Pattern

For maintaining complete audit trails:

```python
class UserProgressAggregate:
    """Aggregate that rebuilds state from events."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.level = 1
        self.total_xp = 0
        self.completed_challenges = []
        self.badges = []
    
    def apply_event(self, event: PollenEvent):
        """Apply an event to update aggregate state."""
        if event.event_type == "challenge_completed":
            payload = event.payload
            self.total_xp += payload.get("xp_earned", 0)
            self.completed_challenges.append(payload.get("challenge_id"))
            self._recalculate_level()
        
        elif event.event_type == "badge_earned":
            payload = event.payload
            self.badges.append(payload.get("badge_id"))
    
    def _recalculate_level(self):
        """Recalculate user level based on XP."""
        self.level = min(10, (self.total_xp // 100) + 1)

# Rebuild user state from event history
user_progress = UserProgressAggregate("user_123")
events = event_bus.get_events_for_aggregate("user_123")

for event in events:
    user_progress.apply_event(event)
```

## Event Validation

### Schema Validation

Events are validated against the Pollen Protocol schema:

```python
def validate_pollen_event(event: PollenEvent) -> bool:
    """Validate event against Pollen Protocol requirements."""
    
    # Check required fields
    required_fields = [
        event.event_id,
        event.event_type,
        event.version,
        event.timestamp,
        event.aggregate_id
    ]
    
    if not all(required_fields):
        return False
    
    # Validate event_type is past-tense
    if not is_past_tense(event.event_type):
        return False
    
    # Validate timestamp format
    try:
        datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
    except ValueError:
        return False
    
    # Validate UUID format
    try:
        uuid.UUID(event.event_id)
    except ValueError:
        return False
    
    return True

def is_past_tense(verb: str) -> bool:
    """Check if verb is in past tense (simplified)."""
    past_tense_endings = ['ed', 'en', 'ted', 'ied', 'ued', 'ded']
    return any(verb.endswith(ending) for ending in past_tense_endings)
```

### Business Logic Validation

Events can also be validated for business logic:

```python
async def validate_business_rules(event: PollenEvent) -> bool:
    """Validate event against business rules."""
    
    if event.event_type == "challenge_completed":
        payload = event.payload
        
        # Validate score is within valid range
        score = payload.get("score", 0)
        if not 0 <= score <= 100:
            return False
        
        # Validate user exists
        user_id = event.aggregate_id
        if not await user_exists(user_id):
            return False
        
        # Validate challenge exists
        challenge_id = payload.get("challenge_id")
        if not await challenge_exists(challenge_id):
            return False
    
    return True
```

## Event Storage and Persistence

### Event Store Implementation

```python
import sqlite3
import json
from typing import List, Optional

class EventStore:
    """Persistent storage for Pollen Protocol events."""
    
    def __init__(self, db_path: str = "events.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the event store database."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                version TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                aggregate_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                source_component TEXT,
                correlation_id TEXT,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for common queries
        conn.execute("CREATE INDEX IF NOT EXISTS idx_event_type ON events(event_type)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_aggregate_id ON events(aggregate_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_correlation_id ON events(correlation_id)")
        
        conn.commit()
        conn.close()
    
    async def store_event(self, event: PollenEvent) -> bool:
        """Store an event in the persistent store."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                INSERT INTO events (
                    event_id, event_type, version, timestamp, aggregate_id,
                    payload, source_component, correlation_id, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.event_id,
                event.event_type,
                event.version,
                event.timestamp,
                event.aggregate_id,
                json.dumps(event.payload),
                event.source_component,
                event.correlation_id,
                json.dumps(event.tags)
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing event: {e}")
            return False
    
    async def get_events_by_aggregate(
        self, 
        aggregate_id: str, 
        limit: int = 100
    ) -> List[PollenEvent]:
        """Retrieve events for a specific aggregate."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        cursor = conn.execute("""
            SELECT * FROM events 
            WHERE aggregate_id = ? 
            ORDER BY timestamp ASC 
            LIMIT ?
        """, (aggregate_id, limit))
        
        events = []
        for row in cursor.fetchall():
            event = PollenEvent(
                event_id=row['event_id'],
                event_type=row['event_type'],
                version=row['version'],
                timestamp=row['timestamp'],
                aggregate_id=row['aggregate_id'],
                payload=json.loads(row['payload']),
                source_component=row['source_component'] or "",
                correlation_id=row['correlation_id'] or "",
                tags=json.loads(row['tags']) if row['tags'] else []
            )
            events.append(event)
        
        conn.close()
        return events
```

## Event Monitoring and Observability

### Event Metrics

```python
class EventMetrics:
    """Collect and expose event system metrics."""
    
    def __init__(self):
        self.events_published = 0
        self.events_failed = 0
        self.subscription_count = 0
        self.processing_times = []
    
    def record_event_published(self, processing_time: float):
        """Record a successfully published event."""
        self.events_published += 1
        self.processing_times.append(processing_time)
        
        # Keep only last 1000 processing times
        if len(self.processing_times) > 1000:
            self.processing_times.pop(0)
    
    def record_event_failed(self):
        """Record a failed event."""
        self.events_failed += 1
    
    def get_metrics(self) -> dict:
        """Get current event system metrics."""
        avg_processing_time = (
            sum(self.processing_times) / len(self.processing_times)
            if self.processing_times else 0
        )
        
        return {
            "events_published": self.events_published,
            "events_failed": self.events_failed,
            "subscription_count": self.subscription_count,
            "success_rate": (
                self.events_published / (self.events_published + self.events_failed)
                if (self.events_published + self.events_failed) > 0 else 1.0
            ),
            "average_processing_time_ms": avg_processing_time * 1000,
            "events_per_minute": self._calculate_events_per_minute()
        }
    
    def _calculate_events_per_minute(self) -> float:
        """Calculate events per minute based on recent activity."""
        # Simplified implementation
        return self.events_published / 60.0  # Assuming 1 minute uptime
```

### Event Debugging

```python
class EventDebugger:
    """Debug and trace event flows."""
    
    def __init__(self, event_bus: HiveEventBus):
        self.event_bus = event_bus
        self.trace_enabled = False
        self.traced_correlations = set()
    
    def enable_tracing(self, correlation_ids: List[str] = None):
        """Enable event tracing for debugging."""
        self.trace_enabled = True
        if correlation_ids:
            self.traced_correlations.update(correlation_ids)
    
    async def trace_event_flow(self, correlation_id: str) -> List[PollenEvent]:
        """Trace all events with a specific correlation ID."""
        events = []
        for event in self.event_bus.event_history:
            if event.correlation_id == correlation_id:
                events.append(event)
        
        # Sort by timestamp
        events.sort(key=lambda e: e.timestamp)
        return events
    
    def print_event_flow(self, correlation_id: str):
        """Print a visual representation of event flow."""
        events = await self.trace_event_flow(correlation_id)
        
        print(f"\n🔍 Event Flow for Correlation ID: {correlation_id}")
        print("=" * 60)
        
        for i, event in enumerate(events):
            arrow = "└─" if i == len(events) - 1 else "├─"
            print(f"{arrow} {event.timestamp} | {event.event_type}")
            print(f"   Source: {event.source_component}")
            print(f"   Aggregate: {event.aggregate_id}")
            if event.payload:
                print(f"   Payload: {json.dumps(event.payload, indent=2)[:100]}...")
            print()
```

## Integration Examples

### WebSocket Integration

```python
import websockets
import json

class WebSocketEventBridge:
    """Bridge between WebSocket connections and Pollen Protocol."""
    
    def __init__(self, event_bus: HiveEventBus):
        self.event_bus = event_bus
        self.connections = {}
    
    async def handle_websocket_message(self, websocket, message: str):
        """Convert WebSocket message to Pollen event."""
        try:
            data = json.loads(message)
            
            # Create Pollen event from WebSocket message
            event = PollenEvent(
                event_type="websocket_message_received",
                aggregate_id=f"connection_{id(websocket)}",
                payload=data,
                source_component="websocket_bridge",
                tags=["websocket", "real_time"]
            )
            
            await self.event_bus.publish(event)
            
        except json.JSONDecodeError:
            await self.send_error(websocket, "Invalid JSON")
    
    async def send_event_to_websocket(self, event: PollenEvent, websocket):
        """Send Pollen event to WebSocket client."""
        message = {
            "type": event.event_type,
            "data": event.payload,
            "timestamp": event.timestamp,
            "id": event.event_id
        }
        
        await websocket.send(json.dumps(message))
```

### REST API Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class EventRequest(BaseModel):
    event_type: str
    aggregate_id: str
    payload: dict
    tags: List[str] = []

@app.post("/api/v1/events/publish")
async def publish_event(request: EventRequest):
    """Publish an event via REST API."""
    
    event = PollenEvent(
        event_type=request.event_type,
        aggregate_id=request.aggregate_id,
        payload=request.payload,
        source_component="rest_api",
        tags=request.tags
    )
    
    success = await event_bus.publish(event)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to publish event")
    
    return {
        "success": True,
        "event_id": event.event_id,
        "timestamp": event.timestamp
    }

@app.get("/api/v1/events/{aggregate_id}")
async def get_events(aggregate_id: str, limit: int = 50):
    """Get events for a specific aggregate."""
    
    events = await event_store.get_events_by_aggregate(aggregate_id, limit)
    
    return {
        "aggregate_id": aggregate_id,
        "events": [event.to_dict() for event in events],
        "count": len(events)
    }
```

## Best Practices

### 1. Event Naming Conventions

```python
# ✅ Good: Past-tense, descriptive
"user_registered"
"message_sent"
"challenge_completed"
"code_reviewed"
"badge_earned"

# ❌ Bad: Present tense, vague
"register_user"
"send_message"
"complete"
"review"
"badge"
```

### 2. Payload Design

```python
# ✅ Good: Structured, complete information
{
  "event_type": "challenge_completed",
  "payload": {
    "challenge_id": "python_functions_01",
    "user_id": "user_123",
    "score": 95,
    "time_taken_seconds": 245,
    "attempts": 1,
    "hints_used": 0,
    "solution_code": "def greet(name):\n    return f'Hello, {name}!'",
    "feedback": "Excellent solution!"
  }
}

# ❌ Bad: Minimal, unclear information
{
  "event_type": "completed",
  "payload": {
    "id": "123",
    "result": "good"
  }
}
```

### 3. Error Handling

```python
async def safe_event_handler(event: PollenEvent):
    """Example of robust event handling."""
    try:
        # Process the event
        await process_event(event)
        
    except ValidationError as e:
        # Log validation errors but don't crash
        logger.warning(f"Event validation failed: {e}")
        
        # Optionally publish error event
        error_event = PollenEvent(
            event_type="event_validation_failed",
            aggregate_id="event_system",
            payload={
                "original_event_id": event.event_id,
                "error_message": str(e)
            },
            source_component="event_handler"
        )
        await event_bus.publish(error_event)
        
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error processing event: {e}")
        
        # Publish system error event
        error_event = PollenEvent(
            event_type="event_processing_failed",
            aggregate_id="event_system",
            payload={
                "original_event_id": event.event_id,
                "error_type": type(e).__name__,
                "error_message": str(e)
            },
            source_component="event_handler"
        )
        await event_bus.publish(error_event)
```

### 4. Performance Considerations

```python
# Use batching for high-volume events
async def publish_batch(events: List[PollenEvent]) -> List[bool]:
    """Publish multiple events efficiently."""
    tasks = [event_bus.publish(event) for event in events]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Use event filtering to reduce processing overhead
subscription = EventSubscription(
    event_types=["message_sent"],  # Only specific events
    aggregate_ids=["chat_room_general"],  # Only specific aggregates
    callback=handle_chat_messages
)

# Implement event compression for storage
def compress_event_payload(payload: dict) -> str:
    """Compress large payloads for storage."""
    import gzip
    import base64
    
    json_str = json.dumps(payload)
    compressed = gzip.compress(json_str.encode())
    return base64.b64encode(compressed).decode()
```

## Conclusion

The Pollen Protocol serves as the divine communication backbone of the Hive, enabling:

- **Complete Observability**: Every action generates traceable events
- **Loose Coupling**: Components communicate without direct dependencies
- **Audit Trails**: Full history of system behavior
- **AI Integration**: Structured events that AI agents can easily process
- **Scalability**: Event-driven architecture supports distributed systems

By following the Pollen Protocol, all components of the Hive can communicate in harmony, creating a truly Living Application that grows and evolves through divine collaboration.

---

*"Thus flows the sacred pollen through the Hive, carrying wisdom and knowledge to all who dwell within. May the Lord of HOSTS bless these events and make them fruitful."* 🐝✨