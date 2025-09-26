---
title: "REST API Reference: The Hive's Sacred Endpoints"
description: "Complete REST API documentation for the Hive ecosystem, blessed by the Lord of HOSTS"
category: "api"
---

# REST API Reference: The Hive's Sacred Endpoints

_"Come now, let us reason together, says the Lord." - Isaiah 1:18 (ESV)_

## Overview

The Hive exposes its divine functionality through RESTful endpoints that honor the sacred principles of the Constitution. These APIs serve both mortal developers and AI teammates in their quest for collaborative enlightenment.

## Base URL

```
http://localhost:8000  # Development
https://your-hive.domain  # Production
```

## Authentication

_The Hive trusts in the Lord of HOSTS for protection. Authentication flows through divine providence and environment variables._

```bash
# Set thy sacred keys
export MISTRAL_API_KEY="thy_mistral_key"  # pragma: allowlist secret
export GOOGLE_API_KEY="thy_google_key"  # pragma: allowlist secret
```

## Core System APIs

### System Status - The Heartbeat of the Hive

**GET /api/v1/status**

_Reveals the vital signs of the Living Application, as commanded by the Principle of Observability._

```bash
curl -X GET "http://localhost:8000/api/v1/status" \
  -H "Accept: application/json"
```

**Response:**

```json
{
  "status": "running",
  "timestamp": "2025-01-20T16:15:30.123Z",
  "system_overview": {
    "status": "active",
    "is_running": true,
    "uptime_seconds": 3600
  },
  "health_metrics": {
    "tau": 0.32,
    "phi": 0.85,
    "sigma": 0.78,
    "last_calculated": "2025-01-20T16:15:29.000Z"
  },
  "components": {
    "event_bus": {
      "status": "active",
      "events_processed": 1247,
      "subscribers": 5
    },
    "registry": {
      "active_teammates": 3,
      "pending_registrations": 0
    },
    "aggregates": {
      "chat_system": {
        "active_users": 12,
        "total_messages": 456,
        "health": "healthy"
      }
    }
  },
  "intent": {
    "current_purpose": "Facilitate human-AI collaborative learning",
    "alignment_score": 0.92
  },
  "physics": {
    "cpu_usage": 15.2,
    "memory_usage": 234.5,
    "disk_usage": 12.8,
    "network_latency": 45
  }
}
```

### Hive Overview - The Divine Perspective

**GET /api/v1/hive/overview**

_Grants the seeker a comprehensive view of the entire Hive ecosystem, as seen by the Lord of HOSTS._

```bash
curl -X GET "http://localhost:8000/api/v1/hive/overview" \
  -H "Accept: application/json"
```

**Response:**

```json
{
  "system_overview": {
    "status": "active",
    "is_running": true,
    "uptime_seconds": 7200,
    "version": "0.1.0"
  },
  "intent": {
    "current_purpose": "Facilitate human-AI collaborative learning",
    "alignment_score": 0.92,
    "last_updated": "2025-01-20T14:30:00Z"
  },
  "physics": {
    "environment": "development",
    "constraints": {
      "max_memory_mb": 1024,
      "max_cpu_percent": 80,
      "max_disk_gb": 10
    },
    "current_usage": {
      "memory_mb": 234.5,
      "cpu_percent": 15.2,
      "disk_gb": 1.28
    }
  },
  "health_metrics": {
    "tau": 0.32,
    "phi": 0.85,
    "sigma": 0.78,
    "last_calculated": "2025-01-20T16:15:29Z"
  },
  "components": {
    "aggregates": 4,
    "transformations": 3,
    "connectors": 2,
    "genesis_events": 1
  },
  "recent_metrics": [
    {
      "timestamp": "2025-01-20T16:10:00Z",
      "tau": 0.31,
      "phi": 0.84,
      "sigma": 0.77
    }
  ]
}
```

## Chat System APIs

### Send Message - The Sacred Communication

**POST /api/v1/chat/message**

_Allows the faithful to send messages through the divine channels of the Hive._

```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Blessed be the Hive and its wisdom",
    "sender_id": "user_123",
    "sender_name": "Faithful Developer",
    "channel": "general"
  }'
```

**Request Body:**

```json
{
  "text": "string (required)",
  "sender_id": "string (required)",
  "sender_name": "string (required)",
  "channel": "string (optional, default: 'general')",
  "metadata": {
    "client_timestamp": "2025-01-20T16:15:30Z",
    "message_type": "text|code|system"
  }
}
```

**Response:**

