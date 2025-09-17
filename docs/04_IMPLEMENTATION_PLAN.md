# 04_IMPLEMENTATION_PLAN.md: Detailed Implementation Plan

## 1. Introduction

This document serves as the detailed blueprint for implementing the Hive Host architecture, incorporating the separate `p2pd` daemon for P2P communication. It moves from high-level architectural overview to low-level pseudo-code and a step-by-step coding plan.

## 2. High-Level Architecture Diagram

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
| | IPC Client (WebSockets)                        | |
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
| | p2pd Network Stack (asyncio event loop)        | |
| +------------------------------------------------+ |
| | IPC Server (WebSockets)                        | |
| +------------------------------------------------+ |
|                                                    |
+----------------------------------------------------+
```

## 3. Component Breakdown (High-Level)

*   **Hive Host:** The main executable. Responsibilities include: application lifecycle management, providing foundational services (Event Bus, Logger), loading and managing agents, running the FastAPI server (for frontend and API), and managing the lifecycle of the `P2P Daemon`.
*   **P2P Daemon:** A standalone Python process. Responsibilities include: running the `p2pd` node, handling all P2P communication (discovery, pub/sub), and exposing a WebSocket server for IPC with the Hive Host.
*   **Agents:** Self-contained modules (e.g., Python classes) that implement specific functionalities. They interact with the outside world and other agents through the Host's provided services (IPC client to P2P Daemon, Event Bus, Logger).

## 4. Inter-Process Communication (IPC) Details

*   **Mechanism:** WebSockets will be used for real-time, bidirectional communication between the Hive Host and the P2P Daemon.
*   **Message Format:** A simple JSON message format will be used for commands and data exchange.
    *   **Host to Daemon (Commands):** `{"type": "publish", "topic": "/chat", "message": "hello"}` or `{"type": "get_peer_id"}`
    *   **Daemon to Host (Events/Responses):** `{"type": "message_received", "topic": "/chat", "message": "hello"}` or `{"type": "peer_id_response", "peer_id": "Qm..."}`
*   **Client (Host side):** The Hive Host will establish a WebSocket connection to the P2P Daemon on startup and use it to send commands and receive events.
*   **Server (Daemon side):** The P2P Daemon will run a WebSocket server that listens for connections from the Hive Host. It will process commands and send back responses/events.

## 5. Foundational Services (Host-Provided)

These services will be initialized by the Hive Host and passed to each agent upon loading.

### 5.1. Async Event Bus

*   **Purpose:** For system-level notifications (e.g., `agent_loaded`, `host_shutdown`). Agents can subscribe to these events.
*   **Implementation:** A simple `asyncio.Queue` or `asyncio.Event` based system.
*   **Pseudo-code (Host):**
    ```python
    # host.py
    class HiveHost:
        def __init__(self):
            self.event_bus = asyncio.Queue()
            # ...

        async def publish_event(self, event_type: str, data: dict = None):
            await self.event_bus.put({"type": event_type, "data": data})

        async def _event_consumer(self):
            while True:
                event = await self.event_bus.get()
                # Process event (e.g., log, notify agents)
    ```
*   **Pseudo-code (Agent):**
    ```python
    # agents/base_agent.py
    class BaseAgent:
        def __init__(self, event_bus: asyncio.Queue, logger: logging.Logger, p2p_client: WebSocketClient):
            self.event_bus = event_bus
            self.logger = logger
            self.p2p_client = p2p_client
            asyncio.create_task(self._subscribe_to_events())

        async def _subscribe_to_events(self):
            while True:
                event = await self.event_bus.get()
                if event["type"] == "host_shutdown":
                    self.logger.info("Agent received host shutdown event.")
                    break
                # Handle other events
    ```

### 5.2. Structured Audit Logger

*   **Purpose:** For recording all significant actions and events in a machine-readable format.
*   **Implementation:** Python's standard `logging` module configured with a JSON formatter.
*   **Pseudo-code (Host):**
    ```python
    # host.py
    class HiveHost:
        def __init__(self):
            self.logger = self.setup_logger()
            # ...

        def setup_logger(self):
            logger = logging.getLogger("hive")
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler() # Or FileHandler, etc.
            formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "agent": "%(name)s"}')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            return logger
    ```
*   **Pseudo-code (Agent):**
    ```python
    # agents/base_agent.py
    class BaseAgent:
        def __init__(self, event_bus: asyncio.Queue, logger: logging.Logger, p2p_client: WebSocketClient):
            self.logger = logger
            # ...

        def do_something(self):
            self.logger.info("Agent performed an action.", extra={'action': 'some_action', 'data': {'key': 'value'}})
    ```

## 6. Agent Structure (Low-Level)

*   **Base `Agent` Class:** All agents will inherit from a common base class that provides access to the Host's foundational services (Event Bus, Logger, P2P IPC client).
*   **Loading and Initialization:** The Host will have a mechanism to discover and load agent modules. Each agent will have a `start()` and `stop()` method.

## 7. Refactoring the Chat Application into an Agent

*   The existing `chat.py` functionality will be moved into a `ChatAgent` class.
*   The `ChatAgent` will receive the Host's services (Event Bus, Logger, P2P IPC client).
*   It will use the P2P IPC client to send messages (publish to `p2pd`) and receive messages (subscribe to `p2pd` and forward to web clients).
*   The FastAPI routes for the chat UI and WebSockets will be managed by the `ChatAgent` or registered by the Host based on the agent's needs.

## 8. Step-by-Step Implementation Plan (Coding Tasks)

1.  **Implement Foundational Services:** Create the Async Event Bus and Structured Audit Logger within the `HiveHost` class.
2.  **Create `p2p_daemon.py`:** Implement the `p2pd` daemon with its WebSocket server for IPC.
3.  **Implement `HiveHost`:**
    *   Manage `p2p_daemon` lifecycle (`asyncio.subprocess`).
    *   Implement WebSocket client to `p2p_daemon`.
    *   Implement `get_system_status()` API endpoint (querying `p2p_daemon` via IPC).
4.  **Create Base `Agent` Class:** Define the common interface for agents.
5.  **Refactor `ChatAgent`:** Move existing chat logic into `ChatAgent`, integrating with Host services and P2P IPC.
6.  **Integrate `ChatAgent` with Host:** Load `ChatAgent` from `HiveHost`.
7.  **Implement Simple Management CLI:** Basic commands to interact with the Hive Host.
8.  **Bundle with PyInstaller:** Create the single executable binary.
