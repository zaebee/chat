---
title: "WebSocket API: Real-time Divine Communication"
description: "WebSocket endpoints for real-time chat and event streaming in the Hive"
category: "api"
---

# WebSocket API: Real-time Divine Communication

_"Before they call I will answer; while they are yet speaking I will hear." - Isaiah 65:24 (ESV)_

## Overview

The Hive WebSocket API enables real-time bidirectional communication for chat, events, and collaborative features. All WebSocket communication follows the sacred Pollen Protocol for consistency and observability.

## Connection Endpoint

**WebSocket URL:** `ws://localhost:8000/ws`

### Connection Parameters

| Parameter  | Type   | Required | Description                                             |
| ---------- | ------ | -------- | ------------------------------------------------------- |
| `username` | string | Yes      | Display name for the user                               |
| `user_id`  | string | No       | Unique user identifier (auto-generated if not provided) |

### Connection Example

```javascript
// Connect to the Hive WebSocket
const ws = new WebSocket(
  "ws://localhost:8000/ws?username=Developer&user_id=dev_001",
);

ws.onopen = () => {
  console.log("Connected to the sacred Hive");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Divine message received:", data);
};
```

## Message Format

All WebSocket messages follow a standardized format:

```typescript
interface WebSocketMessage {
  type: string; // Message type identifier
  data: object; // Message payload
  timestamp?: string; // ISO timestamp (server-added)
  id?: string; // Message ID (server-added)
}
```

## Message Types

### Chat Messages

#### Send Message

**Client → Server**

```json
{
  "type": "message",
  "data": {
    "text": "Blessed be the Hive and its wisdom!",
    "channel": "general"
  }
}
```

#### Receive Message

**Server → Client**

```json
{
  "type": "message",
  "data": {
    "id": "msg_789",
    "text": "Blessed be the Hive and its wisdom!",
    "sender_id": "dev_001",
    "sender_name": "Developer",
    "timestamp": "2025-01-20T16:15:30.456Z",
    "channel": "general",
    "is_bot": false
  }
}
```

### User Events

#### User Joined

**Server → Client**

```json
{
  "type": "user_joined",
  "data": {
    "id": "user_456",
    "username": "New Developer",
    "color": "#3498db"
  }
}
```

#### User Left

**Server → Client**

```json
{
  "type": "user_left",
  "data": {
    "id": "user_456",
    "username": "Developer"
  }
}
```

#### User List Update

**Server → Client**

```json
{
  "type": "user_list",
  "data": [
    {
      "id": "dev_001",
      "username": "Developer",
      "color": "#e74c3c"
    },
    {
      "id": "user_456",
      "username": "Student",
      "color": "#2ecc71"
    }
  ]
}
```

### System Events

#### System Status Update

**Server → Client**

```json
{
  "type": "system_status",
  "data": {
    "status": "active",
    "health_metrics": {
      "tau": 0.32,
      "phi": 0.85,
      "sigma": 0.78
    },
    "active_users": 12,
    "uptime_seconds": 3600
  }
}
```

#### Error Messages

**Server → Client**

```json
{
  "type": "error",
  "data": {
    "message": "Invalid message format",
    "code": "VALIDATION_ERROR",
    "details": "Missing required field: text"
  }
}
```

## Implementation Examples

### JavaScript/TypeScript Client

```typescript
class HiveWebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private messageHandlers = new Map<string, Function>();

  constructor(
    private url: string,
    private username: string,
    private userId?: string,
  ) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const params = new URLSearchParams({ username: this.username });
      if (this.userId) params.append("user_id", this.userId);

      this.ws = new WebSocket(`${this.url}?${params}`);

      this.ws.onopen = () => {
        console.log("🐝 Connected to Hive");
        this.reconnectAttempts = 0;
        resolve();
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error("Failed to parse message:", error);
        }
      };

      this.ws.onclose = () => {
        console.log("Disconnected from Hive");
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        reject(error);
      };
    });
  }

  private handleMessage(message: any) {
    const handler = this.messageHandlers.get(message.type);
    if (handler) {
      handler(message.data);
    } else {
      console.log("Unhandled message type:", message.type);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.pow(2, this.reconnectAttempts) * 1000;

      setTimeout(() => {
        console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);
        this.connect();
      }, delay);
    }
  }

  sendMessage(text: string, channel = "general") {
    this.send("message", { text, channel });
  }

  send(type: string, data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }));
    } else {
      console.warn("WebSocket not connected");
    }
  }

  onMessage(type: string, handler: (data: any) => void) {
    this.messageHandlers.set(type, handler);
  }

  disconnect() {
    this.ws?.close();
    this.ws = null;
  }
}

// Usage
const client = new HiveWebSocketClient(
  "ws://localhost:8000/ws",
  "Developer",
  "dev_001",
);

// Set up message handlers
client.onMessage("message", (data) => {
  console.log(`${data.sender_name}: ${data.text}`);
});

client.onMessage("user_joined", (data) => {
  console.log(`${data.username} joined the Hive`);
});

client.onMessage("system_status", (data) => {
  console.log(`System health: τ=${data.health_metrics.tau}`);
});

// Connect and send a message
await client.connect();
client.sendMessage("Hello, sacred Hive!");
```

