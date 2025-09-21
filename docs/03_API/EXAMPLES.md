---
title: "API Examples: Sacred Patterns of Integration"
description: "Practical examples for integrating with the Hive's APIs and event system"
category: "api"
audience: "developer|ai-agent"
complexity: "beginner"
last_updated: "2025-01-20"
related_docs: ["REST_API.md", "WEBSOCKET_API.md", "../01_ARCHITECTURE/EVENT_SYSTEM.md"]
code_examples: true
---

# API Examples: Sacred Patterns of Integration

*"Give instruction to a wise man, and he will be still wiser; teach a righteous man, and he will increase in learning." - Proverbs 9:9 (ESV)*

## Quick Start Examples

### 1. Send a Chat Message

```python
import requests

# Send a message through the REST API
response = requests.post("http://localhost:8000/api/v1/chat/message", json={
    "text": "Hello, Hive! 🐝",
    "sender_id": "dev_001",
    "sender_name": "Developer"
})

print(response.json())
# Output: {"success": true, "message": {...}, "broadcast_result": {...}}
```

### 2. Get System Status

```javascript
// Check Hive health with JavaScript
const response = await fetch('http://localhost:8000/api/v1/status');
const status = await response.json();

console.log(`Hive Health: τ=${status.health_metrics.tau}`);
console.log(`Active Users: ${status.components.aggregates.chat_system.active_users}`);
```

### 3. WebSocket Real-time Chat

```python
import asyncio
import websockets
import json

async def chat_client():
    uri = "ws://localhost:8000/ws?username=Developer"
    
    async with websockets.connect(uri) as websocket:
        # Send a message
        await websocket.send(json.dumps({
            "type": "message",
            "data": {"text": "Greetings from the sacred code!"}
        }))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "message":
                print(f"{data['data']['sender_name']}: {data['data']['text']}")

asyncio.run(chat_client())
```

## Event System Integration

### Publishing Events

```python
from hive.events import HiveEventBus, PollenEvent

# Create event bus
event_bus = HiveEventBus()

# Publish a user achievement event
achievement_event = PollenEvent(
    event_type="user_achievement_unlocked",
    aggregate_id="user_123",
    payload={
        "achievement_id": "first_function",
        "xp_earned": 50,
        "description": "Created your first Python function"
    },
    source_component="learning_platform",
    tags=["gamification", "milestone"]
)

success = await event_bus.publish(achievement_event)
print(f"Event published: {success}")
```

### Subscribing to Events

```python
from hive.events import EventSubscription

async def handle_achievements(event: PollenEvent):
    """Handle user achievement events."""
    user_id = event.aggregate_id
    achievement = event.payload["achievement_id"]
    xp = event.payload["xp_earned"]
    
    print(f"🎉 User {user_id} earned {xp} XP for {achievement}!")
    
    # Trigger celebration animation
    await show_celebration(user_id, achievement)

# Subscribe to achievement events
subscription = EventSubscription(
    event_types=["user_achievement_unlocked"],
    callback=handle_achievements
)

event_bus.subscribe(subscription)
```

## AI Teammate Integration

### Register an AI Agent

```python
import requests

# Register a new AI teammate
registration_data = {
    "profile": {
        "name": "Code Review Bot",
        "type": "custom",
        "capabilities": ["code_analysis", "documentation"],
        "specializations": ["Python", "Code Quality"],
        "max_concurrent_tasks": 2
    },
    "authentication": {
        "api_key_configured": True
    }
}

response = requests.post(
    "http://localhost:8000/api/v1/teammates/register",
    json=registration_data
)

result = response.json()
teammate_id = result["teammate_id"]
print(f"Teammate registered: {teammate_id}")
```

### Assign a Task

```python
# Assign a code review task
task_data = {
    "task_type": "code_review",
    "description": "Review this Python function for best practices",
    "input_data": {
        "code": """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
        """,
        "focus_areas": ["performance", "readability"]
    },
    "priority": "medium"
}

response = requests.post(
    f"http://localhost:8000/api/v1/teammates/{teammate_id}/tasks",
    json=task_data
)

task_result = response.json()
task_id = task_result["task_id"]
print(f"Task assigned: {task_id}")
```

