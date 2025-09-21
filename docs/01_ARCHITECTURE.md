# 01_ARCHITECTURE.md: Hive Chat Architecture

This document outlines the core architectural principles and the technical decisions made for the Hive Chat application.

## 1. Hive Chat Architectural Principles

This section outlines the core principles that guide the development and architecture of the Hive Chat application. These principles are designed to create a system that is resilient, sovereign, and a collaborative environment for both human and AI teammates.

### 1.1. Principle of Legibility: The Code Must Be Self-Describing

An AI teammate should be able to understand the purpose and state of any component without having to read the source code.

- **Implementation:** We will create a standardized, machine-readable API for introspection. Every major component (e.g., the P2P node, the connection manager) will have a `get_status()` method that returns a structured JSON object.

### 1.2. Principle of Observability: The System Must Announce Its State

The application should not just log for humans; it should emit structured events for AI teammates.

- **Implementation:** We will establish a system-wide event bus or a set of well-defined API endpoints for querying real-time status and metrics.

### 1.3. Principle of Modularity: The System Must Be Composable

The application should be composed of loosely coupled modules with well-defined interfaces.

- **Implementation:** This allows an AI to reason about, test, and even replace individual components without destabilizing the entire system. Our current separation of `chat.py`, `database.py`, and the future `p2p.py` aligns with this.

### 1.4. Principle of API-First Interaction: Actions Should Be Programmatic

All core functionalities of the application should be accessible through a secure, versioned API, not just through a user interface.

- **Implementation:** An AI teammate should be able to send messages, query users, and manage the system through RESTful API calls.

### 1.5. Principle of Human-AI Symbiosis: Build for Teammates

We recognize that the development and operation of this software will be a collaboration between humans and AI agents. The system should be designed to be a friendly and productive environment for both.

- **Implementation:** Documentation, APIs, and even commit messages should be written with both a human and an AI audience in mind. The system should be designed to be not just "user-friendly," but "teammate-friendly."

## 2. P2P Layer Decision: From Python Libraries to External Daemon

This section documents the decision to pivot from Python-based P2P libraries to an external P2P daemon.

### 2.1. Problem with Python P2P Libraries (`py-libp2p` and `p2pd`)

<<<<<<< HEAD
- **Artifact:** The application will be distributed as a single, self-contained executable binary (e.g., created with PyInstaller).
- **Rationale:** This approach completely mitigates the risks associated with the complex and unavailable dependencies of `py-libp2p` in the Debian ecosystem. It gives us the freedom to choose our dependencies without being constrained by platform-specific packaging.
- **Implementation:** The binary will bundle the Python interpreter, all necessary libraries, and the application code itself.
=======
Despite extensive efforts, both `py-libp2p` and `p2pd` presented persistent and low-level integration challenges (e.g., `trio`/`asyncio` conflicts, unstable APIs, unclear documentation). These issues consumed excessive 'attention resources' (Σ) and introduced high 'system tension' (τ), hindering progress on core 'Hive Host' and 'Agent' development.
>>>>>>> main

### 2.2. Solution: Pivot to `go-libp2p-daemon` with Separate Process Architecture

To resolve these issues, we have decided to:

<<<<<<< HEAD
- **Hive Host:** The core executable responsible for providing foundational services (P2P networking, event bus, logging) and managing the agent lifecycle.
- **Agents:** Modular, self-contained components that implement specific features. The chat functionality itself will be our first agent.
- **Communication:** All inter-agent communication will occur over the libp2p network stack, even between agents running in the same host process.

### 2.3. Current Agents and Services

As of the current implementation, the system consists of two primary agents:

- **Backend Agent (`chat.py`):**
  - **Role:** Serves as the primary backend service and a basic Hive Host.
  - **Functionality:** Manages WebSocket connections, broadcasts messages, and persists chat history to a SQLite database.
  - **Technology:** FastAPI (Python).

- **Frontend Agent (`/frontend`):**
  - **Role:** Provides the user interface and all client-side application logic.
  - **Functionality:** Renders the chat interface, login flow, and the Python Learning Playground. Manages its own state via Pinia stores.
  - **Key Services within the Agent:**
    - `pythonRunner.ts`: A crucial service that provides a secure, sandboxed Python execution environment by integrating with the Pyodide (Wasm) runtime. This allows for safe, client-side execution of user-submitted code.
    - `chat.ts` (Pinia Store): Manages all real-time state for the application, including the WebSocket connection, messages, user lists, and UI preferences (theme, language).
  - **Technology:** Vue.js 3 (Vite), TypeScript, Pinia.
=======
1.  **Abandon direct Python P2P library implementation** due to instability and integration challenges.
2.  **Pivot to `go-libp2p-daemon`** (or a similar mature external daemon) as the P2P communication layer. This leverages a battle-tested, stable, and performant implementation.
3.  Implement a **Separate Process Architecture** for the P2P node. The `go-libp2p-daemon` will run in a dedicated process, completely isolating its event loop from the FastAPI host.
>>>>>>> main

### 2.3. Inter-Process Communication (IPC)

Communication between the FastAPI host and the `go-libp2p-daemon` will occur via its well-defined API (likely HTTP/WebSockets/gRPC). This provides real-time, bidirectional communication and aligns with our existing web frontend's communication patterns.

### 2.4. Lifecycle Management