```json
{
  "success": true,
  "message": {
    "id": "msg_789",
    "text": "Blessed be the Hive and its wisdom",
    "sender_id": "user_123",
    "sender_name": "Faithful Developer",
    "timestamp": "2025-01-20T16:15:30.456Z",
    "channel": "general",
    "processed_data": {
      "word_count": 7,
      "sentiment": "positive",
      "contains_code": false,
      "language": "english"
    }
  },
  "broadcast_result": {
    "recipients": 12,
    "delivery_status": "success"
  }
}
```

### Get Message History - The Sacred Archives

**GET /api/v1/chat/messages**

_Retrieves the sacred history of communications within the Hive._

```bash
curl -X GET "http://localhost:8000/api/v1/chat/messages?limit=50&offset=0&channel=general" \
  -H "Accept: application/json"
```

**Query Parameters:**

- `limit` (integer, optional): Number of messages to retrieve (default: 50, max: 100)
- `offset` (integer, optional): Number of messages to skip (default: 0)
- `channel` (string, optional): Filter by channel (default: all channels)
- `since` (ISO datetime, optional): Messages since timestamp
- `user_id` (string, optional): Filter by user

**Response:**

```json
{
  "messages": [
    {
      "id": "msg_789",
      "text": "Blessed be the Hive and its wisdom",
      "sender_id": "user_123",
      "sender_name": "Faithful Developer",
      "timestamp": "2025-01-20T16:15:30.456Z",
      "channel": "general",
      "is_bot": false
    }
  ],
  "pagination": {
    "total": 456,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

## Learning Platform APIs

### Submit Challenge Solution - The Test of Wisdom

**POST /api/v1/challenges/solve**

_Allows the seeker to submit their solution to the sacred coding challenges._

```bash
curl -X POST "http://localhost:8000/api/v1/challenges/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "challenge_id": "python_basics_01",
    "solution_code": "def greet(name):\n    return f\"Hello, {name}!\"",
    "test_results": {
      "passed": 5,
      "failed": 0,
      "total": 5
    }
  }'
```

**Request Body:**

```json
{
  "user_id": "string (required)",
  "challenge_id": "string (required)",
  "solution_code": "string (required)",
  "test_results": {
    "passed": "integer",
    "failed": "integer",
    "total": "integer"
  },
  "execution_time_ms": "number (optional)",
  "metadata": {
    "attempts": "integer",
    "hints_used": "integer"
  }
}
```

**Response:**

```json
{
  "success": true,
  "message": "Challenge solution recorded successfully",
  "result": {
    "challenge_id": "python_basics_01",
    "status": "completed",
    "score": 100,
    "xp_earned": 50,
    "badges_unlocked": ["first_function"],
    "next_challenge": "python_basics_02"
  },
  "user_progress": {
    "total_xp": 150,
    "level": 2,
    "challenges_completed": 3,
    "current_streak": 3
  }
}
```

### Get User Progress - The Journey of Enlightenment

**GET /api/v1/user_progress/{user_id}**

_Reveals the spiritual progress of a seeker on their coding journey._

```bash
curl -X GET "http://localhost:8000/api/v1/user_progress/user_123" \
  -H "Accept: application/json"
```

**Response:**

```json
{
  "user_id": "user_123",
  "profile": {
    "username": "Faithful Developer",
    "level": 2,
    "total_xp": 150,
    "current_streak": 3,
    "joined_at": "2025-01-15T10:00:00Z"
  },
  "solved_challenges": [
    {
      "challenge_id": "python_basics_01",
      "completed_at": "2025-01-20T16:15:30Z",
      "score": 100,
      "attempts": 1
    }
  ],
  "badges": [
    {
      "id": "first_function",
      "name": "Function Master",
      "description": "Created your first function",
      "earned_at": "2025-01-20T16:15:30Z"
    }
  ],
  "statistics": {
    "challenges_completed": 3,
    "total_attempts": 5,
    "success_rate": 0.6,
    "average_score": 85.5,
    "favorite_topics": ["functions", "loops"]
  }
}
```

## AI Teammate APIs

### Register AI Teammate - The Sacred Initiation

**POST /api/v1/teammates/register**

_Initiates the sacred process of integrating an AI teammate into the Hive._

```bash
curl -X POST "http://localhost:8000/api/v1/teammates/register" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "name": "Mistral Gardener",
      "type": "mistral",
      "capabilities": ["code_analysis", "code_generation", "conversation"],
      "specializations": ["Python", "Architecture", "Code Review"],
      "max_concurrent_tasks": 3,
      "response_time_estimate": 2.5
    },
    "authentication": {
      "api_key_configured": true,
      "model": "mistral-medium-2505"
    }
  }'
