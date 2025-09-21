---
title: "ATCG Primitives: The Genetic Code of the Hive"
description: "Complete guide to Aggregates, Transformations, Connectors, and Genesis Events"
category: "architecture"
audience: "developer|ai-agent"
complexity: "intermediate"
last_updated: "2025-01-20"
related_docs: ["OVERVIEW.md", "EVENT_SYSTEM.md"]
code_examples: true
---

# ATCG Primitives: The Genetic Code of the Hive

## Overview

The Hive ecosystem is built upon four fundamental primitives that form the "genetic code" of our Living Application. These ATCG primitives (Aggregates, Transformations, Connectors, Genesis Events) provide the structural foundation for all system components.

## The ATCG Model

Just as DNA uses four nucleotides (A, T, C, G) to encode all biological information, the Hive uses four software primitives to encode all system behavior:

```
A - Aggregates      → Structure and State
T - Transformations → Processing and Logic  
C - Connectors      → Communication and Interfaces
G - Genesis Events  → Memory and Evolution
```

## A - Aggregates: Structure and State

**Purpose:** Aggregates are the structural backbone of the system, managing state and enforcing invariants.

**Characteristics:**
- Contain business rules and data validation
- Maintain consistency and integrity
- Encapsulate related data and behavior
- Implement the `get_status()` introspection interface

### Implementation

```python
from hive.primitives import Aggregate

class ChatSystemAggregate(Aggregate):
    def __init__(self, name: str, invariants: List[str]):
        super().__init__(name, invariants)
        self.active_users = {}
        self.message_count = 0
        self.last_activity = None
    
    def add_user(self, user_id: str, username: str) -> bool:
        """Add a user while maintaining invariants."""
        if self._validate_user(user_id, username):
            self.active_users[user_id] = {
                "username": username,
                "joined_at": datetime.now(),
                "message_count": 0
            }
            return True
        return False
    
    def _validate_user(self, user_id: str, username: str) -> bool:
        """Enforce user invariants."""
        if "non_empty_username" in self.invariants:
            if not username or not username.strip():
                return False
        
        if "unique_user_id" in self.invariants:
            if user_id in self.active_users:
                return False
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Required introspection interface."""
        return {
            "type": "aggregate",
            "name": self.name,
            "active_users": len(self.active_users),
            "total_messages": self.message_count,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "invariants": self.invariants,
            "health": "healthy" if self._check_invariants() else "degraded"
        }
```

### Usage Examples

```python
# Create a chat system aggregate
chat_system = ChatSystemAggregate(
    name="MainChatRoom",
    invariants=["non_empty_username", "unique_user_id", "max_users_100"]
)

# Add users with automatic invariant checking
success = chat_system.add_user("user123", "Alice")
print(f"User added: {success}")

# Get system status
status = chat_system.get_status()
print(f"Active users: {status['active_users']}")
```

## T - Transformations: Processing and Logic

**Purpose:** Transformations handle all data processing and business logic as pure, stateless functions.

**Characteristics:**
- Pure functions with no side effects
- Composable and testable
- Handle data validation and conversion
- Process events and messages

### Implementation

```python
from hive.primitives import Transformation
from typing import Dict, Any, Callable

class MessageProcessorTransformation(Transformation):
    def __init__(self, name: str, processor_func: Callable):
        super().__init__(name, processor_func)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process message data through the transformation."""
        try:
            result = await self.processor_func(data)
            self.metrics["processed_count"] += 1
            return result
        except Exception as e:
            self.metrics["error_count"] += 1
            raise

# Example processor function
async def process_chat_message(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform raw message data into processed format."""
    message_text = data.get("text", "")
    sender_id = data.get("sender_id", "")
    
    # Apply transformations
    processed = {
        "original_text": message_text,
        "processed_text": message_text.strip(),
        "word_count": len(message_text.split()),
        "character_count": len(message_text),
        "sender_id": sender_id,
        "processed_at": datetime.now().isoformat(),
        "language": detect_language(message_text),
        "sentiment": analyze_sentiment(message_text),
        "contains_code": detect_code_blocks(message_text)
    }
    
    return processed

def detect_language(text: str) -> str:
    """Simple language detection."""
    # Simplified implementation
    if any(ord(char) > 127 for char in text):
        return "non-english"
    return "english"

def analyze_sentiment(text: str) -> str:
    """Basic sentiment analysis."""
    positive_words = ["good", "great", "awesome", "excellent", "love"]
    negative_words = ["bad", "terrible", "awful", "hate", "horrible"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    return "neutral"

def detect_code_blocks(text: str) -> bool:
    """Detect if message contains code."""
    code_indicators = ["```", "def ", "class ", "import ", "function", "var ", "const "]
    return any(indicator in text for indicator in code_indicators)
