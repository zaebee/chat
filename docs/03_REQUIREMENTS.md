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

### **3. Functional Requirements Document (FRD) - Revision 5**

#### **3.1. System Architecture: The Hive Host & Agent Model (with Separate P2P Daemon)**

The architecture will be refactored into a **Hive Host** and **Agent** model. The main application binary is the "Host," and all functionality, including the chat application itself, will be implemented as loadable "Agents."

To resolve the `trio`/`asyncio` conflict, the `py-libp2p` node will run in a **separate process** as a dedicated daemon.

```
+----------------------------------------------------+
| Hive Host Binary (Living Application)              |
|                                                    |
| +------------------------------------------------+ |
| | FastAPI (serving Frontend & Agent Mgmt API)     | |
| +------------------------------------------------+ |
|         |                                          |
| +-------v----------------------------------------+ |
| | Foundational Services (Event Bus, Logger)      | |
| +------------------------------------------------+ |
|         |                                          |
| +-------v----------------------------------------+ |
| | IPC (WebSockets)                               | |
| +------------------------------------------------+ |
|                                                    |
| +-----------------+   +--------------------------+ |
| | Agent: Chat     |   | Agent: [Future Agent]    | |
| +-------+---------+   +--------------------------+ |
|                                                    |
+----------------------------------------------------+
         ^                                          ^
         |                                          |
         | (Manages Lifecycle)                      |
         |                                          |
         +------------------------------------------+
                                                    |
                                                    |
+----------------------------------------------------+
| P2P Daemon (Separate Process)                      |
|                                                    |
| +------------------------------------------------+ |
| | libp2p Network Stack (trio event loop)         | |
| +------------------------------------------------+ |
|                                                    |
+----------------------------------------------------+
```

*   **Component: Hive Host:** The main executable. Its primary responsibilities are to manage the application lifecycle, load and unload agents, and provide core services. It will also manage the lifecycle of the `P2P Daemon`.
*   **Component: Foundational Services:** The Host will provide a shared **Async Event Bus** and a **Structured Audit Logger** to all agents.
*   **Component: Agent:** A self-contained module that implements a specific piece of functionality. The existing chat application will be refactored into the first agent.
*   **Component: P2P Daemon:** A separate Python process running the `py-libp2p` node with its own `trio` event loop. It will communicate with the Hive Host via WebSockets.
*   **Component: FastAPI:** Serves the web frontend and the `/api/v1` endpoints.

#### **3.2. Implementation Plan (Version 1.0)**

1.  **Create the P2P Daemon:** Create a `p2p_daemon.py` script that runs the `py-libp2p` node and exposes a WebSocket server for IPC.
2.  **Create the Hive Host Runtime:** Create a main `host.py` that initializes the foundational services, manages the `p2p_daemon`'s lifecycle, and initializes the FastAPI server.
3.  **Refactor Chat into an Agent:** The existing code in `chat.py` will be refactored into a `ChatAgent` class that receives the foundational services and communicates with the `p2p_daemon` via the Host.
4.  **Implement Introspection & Management:** Implement the `/api/v1/status` endpoint and a simple CLI for the user to view the hive's status.

#### **3.3. Pseudo-code for the Hive Host & P2P Daemon**

```python
# p2p_daemon.py - NEW - Runs the libp2p node in a separate process

import trio
from libp2p.p2p_node import P2PNode
import websockets
import asyncio

async def p2p_daemon_main(websocket_port: int):
    node = P2PNode()
    await node.start() # Starts the trio event loop internally

    async def websocket_handler(websocket, path):
        # Handle messages from the Hive Host
        async for message in websocket:
            # Process message (e.g., publish to libp2p topic)
            await node.publish("/hive-chat/1.0.0", message)
            # Send response back to host if needed

    # Start WebSocket server for IPC
    async with websockets.serve(websocket_handler, "localhost", websocket_port):
        await asyncio.Future() # Run forever

if __name__ == "__main__":
    # This daemon runs its own trio event loop
    # It needs to be run with `trio.run()` or similar
    # For now, we'll assume it's started correctly
    trio.run(p2p_daemon_main, 5000) # Example port

# host.py - REVISED - Manages the P2P Daemon

import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
import websockets # For IPC client

# Assuming P2PNode is now managed by the daemon
# from libp2p.p2p_node import P2PNode
from agents.chat_agent import ChatAgent # New agent structure

class HiveHost:
    def __init__(self):
        self.p2p_daemon_process = None
        self.p2p_websocket_client = None
        self.event_bus = asyncio.Queue()
        self.logger = self.setup_logger()
        self.fastapi_app = FastAPI(lifespan=self.lifespan)

    def setup_logger(self):
        logger = logging.getLogger("hive")
        # ... configuration ...
        return logger

    async def lifespan(self, app: FastAPI):
        # On startup
        self.logger.info("Hive Host starting.")
        # Start the P2P Daemon process
        self.p2p_daemon_process = await asyncio.create_subprocess_exec(
            "python", "p2p_daemon.py", "--websocket-port", "5000", # Example port
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.logger.info(f"P2P Daemon started with PID: {self.p2p_daemon_process.pid}")

        # Connect to the P2P Daemon via WebSocket
        self.p2p_websocket_client = await websockets.connect("ws://localhost:5000")
        self.logger.info("Connected to P2P Daemon WebSocket.")

        self.load_default_agents()
        self.logger.info("Hive Host started.")
        yield
        # On shutdown
        self.logger.info("Hive Host shutting down.")
        if self.p2p_websocket_client:
            await self.p2p_websocket_client.close()
        if self.p2p_daemon_process:
            self.p2p_daemon_process.terminate()
            await self.p2p_daemon_process.wait()

    def load_default_agents(self):
        # Agents receive the host's core services and a way to talk to the p2p daemon
        chat_agent = ChatAgent(self.p2p_websocket_client, self.event_bus, self.logger)
        self.agents.append(chat_agent)
        chat_agent.start()

    def setup_api_routes(self):
        @self.fastapi_app.get("/api/v1/status")
        async def get_system_status():
            # Query daemon for p2p status
            await self.p2p_websocket_client.send("get_status")
            daemon_status = await self.p2p_websocket_client.recv()
            return { "status": "running", "agents": [agent.get_status() for agent in self.agents], "p2p_daemon": daemon_status }

host = HiveHost()
app = host.fastapi_app
```

#### **3.4. Debian Packaging Impact & Risks (Unchanged)**

Our decision to pivot to a self-contained binary (e.g., using PyInstaller) instead of a `.deb` package mitigates the risks identified in the P2P dependency analysis. This remains the correct path.

#### **3.5. Definition of Done (Revised for V1.0)**

*   The application is refactored into a `HiveHost` and `ChatAgent` architecture.
*   The `py-libp2p` node runs as a separate `P2P Daemon` process.
*   The Host provides a shared event bus and structured logger to all agents.
*   All chat messages are sent and received over the libp2p pub/sub topic (via IPC to the daemon).
*   The system's state is legible through the `/api/v1/status` endpoint.
*   A simple CLI exists for the user to view the hive's status.
*   The entire application can be bundled into a single executable binary.