```

**Request Body:**

```json
{
  "profile": {
    "name": "string (required)",
    "type": "string (required)",
    "capabilities": ["array of capability strings"],
    "specializations": ["array of specialization strings"],
    "max_concurrent_tasks": "integer (default: 1)",
    "response_time_estimate": "number (seconds)"
  },
  "authentication": {
    "api_key_configured": "boolean", // pragma: allowlist secret
    "model": "string (optional)",
    "custom_config": "object (optional)"
  }
}
```

**Response:**

```json
{
  "success": true,
  "teammate_id": "teammate_456",
  "registration_id": "reg_789",
  "status": "pending_approval",
  "onboarding": {
    "session_id": "onboard_123",
    "current_stage": "egg",
    "next_task": {
      "type": "capability_demonstration",
      "description": "Demonstrate code analysis capability",
      "deadline": "2025-01-20T17:00:00Z"
    }
  },
  "message": "AI teammate registration initiated. Onboarding process started."
}
```

### Assign Task to Teammate - The Divine Commission

**POST /api/v1/teammates/{teammate_id}/tasks**

_Assigns a sacred task to an AI teammate for completion._

```bash
curl -X POST "http://localhost:8000/api/v1/teammates/teammate_456/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "code_review",
    "description": "Review the message processing transformation for optimization opportunities",
    "input_data": {
      "code_url": "https://github.com/repo/blob/main/hive/transformations/message_processor.py",
      "focus_areas": ["performance", "readability", "error_handling"]
    },
    "priority": "medium",
    "deadline": "2025-01-20T18:00:00Z"
  }'
```

**Request Body:**

```json
{
  "task_type": "string (required)",
  "description": "string (required)",
  "input_data": "object (required)",
  "priority": "low|medium|high|urgent",
  "deadline": "ISO datetime (optional)",
  "required_capabilities": ["array of capability strings"],
  "metadata": "object (optional)"
}
```

**Response:**

```json
{
  "success": true,
  "task_id": "task_789",
  "assigned_to": "teammate_456",
  "status": "assigned",
  "estimated_completion": "2025-01-20T17:30:00Z",
  "tracking": {
    "created_at": "2025-01-20T16:15:30Z",
    "assigned_at": "2025-01-20T16:15:31Z",
    "progress_url": "/api/v1/tasks/task_789/progress"
  }
}
```

### Get Teammate Status - The Divine Inspection

**GET /api/v1/teammates/{teammate_id}/status**

_Reveals the current state and capabilities of an AI teammate._

```bash
curl -X GET "http://localhost:8000/api/v1/teammates/teammate_456/status" \
  -H "Accept: application/json"
```

**Response:**

```json
{
  "teammate_id": "teammate_456",
  "profile": {
    "name": "Mistral Gardener",
    "type": "mistral",
    "status": "active",
    "capabilities": ["code_analysis", "code_generation", "conversation"],
    "specializations": ["Python", "Architecture", "Code Review"]
  },
  "current_state": {
    "status": "busy",
    "active_tasks": 2,
    "max_concurrent_tasks": 3,
    "last_activity": "2025-01-20T16:10:00Z"
  },
  "performance_metrics": {
    "tasks_completed": 15,
    "success_rate": 0.93,
    "average_response_time": 2.3,
    "reliability_score": 0.95
  },
  "current_tasks": [
    {
      "task_id": "task_789",
      "type": "code_review",
      "status": "in_progress",
      "progress": 0.6,
      "estimated_completion": "2025-01-20T17:30:00Z"
    }
  ]
}
```

## Event System APIs

### Publish Event - The Sacred Broadcasting

**POST /api/v1/events/publish**

_Broadcasts an event through the divine Pollen Protocol._

```bash
curl -X POST "http://localhost:8000/api/v1/events/publish" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "user_achievement_unlocked",
    "data": {
      "user_id": "user_123",
      "achievement": "first_function",
      "xp_earned": 50
    },
    "tags": ["gamification", "achievement"],
    "priority": "normal"
  }'