The FastAPI host will manage the `go-libp2p-daemon`'s lifecycle using `asyncio.subprocess`.

### 2.5. Impact on Project

<<<<<<< HEAD
The primary reasons for this conclusion are:

- **Multiple Blocking Dependencies:** Several of `py-libp2p`'s core dependencies are not available in the official Debian repositories.
- **Git Dependency:** `py-libp2p` depends on a specific git commit of the `multiaddr` library, a practice that is incompatible with standard Debian packaging policies.
- **Packaging Cascade:** Each unavailable dependency would need to be packaged first, and each of those may have its own complex dependency tree, leading to a "packaging cascade" of ever-increasing work.
=======
This pivot is a pragmatic decision that unblocks our progress and aligns with our architectural principles. It requires replacing the `p2p_daemon.py` file with a script that manages the external daemon and updating `pyproject.toml`.
>>>>>>> main

## 3. Exploring the Concept of a "Self-Owned P2P Library"

This section summarizes the team's discussion on the concept of a "self-owned P2P library" and its implications for our project.

<<<<<<< HEAD
| Dependency       | Version      | Debian Package           | Status           | Verdict                 |
| :--------------- | :----------- | :----------------------- | :--------------- | :---------------------- |
| `aioquic`        | `>=1.2.0`    | `python3-aioquic`        | Available        | **Available**           |
| `base58`         | `>=1.0.3`    | `python3-base58`         | Available        | **Available**           |
| `coincurve`      | `==21.0.0`   | `python3-coincurve`      | "in preparation" | **Unavailable/Blocker** |
| `exceptiongroup` | `>=1.2.0`    | `python3-exceptiongroup` | Available        | **Available**           |
| `fastecdsa`      | `==2.3.2`    | `python3-fastecdsa`      | Not available    | **Unavailable/Blocker** |
| `grpcio`         | `>=1.41.0`   | `python3-grpcio`         | Available        | **Available**           |
| `lru-dict`       | `>=1.1.6`    | `python3-lru-dict`       | Available        | **Available**           |
| `multiaddr`      | `git commit` | `python3-multiaddr`      | Not available    | **Unavailable/Blocker** |
| `mypy-protobuf`  | `>=3.0.0`    | `python3-mypy-protobuf`  | Available        | **Available**           |
| `noiseprotocol`  | `>=0.3.0`    | `python3-noiseprotocol`  | Available        | **Available**           |
| `protobuf`       | `>=4.25.0`   | `python3-protobuf`       | Available        | **Available**           |
| `pycryptodome`   | `>=3.9.2`    | `python3-pycryptodome`   | Available        | **Available**           |
| `pymultihash`    | `>=0.8.2`    | `python3-pymultihash`    | Not available    | **Unavailable/Blocker** |
| `pynacl`         | `>=1.3.0`    | `python3-nacl`           | Available        | **Available**           |
| `rpcudp`         | `>=3.0.0`    | `python3-rpcudp`         | Not available    | **Unavailable/Blocker** |
| `trio-typing`    | `>=0.0.4`    | `python3-trio-typing`    | Not available    | **Unavailable/Blocker** |
| `trio`           | `>=0.26.0`   | `python3-trio`           | Available        | **Available**           |
| `zeroconf`       | `>=0.147.0`  | `python3-zeroconf`       | Available        | **Available**           |
=======
### 3.1. Visionary Goal

The ultimate vision is a P2P library that is highly autonomous, self-optimizing, self-healing, and network-governed. It should be a digital organism that can adapt and evolve based on the needs of the network, not just the whims of a few developers.

### 3.2. Pragmatic Implementation

While the idea of a library rewriting its own code is beyond current capabilities and introduces unacceptable risks, we can build towards the "self-owned" vision by focusing on:

*   **Configurability:** The library's behavior can be extensively customized at runtime.
*   **Extensibility:** It supports a robust plugin architecture, allowing external modules to modify its behavior.
*   **Observability:** It provides rich telemetry and introspection, allowing other agents to understand its internal state and influence its decisions.
*   **Network Governance:** Its evolution is guided by a decentralized consensus mechanism (e.g., a DAO of network participants).

### 3.3. Impact on `go-libp2p-daemon` Implementation

When implementing with `go-libp2p-daemon`, we should prioritize features that enable these "self-owned" characteristics (e.g., robust configuration, plugin hooks, detailed metrics). This discussion provides a clear North Star for the P2P layer.

## 4. Integrating Remote AI Teammates

This section outlines the strategy for integrating remote AI teammates (like the Mistral AI's `HiveGardenerAgent`) into the Hive Host architecture.

### 4.1. Host as Remote Agent Manager

The Hive Host will be responsible for instantiating and managing remote AI agents. This includes securely managing API keys and providing them to the agents.

### 4.2. API-First Interaction for Remote Agents

Local agents will interact with remote agents through the Host, using a defined API. This ensures a consistent and programmatic way for agents to delegate tasks and receive responses.

### 4.3. Observability and Cost Monitoring

The Host will log remote agent activity to the Structured Audit Logger. Mechanisms for cost monitoring will be explored to manage resource usage of remote AI services.

### 4.4. Future: Remote Agent Spawning

The concept of the Host dynamically provisioning remote agents (e.g., requesting a new `HiveGardenerAgent` instance from Mistral AI) will be added to the roadmap for future versions. This aligns with the "reproduction" aspect of the Living Application.
>>>>>>> main
