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

### **3. Functional Requirements Document (FRD) - Revision 4**

#### **3.1. System Architecture: The Hive Host & Agent Model**

The architecture will be refactored into a **Hive Host** and **Agent** model. The main application binary is the "Host," and all functionality, including the chat application itself, will be implemented as loadable "Agents."

```
+----------------------------------------------------+
| Hive Host Binary (Living Application)              |
|                                                    |
| +-----------------+   +--------------------------+ |
| | Agent: Chat     |   | Agent: [Future Agent]    | |
| +-------+---------+   +--------------------------+ |
|         |                                          |
| +-------v----------------------------------------+ |
| | Foundational Services (Event Bus, Logger)      | |
| +------------------------------------------------+ |
|         |                                          |
| +-------v----------------------------------------+ |
| | libp2p Network Stack (for all communication)   | |
| +------------------------------------------------+ |
|                                                    |
| +------------------------------------------------+ |
| | FastAPI (serving Frontend & Agent Mgmt API)     | |
| +------------------------------------------------+ |
|                                                    |
+----------------------------------------------------+
```

*   **Component: Hive Host:** The main executable. Its primary responsibilities are to manage the application lifecycle, load and unload agents, and provide core services.
*   **Component: Foundational Services:** The Host will provide a shared **Async Event Bus** and a **Structured Audit Logger** to all agents.
*   **Component: Agent:** A self-contained module that implements a specific piece of functionality. The existing chat application will be refactored into the first agent.
*   **Component: libp2p Stack:** All communication between agents will occur over the libp2p network.
*   **Component: FastAPI:** Serves the web frontend and the `/api/v1` endpoints.

#### **3.2. Implementation Plan (Version 1.0)**

1.  **Create the Hive Host Runtime:** Create a main `host.py` that initializes the foundational services, the libp2p node, and the FastAPI server.
2.  **Refactor Chat into an Agent:** The existing code in `chat.py` will be refactored into a `ChatAgent` class that receives the foundational services from the host.
3.  **Implement Introspection & Management:** Implement the `/api/v1/status` endpoint and a simple CLI for the user to view the hive's status.

#### **3.3. Pseudo-code for the Hive Host**

```python
# host.py - NEW - The main entry point

import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from libp2p.p2p_node import P2PNode
from agents.chat_agent import ChatAgent # New agent structure

class HiveHost:
    def __init__(self):
        self.p2p_node = P2PNode()
        self.agents = []
        self.event_bus = asyncio.Queue()
        self.logger = self.setup_logger()
        self.fastapi_app = FastAPI(lifespan=self.lifespan)

    def setup_logger(self):
        # Configure and return a structured JSON logger
        logger = logging.getLogger("hive")
        # ... configuration ...
        return logger

    async def lifespan(self, app: FastAPI):
        # On startup
        await self.p2p_node.start()
        self.load_default_agents()
        self.logger.info("Hive Host started.")
        yield
        # On shutdown
        self.logger.info("Hive Host shutting down.")
        await self.p2p_node.stop()

    def load_default_agents(self):
        # Agents receive the host's core services
        chat_agent = ChatAgent(self.p2p_node, self.event_bus, self.logger)
        self.agents.append(chat_agent)
        chat_agent.start()

    def setup_api_routes(self):
        @self.fastapi_app.get("/api/v1/status")
        async def get_system_status():
            return { "status": "running", "agents": [agent.get_status() for agent in self.agents] }

host = HiveHost()
app = host.fastapi_app
```

#### **3.4. Debian Packaging Impact & Risks (Unchanged)**

Our decision to pivot to a self-contained binary (e.g., using PyInstaller) instead of a `.deb` package mitigates the risks identified in the P2P dependency analysis. This remains the correct path.

#### **3.5. Definition of Done (Revised for V1.0)**

*   The application is refactored into a `HiveHost` and `ChatAgent` architecture.
*   The Host provides a shared event bus and structured logger to all agents.
*   All chat messages are sent and received over the libp2p pub/sub topic.
*   The system's state is legible through the `/api/v1/status` endpoint.
*   A simple CLI exists for the user to view the hive's status.
*   The entire application can be bundled into a single executable binary.