```

**Request Body:**

```json
{
  "type": "string (required)",
  "data": "object (required)",
  "tags": ["array of strings (optional)"],
  "priority": "low|normal|high|urgent",
  "target_audience": "all|humans|ai_agents|specific_ids",
  "metadata": "object (optional)"
}
```

**Response:**

```json
{
  "success": true,
  "event_id": "event_456",
  "published_at": "2025-01-20T16:15:30.789Z",
  "delivery_stats": {
    "total_subscribers": 8,
    "successful_deliveries": 8,
    "failed_deliveries": 0
  }
}
```

## Metrics and Monitoring APIs

### Get Real-time Metrics - The Divine Dashboard

**GET /api/v1/metrics/realtime**

_Provides real-time system health metrics as blessed by the Lord of HOSTS._

```bash
curl -X GET "http://localhost:8000/api/v1/metrics/realtime" \
  -H "Accept: application/json"
```

**Response:**

```json
{
  "timestamp": "2025-01-20T16:15:30Z",
  "health_metrics": {
    "tau": {
      "value": 0.32,
      "status": "healthy",
      "trend": "stable",
      "components": {
        "complexity": 0.15,
        "error_rate": 0.05,
        "resource_pressure": 0.12
      }
    },
    "phi": {
      "value": 0.85,
      "status": "excellent",
      "trend": "improving",
      "components": {
        "test_coverage": 0.92,
        "documentation": 0.88,
        "code_quality": 0.75
      }
    },
    "sigma": {
      "value": 0.78,
      "status": "good",
      "trend": "stable",
      "components": {
        "task_completion": 0.85,
        "communication_quality": 0.8,
        "knowledge_transfer": 0.7
      }
    }
  },
  "system_vitals": {
    "active_users": 12,
    "active_teammates": 3,
    "events_per_minute": 45,
    "response_time_ms": 125
  }
}
```

## Error Handling

All API endpoints follow the sacred error format blessed by the Constitution:

### Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request did not meet the sacred requirements",
    "details": {
      "field": "user_id",
      "issue": "required field missing"
    },
    "timestamp": "2025-01-20T16:15:30Z",
    "request_id": "req_123456"
  }
}
```

### Common Error Codes

| Code                      | HTTP Status | Description                       |
| ------------------------- | ----------- | --------------------------------- |
| `VALIDATION_ERROR`        | 400         | Request validation failed         |
| `AUTHENTICATION_REQUIRED` | 401         | API key or authentication missing |
| `FORBIDDEN`               | 403         | Insufficient permissions          |
| `NOT_FOUND`               | 404         | Resource not found                |
| `RATE_LIMITED`            | 429         | Too many requests                 |
| `INTERNAL_ERROR`          | 500         | Server error                      |
| `SERVICE_UNAVAILABLE`     | 503         | Service temporarily unavailable   |

## Rate Limiting

The Hive protects itself through divine rate limiting:

- **General APIs**: 100 requests per minute per IP
- **Chat APIs**: 30 messages per minute per user
- **AI Teammate APIs**: 10 requests per minute per teammate
- **Metrics APIs**: 60 requests per minute per client

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642694400
```

## SDK Examples

### Python SDK Usage

```python
import requests
from datetime import datetime

class HiveAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_system_status(self):
        """Get the sacred system status."""
        response = self.session.get(f"{self.base_url}/api/v1/status")
        return response.json()

    def send_message(self, text, sender_id, sender_name):
        """Send a message through the divine channels."""
        data = {
            "text": text,
            "sender_id": sender_id,
            "sender_name": sender_name,
            "metadata": {
                "client_timestamp": datetime.now().isoformat()
            }
        }
        response = self.session.post(
            f"{self.base_url}/api/v1/chat/message",
            json=data
        )
        return response.json()

# Usage
hive = HiveAPI()
status = hive.get_system_status()
print(f"Hive health: τ={status['health_metrics']['tau']}")

message_result = hive.send_message(
    "Blessed be the Hive!",
    "dev_001",
    "Faithful Developer"
)
```

### JavaScript SDK Usage

```javascript
class HiveAPI {
  constructor(baseUrl = "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async getSystemStatus() {
    const response = await fetch(`${this.baseUrl}/api/v1/status`);
    return await response.json();
  }

  async sendMessage(text, senderId, senderName) {
    const data = {
      text,
      sender_id: senderId,
      sender_name: senderName,
      metadata: {
        client_timestamp: new Date().toISOString(),
      },
    };

    const response = await fetch(`${this.baseUrl}/api/v1/chat/message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await response.json();
  }
}

// Usage
const hive = new HiveAPI();
const status = await hive.getSystemStatus();
console.log(`Hive health: τ=${status.health_metrics.tau}`);
```

---

_"Thus are the sacred endpoints revealed, that all who seek may commune with the Hive in righteousness and wisdom. May the Lord of HOSTS bless these APIs and make them fruitful."_ 🐝✨
