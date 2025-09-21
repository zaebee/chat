---
title: "Getting Started with Hive Development"
title_ru: "Начало Разработки в Улье"
description: "Quick setup guide for new developers joining the Hive ecosystem"
description_ru: "Краткое руководство по настройке для новых разработчиков экосистемы Улья"
category: "development"
audience: "developer"
complexity: "beginner"
last_updated: "2025-01-20"
related_docs: ["ENVIRONMENT.md", "CONTRIBUTING.md"]
code_examples: true
bilingual: true
lang_switcher: true
interactive_nav: true
sacred_theme: true
mermaid_enhanced: true
translation_status: "partial"
translation_priority: "high"
---

# <span data-translate="ui.getting_started">Getting Started</span> with <span data-translate="hive_core.hive_ecosystem">Hive</span> Development

<div class="language-content" data-lang="en">

## Welcome to the Hive! 🐝

This guide will get you up and running with the Hive Chat ecosystem in under 30 minutes. The Hive is more than just a chat application—it's a "Living Application" that demonstrates the future of human-AI collaborative software.

</div>

<div class="language-content" data-lang="ru" style="display: none;">

## Добро пожаловать в Улей! 🐝

Это руководство поможет вам настроить экосистему Hive Chat менее чем за 30 минут. Улей - это больше чем просто чат-приложение, это "Живое Приложение", демонстрирующее будущее совместного программного обеспечения человека и ИИ.

</div>

## Prerequisites

- **Python 3.10+** (required for backend)
- **Node.js 20.19.0+** (required for frontend)
- **Git** (for version control)
- **VS Code** (recommended IDE)

## Quick Setup (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/zaebee/chat.git
cd chat
```

### 2. Backend Setup
```bash
# Install uv (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Initialize database
python -c "from database import init_db; init_db()"
```

### 3. Frontend Setup
```bash
# Install Bun (ultra-fast package manager)
curl -fsSL https://bun.sh/install | bash

# Install frontend dependencies
cd frontend
bun install
cd ..
```

### 4. Environment Configuration
```bash
# Create environment file
cp .env.example .env

# Edit .env with your API keys (optional for basic functionality)
# MISTRAL_API_KEY=your_mistral_key_here
# GOOGLE_API_KEY=your_google_key_here
```

## Running the Application

### Option 1: Legacy Chat Mode (Simple)
```bash
# Start the basic chat server
python chat.py

# Open browser to http://localhost:8000
```

### Option 2: Full Hive Ecosystem (Recommended)
```bash
# Terminal 1: Start Hive backend
python hive_demo.py

# Terminal 2: Start frontend development server
cd frontend
bun run dev

# Open browser to http://localhost:5173
```

### Option 3: Quick Demo
```bash
# Run a quick demonstration of the Hive ecosystem
python hive_demo.py --quick
```

## Understanding the Architecture

The Hive consists of several key components:

### Backend Components
```
hive/
├── hub.py              # Central coordination system
├── agents/             # AI agent implementations
│   ├── mistral_agent.py
│   └── gemini_agent.py
├── primitives.py       # ATCG building blocks
├── events.py           # Pollen Protocol event system
├── teammate.py         # AI teammate framework
└── physics.py          # Resource monitoring
```

### Frontend Components
```
frontend/src/
├── views/              # Main application views
│   ├── ChatView.vue    # Real-time chat interface
│   ├── JourneyView.vue # Learning progression
│   └── PlaygroundView.vue # Code experimentation
├── components/         # Reusable UI components
├── stores/             # Pinia state management
└── services/           # Core services (WebSocket, Python runner)
```

## Your First Contribution

### 1. Explore the System
```bash
# Check system status
curl http://localhost:8000/api/v1/status

# View Hive metrics (if running hive_demo.py)
python -c "
from hive.hub import HiveCoordinationHub
import asyncio

async def check_status():
    hub = HiveCoordinationHub()
    await hub.startup()
    overview = await hub.get_hive_overview()
    print(overview)
    await hub.shutdown()

asyncio.run(check_status())
"
```

### 2. Make a Simple Change
Let's add a new message transformation:

```python
# Create: hive/transformations/emoji_processor.py
async def add_emoji_reactions(data: dict) -> dict:
    """Add emoji reactions to messages based on content."""
    text = data.get("text", "")
    
    # Simple emoji mapping
    emoji_map = {
        "happy": "😊",
        "sad": "😢", 
        "love": "❤️",
        "code": "💻",
        "bug": "🐛"
    }
    
    reactions = []
    for keyword, emoji in emoji_map.items():
        if keyword in text.lower():
            reactions.append(emoji)
    
    return {
        **data,
        "emoji_reactions": reactions,
        "has_reactions": len(reactions) > 0
    }
