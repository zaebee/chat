### **1. Business Requirements Document (BRD)**

#### **1.1. Project:** Hive Chat - The Decentralized Evolution

#### **1.2. Project Overview & Goal**

The primary goal of this initiative is to evolve the Hive Chat application from a centralized, server-dependent architecture to a resilient, decentralized communication platform. This evolution is the first practical step towards realizing the "Living Code" and "Hive" architectural principles, where the application itself becomes more sovereign and less reliant on single points of failure.

#### **1.3. Business Need**

In an increasingly centralized digital world, there is a growing need for communication tools that prioritize user sovereignty, privacy, and resilience. By decentralizing Hive Chat, we are not just adding a feature; we are making a statement about the kind of software we want to build. This serves the "business" of creating a more free and open internet.

#### **1.4. Success Metrics**

The success of this initiative will be measured by the following outcomes:
*   **Resilience:** The chat application can continue to function between connected peers even if a central bootstrap or discovery server is temporarily unavailable.
*   **Architectural Foundation:** The new architecture serves as a solid, extensible foundation for future decentralized features (e.g., decentralized identity, file storage).
*   **User Sovereignty:** Users have more control over their data and communication channels, reducing reliance on a single service provider.

---

### **2. Product Requirements Document (PRD)**

#### **2.1. Theme: The Hybrid P2P Model**

This phase focuses on implementing a hybrid P2P model. This approach provides a pragmatic bridge between the web-native world (browsers, WebSockets) and the p2p world (libp2p), allowing us to deliver decentralized features without requiring a complete rewrite of the frontend.

#### **2.2. User Stories**

*   **As a user,** I want to send and receive messages in real-time, knowing that my messages are being broadcast across a peer-to-peer network, making the system more robust.
*   **As a user,** I want my chat history to be loaded from my local database when I start the application, ensuring my data is persistent and under my control.
*   **As a developer,** I want the application to function as a hybrid system, where the web UI is served by a traditional server, but real-time messaging is handled by an underlying p2p network.

#### **2.3. Features**

| Feature ID | Feature Name | Description | Priority |
| :--- | :--- | :--- | :--- |
| P2P-01 | P2P Message Broadcasting | The backend will connect to a libp2p pub/sub topic. Messages sent by users will be published to this topic, and the backend will subscribe to receive messages from other peers. | Must-have |
| P2P-02 | FastAPI as a P2P Gateway | The existing FastAPI server will be maintained to serve the frontend application and act as a bridge between the browser's WebSocket connection and the backend's libp2p node. | Must-have |

#### **2.4. Out of Scope (for this iteration)**

*   Pure browser-to-p2p communication (i.e., removing the FastAPI gateway).
*   Decentralized Identity (DIDs). Users will still be identified by a simple username.
*   Advanced p2p features like direct, encrypted messaging between two peers. All messages will be public on the pub/sub topic for now.

---

### **3. Functional Requirements Document (FRD) - Revision 2**

#### **3.1. System Architecture: The Hybrid Model (Unchanged)**

The overall hybrid architecture remains the same.

```
+---------+      WebSocket      +----------------+      libp2p      +--------------+
| Browser | <-----------------> | FastAPI Server | <--------------> | libp2p Swarm |
+---------+                     +----------------+                  +--------------+
                                |  (p2p Gateway) |
                                +----------------+
```

*   **Component: Frontend:** Remains a single-page application served by FastAPI. No functional changes are required for this phase.
*   **Component: FastAPI Gateway:**
    *   Continues to serve the `index.html` and static files.
    *   Manages WebSocket connections from browser clients.
    *   Will instantiate and manage the lifecycle of a `Libp2pNode` object.
*   **Component: libp2p Node:**
    *   A Python object (`py-libp2p`) that will be initialized on application startup (via FastAPI's `lifespan` event).
    *   It will subscribe to a designated pub/sub topic (e.g., `/hive-chat/1.0.0`).
    *   It will have a callback function to process incoming messages from the p2p network.

#### **3.2. Data Flow: Human and AI Interaction**

The data flows are now expanded to include AI agents as first-class citizens.

*   **Human User Interaction:** (Unchanged) Messages flow from Browser -> WebSocket -> FastAPI -> P2P Swarm.
*   **AI Agent Interaction (New):**
    1.  An authenticated AI agent makes a `POST` request to a new `/api/v1/messages` endpoint.
    2.  The FastAPI server validates the request and creates a `Message` object.
    3.  The message is saved to the database and published to the P2P network.

#### **3.3. Implementation Pseudo-code (Revised)**

This pseudo-code illustrates how `chat.py` would be modified to integrate the libp2p node and expose an API for AI teammates.

```python
# chat.py - Revised High-Level Pseudo-code

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import init_db
from libp2p.p2p_node import P2PNode # Hypothetical import
from security import get_api_key # Hypothetical import for API security

# --- NEW: API for AI Teammates ---

class SystemStatus(BaseModel):
    service_status: str
    p2p_node_status: dict
    active_web_clients: int
    timestamp: str

@app.get("/api/v1/status", response_model=SystemStatus)
async def get_system_status():
    """
    Provides a structured status report for AI agents and monitoring tools.
    This endpoint is the embodiment of the Principle of Legibility.
    """
    return {
        "service_status": "running",
        "p2p_node_status": await p2p_node.get_status(), # Assumes p2p_node has this method
        "active_web_clients": len(manager.active_connections),
        "timestamp": datetime.now().isoformat(),
    }

@app.post("/api/v1/messages")
async def post_message_from_agent(message: Message, api_key: APIKey = Depends(get_api_key)):
    """
    Allows a trusted AI agent to post a message to the network.
    This endpoint embodies the Principle of API-First Interaction.
    """
    await manager.add_message(message)
    await p2p_node.publish("/hive-chat/1.0.0", message.model_dump_json())
    return {"status": "message published"}

# ... (the rest of the file, including the lifespan manager and websocket endpoint) ...
```

#### **3.4. Debian Packaging Impact & Risks (Unchanged)**

*   **Critical Dependency:** This architecture introduces a hard dependency on the `py-libp2p` library.
*   **Packaging Challenge:** `py-libp2p` has a large and complex dependency tree. The biggest challenge and risk for this project will be successfully mapping **all** of these Python dependencies to their corresponding `python3-*` Debian packages. A thorough dependency analysis is required before implementation.

#### **3.5. Definition of Done (Revised)**

*   The application functions as a hybrid P2P chat system.
*   The system's state is legible through the `/api/v1/status` endpoint.
*   An AI agent can post messages through the `/api/v1/messages` endpoint.
*   All new code is written in accordance with the `ARCHITECTURE_PRINCIPLES.md`.

#### **3.6. Agent Management API (Future - V2.0)**

As per the consultation with our AI teammate Eddy, the long-term vision is to evolve this application into a "Single-Node Hive." This will be the focus of Version 2.0, and the requirements will be expanded to include a full agent management API.

*   **Concept:** The application will expose a set of API endpoints for managing the lifecycle of other agents running within the same process.
*   **Endpoints (for V2.0):**
    *   `GET /api/v1/agents`: List all running agents.
    *   `POST /api/v1/agents`: Deploy a new agent (e.g., by providing a URL to its code).
    *   `GET /api/v1/agents/{agent_id}`: Get the status of a specific agent.
    *   `DELETE /api/v1/agents/{agent_id}`: Stop a running agent.