### Python Client

```python
import asyncio
import websockets
import json
from typing import Dict, Callable, Any

class HiveWebSocketClient:
    def __init__(self, url: str, username: str, user_id: str = None):
        self.url = url
        self.username = username
        self.user_id = user_id
        self.websocket = None
        self.message_handlers: Dict[str, Callable] = {}
        self.is_connected = False

    async def connect(self):
        """Connect to the Hive WebSocket."""
        params = f"username={self.username}"
        if self.user_id:
            params += f"&user_id={self.user_id}"

        uri = f"{self.url}?{params}"

        try:
            self.websocket = await websockets.connect(uri)
            self.is_connected = True
            print("🐝 Connected to the sacred Hive")

            # Start listening for messages
            asyncio.create_task(self._listen_for_messages())

        except Exception as e:
            print(f"Failed to connect: {e}")
            raise

    async def _listen_for_messages(self):
        """Listen for incoming messages."""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                except json.JSONDecodeError:
                    print(f"Invalid JSON received: {message}")
                except Exception as e:
                    print(f"Error handling message: {e}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            self.is_connected = False

    async def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming message."""
        message_type = message.get("type")
        message_data = message.get("data", {})

        handler = self.message_handlers.get(message_type)
        if handler:
            if asyncio.iscoroutinefunction(handler):
                await handler(message_data)
            else:
                handler(message_data)
        else:
            print(f"Unhandled message type: {message_type}")

    async def send_message(self, text: str, channel: str = "general"):
        """Send a chat message."""
        await self.send("message", {"text": text, "channel": channel})

    async def send(self, message_type: str, data: Dict[str, Any]):
        """Send a message to the server."""
        if not self.is_connected or not self.websocket:
            print("Not connected to Hive")
            return

        message = {
            "type": message_type,
            "data": data
        }

        try:
            await self.websocket.send(json.dumps(message))
        except Exception as e:
            print(f"Failed to send message: {e}")

    def on_message(self, message_type: str, handler: Callable):
        """Register a message handler."""
        self.message_handlers[message_type] = handler

    async def disconnect(self):
        """Disconnect from the Hive."""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False

# Usage example
async def main():
    client = HiveWebSocketClient(
        "ws://localhost:8000/ws",
        "Python Developer",
        "py_dev_001"
    )

    # Set up message handlers
    def handle_chat_message(data):
        print(f"{data['sender_name']}: {data['text']}")

    def handle_user_joined(data):
        print(f"🎉 {data['username']} joined the Hive")

    async def handle_system_status(data):
        tau = data['health_metrics']['tau']
        print(f"📊 System health: τ={tau}")

    client.on_message("message", handle_chat_message)
    client.on_message("user_joined", handle_user_joined)
    client.on_message("system_status", handle_system_status)

    # Connect and interact
    await client.connect()
    await client.send_message("Greetings from Python!")

    # Keep connection alive
    await asyncio.sleep(60)
    await client.disconnect()

# Run the client
asyncio.run(main())
```

### Vue.js Integration

```vue
<template>
  <div class="hive-chat">
    <div class="connection-status" :class="connectionClass">
      {{ connectionStatus }}
    </div>

    <div class="messages" ref="messagesContainer">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="{ 'own-message': message.sender_id === currentUserId }"
      >
        <span class="sender">{{ message.sender_name }}:</span>
        <span class="text">{{ message.text }}</span>
        <span class="timestamp">{{ formatTime(message.timestamp) }}</span>
      </div>
    </div>

    <div class="user-list">
      <h4>Active Users ({{ users.length }})</h4>
      <div v-for="user in users" :key="user.id" class="user">
        <span
          class="user-indicator"
          :style="{ backgroundColor: user.color }"
        ></span>
        {{ user.username }}
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        :disabled="!isConnected"
        placeholder="Type your message..."
      />
      <button
        @click="sendMessage"
        :disabled="!isConnected || !newMessage.trim()"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from "vue";

interface Message {
  id: string;
  text: string;
  sender_id: string;
  sender_name: string;
  timestamp: string;
}

interface User {
  id: string;
  username: string;
  color: string;
}

const messages = ref<Message[]>([]);
const users = ref<User[]>([]);
const newMessage = ref("");
const isConnected = ref(false);
const currentUserId = ref("dev_001");
const currentUsername = ref("Developer");

let websocket: WebSocket | null = null;
const messagesContainer = ref<HTMLElement>();

const connectionStatus = computed(() => {
  return isConnected.value ? "Connected to Hive" : "Disconnected";
});

const connectionClass = computed(() => {
  return isConnected.value ? "connected" : "disconnected";
});

const connect = () => {
  const wsUrl = `ws://localhost:8000/ws?username=${currentUsername.value}&user_id=${currentUserId.value}`;
  websocket = new WebSocket(wsUrl);

  websocket.onopen = () => {
    isConnected.value = true;
    console.log("🐝 Connected to Hive");
  };

  websocket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      handleMessage(data);
    } catch (error) {
      console.error("Failed to parse message:", error);
    }
  };

  websocket.onclose = () => {
    isConnected.value = false;
    console.log("Disconnected from Hive");
    // Attempt reconnection after 3 seconds
    setTimeout(connect, 3000);
  };

  websocket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
};