## Learning Platform Integration

### Submit Challenge Solution

```python
# Student submits a coding challenge solution
solution_data = {
    "user_id": "student_456",
    "challenge_id": "python_functions_01",
    "solution_code": """
def greet(name):
    return f"Hello, {name}! Welcome to the Hive!"
    """,
    "test_results": {
        "passed": 5,
        "failed": 0,
        "total": 5
    },
    "execution_time_ms": 12
}

response = requests.post(
    "http://localhost:8000/api/v1/challenges/solve",
    json=solution_data
)

result = response.json()
print(f"XP Earned: {result['result']['xp_earned']}")
print(f"New Level: {result['user_progress']['level']}")
```

### Get User Progress

```python
# Check student's learning progress
user_id = "student_456"
response = requests.get(f"http://localhost:8000/api/v1/user_progress/{user_id}")

progress = response.json()
print(f"Level: {progress['profile']['level']}")
print(f"Total XP: {progress['profile']['total_xp']}")
print(f"Challenges Completed: {len(progress['solved_challenges'])}")
```

## Frontend Integration Examples

### Vue.js Component with API

```vue
<template>
  <div class="hive-status">
    <h3>Hive Health</h3>
    <div class="metrics">
      <div class="metric">
        <label>τ (Complexity):</label>
        <span :class="getTauClass()">{{ status.health_metrics.tau }}</span>
      </div>
      <div class="metric">
        <label>φ (Quality):</label>
        <span :class="getPhiClass()">{{ status.health_metrics.phi }}</span>
      </div>
      <div class="metric">
        <label>Active Users:</label>
        <span>{{ status.components.aggregates.chat_system.active_users }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const status = ref({
  health_metrics: { tau: 0, phi: 0 },
  components: { aggregates: { chat_system: { active_users: 0 } } }
})

const fetchStatus = async () => {
  const response = await fetch('/api/v1/status')
  status.value = await response.json()
}

const getTauClass = () => {
  const tau = status.value.health_metrics.tau
  return tau < 0.3 ? 'good' : tau < 0.6 ? 'warning' : 'danger'
}

const getPhiClass = () => {
  const phi = status.value.health_metrics.phi
  return phi > 0.8 ? 'good' : phi > 0.6 ? 'warning' : 'danger'
}

onMounted(() => {
  fetchStatus()
  // Refresh every 30 seconds
  setInterval(fetchStatus, 30000)
})
</script>
```

### React Hook for Hive Integration

```typescript
// useHiveStatus.ts
import { useState, useEffect } from 'react'

interface HiveStatus {
  health_metrics: {
    tau: number
    phi: number
    sigma: number
  }
  system_overview: {
    status: string
    uptime_seconds: number
  }
}

export const useHiveStatus = () => {
  const [status, setStatus] = useState<HiveStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch('/api/v1/status')
        if (!response.ok) throw new Error('Failed to fetch status')
        
        const data = await response.json()
        setStatus(data)
        setError(null)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 30000)
    
    return () => clearInterval(interval)
  }, [])

  return { status, loading, error }
}
```

## Error Handling Examples

### Robust API Client

```python
import requests
from typing import Optional, Dict, Any
import time

class HiveAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "HiveClient/1.0"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """Make HTTP request with error handling and retries."""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(3):  # 3 retry attempts
            try:
                response = self.session.request(method, url, **kwargs)
                
                if response.status_code == 429:  # Rate limited
                    wait_time = int(response.headers.get('Retry-After', 60))
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.ConnectionError:
                if attempt < 2:  # Don't sleep on last attempt
                    print(f"Connection failed. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                else:
                    print("Failed to connect to Hive after 3 attempts")
                    return None
            
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error: {e}")
                return None
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                return None
        
        return None
    
    def get_status(self) -> Optional[Dict[Any, Any]]:
        """Get system status with error handling."""
        return self._make_request("GET", "/api/v1/status")
    
    def send_message(self, text: str, sender_id: str, sender_name: str) -> bool:
        """Send message with error handling."""
        data = {
            "text": text,
            "sender_id": sender_id,
            "sender_name": sender_name
        }
        
        result = self._make_request("POST", "/api/v1/chat/message", json=data)
        return result is not None and result.get("success", False)

# Usage
client = HiveAPIClient()
status = client.get_status()

if status:
    print(f"Hive is {status['system_overview']['status']}")
else:
    print("Failed to get Hive status")
```