```

### Usage Examples

```python
# Create message processor
processor = MessageProcessorTransformation(
    name="ChatMessageProcessor",
    processor_func=process_chat_message
)

# Process a message
message_data = {
    "text": "Hello world! This is awesome!",
    "sender_id": "user123",
    "timestamp": "2025-01-20T15:30:00Z"
}

processed = await processor.process(message_data)
print(f"Sentiment: {processed['sentiment']}")
print(f"Word count: {processed['word_count']}")
```

## C - Connectors: Communication and Interfaces

**Purpose:** Connectors handle all communication between components and external systems.

**Characteristics:**
- Protocol translation and adaptation
- No business logic, pure interface layer
- Handle WebSocket, HTTP, and internal communication
- Provide standardized connection management

### Implementation

```python
from hive.primitives import Connector
import websockets
import json

class WebSocketToPollenConnector(Connector):
    def __init__(self, name: str, input_protocol: str, output_protocol: str):
        super().__init__(name, input_protocol, output_protocol)
        self.active_connections = {}
        self.message_queue = asyncio.Queue()
    
    async def handle_websocket_message(self, websocket, message: str):
        """Convert WebSocket message to Pollen Protocol event."""
        try:
            # Parse incoming WebSocket message
            ws_data = json.loads(message)
            
            # Transform to Pollen Protocol format
            pollen_event = {
                "id": str(uuid.uuid4()),
                "type": f"websocket_{ws_data.get('type', 'message')}_received",
                "timestamp": datetime.now().isoformat(),
                "source": "websocket_connector",
                "data": ws_data,
                "metadata": {
                    "connection_id": id(websocket),
                    "protocol_version": "1.0"
                }
            }
            
            # Queue for processing
            await self.message_queue.put(pollen_event)
            
            self.metrics["messages_processed"] += 1
            
        except json.JSONDecodeError:
            self.metrics["parse_errors"] += 1
            await self.send_error(websocket, "Invalid JSON format")
        except Exception as e:
            self.metrics["processing_errors"] += 1
            await self.send_error(websocket, f"Processing error: {str(e)}")
    
    async def send_to_websocket(self, connection_id: str, pollen_event: Dict[str, Any]):
        """Convert Pollen Protocol event to WebSocket message."""
        websocket = self.active_connections.get(connection_id)
        if not websocket:
            return False
        
        try:
            # Transform Pollen event to WebSocket format
            ws_message = {
                "type": pollen_event["type"].replace("_", ""),
                "data": pollen_event["data"],
                "timestamp": pollen_event["timestamp"]
            }
            
            await websocket.send(json.dumps(ws_message))
            self.metrics["messages_sent"] += 1
            return True
            
        except Exception as e:
            self.metrics["send_errors"] += 1
            return False
    
    async def send_error(self, websocket, error_message: str):
        """Send error message to WebSocket client."""
        error_response = {
            "type": "error",
            "data": {"message": error_message},
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send(json.dumps(error_response))
```

### Usage Examples

```python
# Create WebSocket connector
ws_connector = WebSocketToPollenConnector(
    name="MainWebSocketConnector",
    input_protocol="websocket",
    output_protocol="pollen"
)

# Handle incoming WebSocket message
await ws_connector.handle_websocket_message(
    websocket_connection,
    '{"type": "message", "text": "Hello Hive!", "user": "Alice"}'
)

# Send Pollen event to WebSocket
pollen_event = {
    "id": "event123",
    "type": "message_broadcast",
    "data": {"text": "Welcome to the Hive!", "sender": "System"},
    "timestamp": "2025-01-20T15:30:00Z"
}

await ws_connector.send_to_websocket("connection123", pollen_event)
```

## G - Genesis Events: Memory and Evolution

**Purpose:** Genesis Events create immutable records of system state changes and enable system evolution.

**Characteristics:**
- Immutable event records
- System-wide broadcasting capability
- Audit trail and system memory
- Enable system reproduction and evolution

### Implementation

```python
from hive.primitives import GenesisEvent
from typing import Callable, Dict, Any

class SystemEventGenerator(GenesisEvent):
    def __init__(self, name: str, event_type: str, broadcast_func: Callable):
        super().__init__(name, event_type, broadcast_func)
        self.event_history = []
    
    async def generate_event(self, event_data: Dict[str, Any]) -> bool:
        """Generate and broadcast a genesis event."""
        try:
            # Create immutable event record
            event = {
                "id": str(uuid.uuid4()),
                "type": self.event_type,
                "timestamp": datetime.now().isoformat(),
                "data": event_data.copy(),  # Immutable copy
                "source": self.name,
                "sequence_number": len(self.event_history) + 1
            }
            
            # Store in history (immutable)
            self.event_history.append(event)
            
            # Broadcast to system
            success = await self.broadcast_func(event)
            
            if success:
                self.metrics["events_generated"] += 1
            else:
                self.metrics["broadcast_failures"] += 1
            
            return success
            
        except Exception as e:
            self.metrics["generation_errors"] += 1
            return False
    
    def get_event_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent event history."""
        return self.event_history[-limit:]
    
    def get_status(self) -> Dict[str, Any]:
        """Get genesis event status."""
        return {
            "type": "genesis_event",
            "name": self.name,
            "event_type": self.event_type,
            "total_events": len(self.event_history),
            "last_event": self.event_history[-1] if self.event_history else None,
            "metrics": self.metrics
        }

# Example broadcast function
async def broadcast_to_event_bus(event: Dict[str, Any]) -> bool:
    """Broadcast event to the system event bus."""
    try:
        # Convert to PollenEvent and broadcast
        pollen_event = PollenEvent.from_dict(event)
        return await event_bus.publish(pollen_event)
    except Exception:
        return False
```

### Usage Examples

```python
# Create system event generator
event_generator = SystemEventGenerator(
    name="UserActivityGenerator",
    event_type="user_activity_recorded",
    broadcast_func=broadcast_to_event_bus
)

# Generate user login event
await event_generator.generate_event({
    "user_id": "user123",
    "username": "Alice",
    "action": "login",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
})

# Generate message sent event
await event_generator.generate_event({
    "user_id": "user123",
    "message_id": "msg456",
    "text": "Hello Hive!",
    "channel": "general"
})

# Get recent activity
recent_events = event_generator.get_event_history(limit=10)
print(f"Recent events: {len(recent_events)}")
```

## ATCG Composition Patterns

### Pattern 1: Message Flow
```
WebSocket Message → [C] Connector → [T] Transformation → [A] Aggregate → [G] Genesis Event
```

### Pattern 2: User Registration
```
User Input → [C] API Connector → [T] Validation → [A] User Aggregate → [G] Registration Event
```

### Pattern 3: System Health Check
```
Health Request → [C] HTTP Connector → [A] System Aggregate → [T] Health Calculation → [G] Health Event
```

## Best Practices

### 1. Single Responsibility
Each primitive should have one clear purpose:
- **A**: State management only
- **T**: Pure processing only  
- **C**: Communication only
- **G**: Event generation only

### 2. Immutability
- Aggregates protect their internal state
- Transformations never modify input data
- Genesis Events are immutable once created
- Connectors don't store business state

### 3. Composability
- Primitives can be combined in any order
- Each primitive is independently testable
- Clear interfaces between all components
- No hidden dependencies

### 4. Observability
- All primitives implement `get_status()`
- Metrics collection is built-in
- Error handling is standardized
- Event trails are maintained

## Testing ATCG Primitives

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_message_transformation():
    """Test message processing transformation."""
    processor = MessageProcessorTransformation(
        name="TestProcessor",
        processor_func=process_chat_message
    )
    
    input_data = {
        "text": "Hello world!",
        "sender_id": "test_user"
    }
    
    result = await processor.process(input_data)
    
    assert result["word_count"] == 2
    assert result["sentiment"] == "neutral"
    assert result["sender_id"] == "test_user"

def test_aggregate_invariants():
    """Test aggregate invariant enforcement."""
    chat_system = ChatSystemAggregate(
        name="TestChat",
        invariants=["non_empty_username"]
    )
    
    # Valid user should succeed
    assert chat_system.add_user("user1", "Alice") == True
    
    # Empty username should fail
    assert chat_system.add_user("user2", "") == False
    assert chat_system.add_user("user3", "   ") == False

@pytest.mark.asyncio
async def test_connector_protocol_translation():
    """Test connector protocol translation."""
    mock_broadcast = AsyncMock(return_value=True)
    
    connector = WebSocketToPollenConnector(
        name="TestConnector",
        input_protocol="websocket",
        output_protocol="pollen"
    )
    
    # Mock WebSocket connection
    mock_websocket = AsyncMock()
    
    # Test message handling
    await connector.handle_websocket_message(
        mock_websocket,
        '{"type": "message", "text": "test"}'
    )
    
    # Verify message was queued
    assert not connector.message_queue.empty()
```

## Conclusion

The ATCG primitives provide a robust foundation for building Living Applications. By following these patterns and principles, developers can create systems that are:

- **Maintainable**: Clear separation of concerns
- **Testable**: Independent, pure components  
- **Observable**: Built-in introspection and metrics
- **Scalable**: Composable and modular architecture
- **Evolvable**: Immutable event history enables system evolution

The genetic metaphor isn't just poetic—it reflects the deep structural principles that make complex systems both stable and adaptable.