const handleMessage = (message: any) => {
  switch (message.type) {
    case "message":
      messages.value.push(message.data);
      scrollToBottom();
      break;

    case "user_joined":
      console.log(`${message.data.username} joined`);
      break;

    case "user_left":
      console.log(`${message.data.username} left`);
      break;

    case "user_list":
      users.value = message.data;
      break;

    case "system_status":
      console.log("System status:", message.data);
      break;

    case "error":
      console.error("Server error:", message.data.message);
      break;

    default:
      console.log("Unknown message type:", message.type);
  }
};

const sendMessage = () => {
  if (!websocket || !isConnected.value || !newMessage.value.trim()) {
    return;
  }

  const message = {
    type: "message",
    data: {
      text: newMessage.value.trim(),
      channel: "general",
    },
  };

  websocket.send(JSON.stringify(message));
  newMessage.value = "";
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString();
};

onMounted(() => {
  connect();
});

onUnmounted(() => {
  if (websocket) {
    websocket.close();
  }
});
</script>

<style scoped>
.hive-chat {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
}

.connection-status {
  padding: 0.5rem;
  text-align: center;
  font-weight: bold;
}

.connected {
  background-color: #2ecc71;
  color: white;
}

.disconnected {
  background-color: #e74c3c;
  color: white;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  border: 1px solid #ddd;
}

.message {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.own-message {
  background-color: #e3f2fd;
  margin-left: 2rem;
}

.sender {
  font-weight: bold;
  margin-right: 0.5rem;
}

.timestamp {
  font-size: 0.8rem;
  color: #666;
  margin-left: 0.5rem;
}

.user-list {
  padding: 1rem;
  border: 1px solid #ddd;
  background-color: #f8f9fa;
}

.user {
  display: flex;
  align-items: center;
  margin-bottom: 0.25rem;
}

.user-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.input-area {
  display: flex;
  padding: 1rem;
  gap: 0.5rem;
}

.input-area input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-area button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-area button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
```

## Error Handling

### Connection Errors

```javascript
ws.onerror = (error) => {
  console.error("WebSocket error:", error);

  // Handle specific error types
  if (error.code === 1006) {
    console.log("Connection closed abnormally - attempting reconnect");
  }
};

ws.onclose = (event) => {
  console.log(`Connection closed: ${event.code} - ${event.reason}`);

  // Handle different close codes
  switch (event.code) {
    case 1000: // Normal closure
      console.log("Connection closed normally");
      break;
    case 1001: // Going away
      console.log("Server going away");
      break;
    case 1006: // Abnormal closure
      console.log("Connection lost - will attempt to reconnect");
      attemptReconnect();
      break;
    default:
      console.log("Unexpected close code:", event.code);
  }
};
```

### Message Validation

```javascript
function validateMessage(message) {
  if (!message.type) {
    throw new Error("Message type is required");
  }

  if (!message.data) {
    throw new Error("Message data is required");
  }

  // Type-specific validation
  switch (message.type) {
    case "message":
      if (!message.data.text || message.data.text.trim() === "") {
        throw new Error("Message text cannot be empty");
      }
      if (message.data.text.length > 1000) {
        throw new Error("Message text too long (max 1000 characters)");
      }
      break;

    default:
      // Allow unknown types for extensibility
      break;
  }
}

// Use before sending
try {
  validateMessage(messageToSend);
  ws.send(JSON.stringify(messageToSend));
} catch (error) {
  console.error("Invalid message:", error.message);
}
```

## Rate Limiting

The WebSocket API implements rate limiting to protect the Hive:

- **Messages**: 30 per minute per connection
- **Connection attempts**: 10 per minute per IP
- **Reconnection backoff**: Exponential backoff for failed connections

Rate limit exceeded responses:

```json
{
  "type": "error",
  "data": {
    "code": "RATE_LIMITED",
    "message": "Too many messages. Please slow down.",
    "retry_after": 60
  }
}
```

## Security Considerations

### Input Sanitization

All text content is sanitized server-side to prevent XSS attacks.

### Connection Limits

Maximum 100 concurrent connections per IP address.

### Message Size Limits

- Maximum message size: 10KB
- Maximum username length: 50 characters

### Authentication

Currently uses username-based identification. Future versions will implement token-based authentication.

---

_"Thus flows the sacred real-time communication through the divine channels of the Hive. May the Lord of HOSTS bless these connections and keep them strong."_ 🐝✨