### WebSocket with Reconnection

```javascript
class HiveWebSocket {
  constructor(url, username) {
    this.url = url
    this.username = username
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.messageHandlers = new Map()
  }

  connect() {
    try {
      this.ws = new WebSocket(`${this.url}?username=${this.username}`)
      
      this.ws.onopen = () => {
        console.log('Connected to Hive')
        this.reconnectAttempts = 0
        this.onConnected?.()
      }
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          const handler = this.messageHandlers.get(data.type)
          if (handler) {
            handler(data)
          }
        } catch (error) {
          console.error('Failed to parse message:', error)
        }
      }
      
      this.ws.onclose = () => {
        console.log('Disconnected from Hive')
        this.attemptReconnect()
      }
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
    } catch (error) {
      console.error('Failed to connect:', error)
      this.attemptReconnect()
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)
      
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`)
      
      setTimeout(() => {
        this.connect()
      }, delay)
    } else {
      console.error('Max reconnection attempts reached')
      this.onMaxReconnectAttemptsReached?.()
    }
  }

  send(type, data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }))
      return true
    } else {
      console.warn('WebSocket not connected')
      return false
    }
  }

  onMessage(type, handler) {
    this.messageHandlers.set(type, handler)
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }
}

// Usage
const hiveWS = new HiveWebSocket('ws://localhost:8000/ws', 'Developer')

hiveWS.onMessage('message', (data) => {
  console.log(`${data.data.sender_name}: ${data.data.text}`)
})

hiveWS.onConnected = () => {
  hiveWS.send('message', { text: 'Hello, Hive!' })
}

hiveWS.connect()
```

## Testing Examples

### API Testing with pytest

```python
import pytest
import requests
from unittest.mock import patch

class TestHiveAPI:
    @pytest.fixture
    def api_client(self):
        return HiveAPIClient("http://localhost:8000")
    
    def test_get_status_success(self, api_client):
        """Test successful status retrieval."""
        status = api_client.get_status()
        
        assert status is not None
        assert "health_metrics" in status
        assert "system_overview" in status
        assert status["system_overview"]["status"] in ["active", "degraded"]
    
    def test_send_message_success(self, api_client):
        """Test successful message sending."""
        success = api_client.send_message(
            "Test message",
            "test_user",
            "Test User"
        )
        
        assert success is True
    
    @patch('requests.Session.request')
    def test_connection_error_handling(self, mock_request, api_client):
        """Test connection error handling."""
        mock_request.side_effect = requests.exceptions.ConnectionError()
        
        status = api_client.get_status()
        assert status is None
        assert mock_request.call_count == 3  # 3 retry attempts
```

### Frontend Component Testing

```typescript
// HiveStatus.test.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import HiveStatus from '@/components/HiveStatus.vue'

// Mock fetch
global.fetch = vi.fn()

describe('HiveStatus', () => {
  it('displays health metrics correctly', async () => {
    const mockStatus = {
      health_metrics: { tau: 0.25, phi: 0.85, sigma: 0.78 },
      components: { aggregates: { chat_system: { active_users: 5 } } }
    }
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockStatus
    })
    
    const wrapper = mount(HiveStatus)
    
    // Wait for async data loading
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))
    
    expect(wrapper.text()).toContain('0.25')
    expect(wrapper.text()).toContain('0.85')
    expect(wrapper.text()).toContain('5')
  })
  
  it('handles API errors gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'))
    
    const wrapper = mount(HiveStatus)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))
    
    expect(wrapper.text()).toContain('Error loading status')
  })
})
```

---

*"The simple believes everything, but the prudent gives thought to his steps." - Proverbs 14:15 (ESV)* 🐝✨