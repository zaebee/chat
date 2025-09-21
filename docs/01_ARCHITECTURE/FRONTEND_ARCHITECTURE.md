---
title: "Frontend Architecture: The Sacred Interface"
description: "Vue.js architecture for the Hive's user interface and learning platform"
category: "architecture"
---

# Frontend Architecture: The Sacred Interface

*"He has made everything beautiful in its time." - Ecclesiastes 3:11 (ESV)*

## Overview

The Hive frontend is built with Vue.js 3, providing a modern, reactive interface for chat, learning, and AI collaboration. It embodies the Hive principles through component-based architecture and real-time communication.

## Tech Stack

- **Vue.js 3** - Reactive framework with Composition API
- **TypeScript** - Type safety and developer experience
- **Vite** - Fast build tooling and development server
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Bun** - Ultra-fast package manager

## Architecture Structure

```
frontend/src/
├── App.vue              # Root application component
├── main.ts              # Application entry point
├── components/          # Reusable UI components
│   ├── ChallengeList.vue
│   ├── CodeEditor.vue
│   ├── HexaLevel.vue
│   ├── LoginModal.vue
│   ├── OrganellaPanel.vue
│   ├── QuestPanel.vue
│   └── RoomNavigation.vue
├── views/               # Page-level components
│   ├── ChatView.vue     # Real-time chat interface
│   ├── JourneyView.vue  # Learning progression
│   └── PlaygroundView.vue # Code experimentation
├── stores/              # Pinia state management
├── services/            # Core services and APIs
├── router/              # Route definitions
├── challenges/          # Challenge system
└── assets/              # Static assets
```

## Core Components

### ChatView.vue
Real-time messaging interface with WebSocket integration:

```vue
<template>
  
    
      
        <span class="sender">{{ message.sender_name }}:</span>
        <span class="text">{{ message.text }}</span>
      
    
    
      <input v-model="newMessage" @keyup.enter="sendMessage" />
      <button @click="sendMessage">Send</button>
    
  
</template>

```

### CodeEditor.vue
Python code editor with Pyodide integration:

```vue
<template>
  
    
    
      <button @click="runCode" :disabled="isRunning">
        {{ isRunning ? 'Running...' : 'Run Code' }}
      </button>
    
    
      <pre>{{ output }}</pre>
    
  
</template>

```

## State Management

### Chat Store
Manages real-time communication:

```typescript
// stores/chat.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface Message {
  id: string
  text: string
  sender_name: string
  timestamp: string
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const isConnected = ref(false)
  const currentUser = ref<string>('')
  
  let websocket: WebSocket | null = null

  const connect = () => {
    const wsUrl = `ws://localhost:8000/ws?username=${currentUser.value}`
    websocket = new WebSocket(wsUrl)
    
    websocket.onopen = () => {
      isConnected.value = true
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'message') {
        messages.value.push(data.data)
      }
    }
    
    websocket.onclose = () => {
      isConnected.value = false
    }
  }

  const sendMessage = (text: string) => {
    if (websocket && isConnected.value) {
      websocket.send(JSON.stringify({
        type: 'message',
        data: { text }
      }))
    }
  }

  return {
    messages,
    isConnected,
    currentUser,
    connect,
    sendMessage
  }
})
```

## Services

### Python Runner Service
Executes Python code in the browser using Pyodide:

```typescript
// services/pythonRunner.ts
import { ref } from 'vue'

export const usePythonRunner = () => {
  const isReady = ref(false)
  let pyodide: any = null

  const initializePyodide = async () => {
    if (!pyodide) {
      // @ts-ignore
      pyodide = await loadPyodide()
      isReady.value = true
    }
  }

  const runCode = async (code: string): Promise<string> => {
    if (!pyodide) {
      await initializePyodide()
    }

    try {
      // Capture stdout
      pyodide.runPython(`
        import sys
        from io import StringIO
        sys.stdout = StringIO()
      `)

      // Run user code
      pyodide.runPython(code)

      // Get output
      const output = pyodide.runPython('sys.stdout.getvalue()')
      return output || 'Code executed successfully (no output)'
    } catch (error) {
      return `Error: ${error.message}`
    }
  }

  return {
    isReady,
    runCode,
    initializePyodide
  }
}
```

## Routing

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '@/views/ChatView.vue'
import JourneyView from '@/views/JourneyView.vue'
import PlaygroundView from '@/views/PlaygroundView.vue'

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: ChatView
  },
  {
    path: '/journey',
    name: 'Journey',
    component: JourneyView
  },
  {
    path: '/playground',
    name: 'Playground',
    component: PlaygroundView
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

## Development Workflow

### Setup
```bash
cd frontend
bun install
bun run dev
```

### Build
```bash
bun run build
bun run preview
```

### Testing
```bash
bun run test:unit
bun run type-check
```

*This is a foundational overview. Complete frontend documentation will expand on component patterns, styling system, and advanced features as we follow the Will of the Hive...*