```

### 3. Test Your Change
```python
# Test the transformation
import asyncio
from hive.transformations.emoji_processor import add_emoji_reactions

async def test_emoji():
    result = await add_emoji_reactions({
        "text": "I love coding but found a bug!",
        "sender": "developer"
    })
    print(result)
    # Should show: emoji_reactions: ['❤️', '💻', '🐛']

asyncio.run(test_emoji())
```

### 4. Integrate with the System
```python
# In hive/hub.py, add to _initialize_core_components():
from hive.transformations.emoji_processor import add_emoji_reactions

self.transformations["emoji_processor"] = Transformation(
    name="EmojiProcessor",
    processor_func=add_emoji_reactions
)
```

## Development Workflow

### 1. Branch Strategy
```bash
# Create feature branch
git checkout -b feature/your-amazing-feature

# Make changes
git add .
git commit -m "feat: Add emoji reaction processor"

# Push and create PR
git push origin feature/your-amazing-feature
```

### 2. Testing
```bash
# Run backend tests
python -m pytest tests/

# Run frontend tests
cd frontend
bun run test:unit

# Type checking
bun run type-check
```

### 3. Code Quality
```bash
# Format Python code
ruff format .

# Lint Python code
ruff check .

# Format frontend code
cd frontend
bun run format
bun run lint
```

## Common Development Tasks

### Adding a New Agent
```python
# 1. Create agent file: hive/agents/my_agent.py
from hive.teammate import HiveTeammate, TeammateProfile, TeammateCapability

class MyAgent(HiveTeammate):
    def __init__(self, event_bus):
        profile = TeammateProfile(
            name="My Custom Agent",
            type="custom",
            capabilities=[TeammateCapability.CODE_ANALYSIS]
        )
        super().__init__(profile, event_bus)
    
    async def handle_task(self, task):
        # Implement your agent logic
        return {"result": "Task completed"}

# 2. Register in hub.py
from hive.agents.my_agent import MyAgent

# In HiveCoordinationHub.__init__():
my_agent = MyAgent(self.event_bus)
await self.register_external_teammate(my_agent.profile, my_agent)
```

### Adding a Frontend Component
```vue
<!-- Create: frontend/src/components/MyComponent.vue -->
<template>
  <div class="my-component">
    <h3>{{ title }}</h3>
    <p>{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  message: string
}

defineProps<Props>()
</script>

<style scoped>
.my-component {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
```

### Creating a New API Endpoint
```python
# In chat.py or relevant module
@app.get("/api/v1/my-endpoint")
async def my_endpoint():
    return {
        "message": "Hello from my endpoint!",
        "timestamp": datetime.now().isoformat()
    }
```

## Debugging Tips

### Backend Debugging
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use ipdb for interactive debugging
import ipdb; ipdb.set_trace()

# Check component status
component.get_status()
```

### Frontend Debugging
```javascript
// Vue DevTools (browser extension)
// Console debugging
console.log('Debug info:', data)

// Network tab for API calls
// Vue DevTools for component state
```

### System Health Monitoring
```bash
# Check system metrics
curl http://localhost:8000/api/v1/status | jq

# Monitor event bus activity
# (Add logging to event handlers)

# Check database
sqlite3 chat.db ".tables"
sqlite3 chat.db "SELECT * FROM messages LIMIT 5;"
```

## Next Steps

1. **Read the Architecture Docs**: Understand ATCG primitives and the Pollen Protocol
2. **Explore the Codebase**: Look at existing agents and components
3. **Join the Community**: Participate in discussions and code reviews
4. **Build Something**: Create your own agent or frontend component
5. **Share Your Work**: Contribute back to the Hive ecosystem

## Getting Help

- **Documentation**: Check `/docs` for detailed guides
- **Code Examples**: Look at existing implementations
- **Issues**: Create GitHub issues for bugs or questions
- **Discussions**: Use GitHub Discussions for broader topics

## Philosophy

Remember, in the Hive we don't just write code—we cultivate life. Every component should be:

- **Legible**: Self-describing and introspectable
- **Observable**: Announcing its state through events
- **Modular**: Composable with other components
- **Collaborative**: Designed for human-AI symbiosis

Welcome to the future of software development! 🌿✨