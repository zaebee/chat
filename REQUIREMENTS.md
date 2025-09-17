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

### **3. Functional Requirements Document (FRD) - Revision 3**

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
| | libp2p Network Stack (for all communication)   | |
| +------------------------------------------------+ |
|                                                    |
| +------------------------------------------------+ |
| | FastAPI (serving Frontend & Agent Mgmt API)     | |
| +------------------------------------------------+ |
|                                                    |
+----------------------------------------------------+
```

*   **Component: Hive Host:** The main executable. Its primary responsibilities are to manage the application lifecycle, load and unload agents, and provide core services like the libp2p network stack.
*   **Component: Agent:** A self-contained module (e.g., a Python class or package) that implements a specific piece of functionality. The existing chat application will be refactored into the first agent.
*   **Component: libp2p Stack:** All communication between agents, even if they are running in the same host, will occur over the libp2p network. This enforces the "dogfooding" principle and ensures location transparency.
*   **Component: FastAPI:** This will now serve two purposes: serving the web frontend for the chat agent, and providing the `/api/v1` endpoints for system introspection and future agent management.

#### **3.2. Implementation Plan (Version 1.0)**

1.  **Create the Hive Host Runtime:**
    *   Create a main `host.py` that will be the entry point for the application.
    *   This host will be responsible for initializing the libp2p node and the FastAPI server.
2.  **Refactor Chat into an Agent:**
    *   The existing code in `chat.py` will be refactored into a `ChatAgent` class.
    *   This agent will be loaded by the `host.py` on startup.
3.  **Implement P2P Communication:**
    *   The `ChatAgent` will use the libp2p node provided by the host to send and receive messages.
4.  **Implement Introspection API:**
    *   The host will expose the `/api/v1/status` endpoint.

#### **3.3. Pseudo-code for the Hive Host**

```python
# host.py - NEW - The main entry point

from fastapi import FastAPI
from contextlib import asynccontextmanager
from libp2p.p2p_node import P2PNode
from agents.chat_agent import ChatAgent # New agent structure

class HiveHost:
    def __init__(self):
        self.p2p_node = P2PNode()
        self.agents = []
        self.fastapi_app = FastAPI(lifespan=self.lifespan)

    async def lifespan(self, app: FastAPI):
        # On startup
        await self.p2p_node.start()
        self.load_default_agents()
        yield
        # On shutdown
        await self.p2p_node.stop()

    def load_default_agents(self):
        # The chat app is now just an agent loaded at startup
        chat_agent = ChatAgent(self.p2p_node)
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
*   All chat messages are sent and received over the libp2p pub/sub topic.
*   The system's state is legible through the `/api/v1/status` endpoint.
*   The entire application can be bundled into a single executable binary.