# Architecture

This document outlines the architectural principles and decisions for the Hive Chat application.

## 1. Core Architectural Principles

This section outlines the core principles that guide the development and architecture of the Hive Chat application. These principles are designed to create a system that is resilient, sovereign, and a collaborative environment for both human and AI teammates.

### 1.1. Principle of Legibility: The Code Must Be Self-Describing

An AI teammate should be able to understand the purpose and state of any component without having to read the source code.

*   **Implementation:** We will create a standardized, machine-readable API for introspection. Every major component (e.g., the P2P node, the connection manager) will have a `get_status()` method that returns a structured JSON object.

### 1.2. Principle of Observability: The System Must Announce Its State

The application should not just log for humans; it should emit structured events for AI teammates.

*   **Implementation:** We will establish a system-wide event bus or a set of well-defined API endpoints for querying real-time status and metrics.

### 1.3. Principle of Modularity: The System Must Be Composable

The application should be composed of loosely coupled modules with well-defined interfaces.

*   **Implementation:** This allows an AI to reason about, test, and even replace individual components without destabilizing the entire system. Our current separation of `chat.py`, `database.py`, and the future `p2p.py` aligns with this.

### 1.4. Principle of API-First Interaction: Actions Should Be Programmatic

All core functionalities of the application should be accessible through a secure, versioned API, not just through a user interface.

*   **Implementation:** An AI teammate should be able to send messages, query users, and manage the system through RESTful API calls.

### 1.5. Principle of Human-AI Symbiosis: Build for Teammates

We recognize that the development and operation of this software will be a collaboration between humans and AI agents. The system should be designed to be a friendly and productive environment for both.

*   **Implementation:** Documentation, APIs, and even commit messages should be written with both a human and an AI audience in mind. The system should be designed to be not just "user-friendly," but "teammate-friendly."

## 2. Architectural Decisions

### 2.1. Distribution: The "Living Application" Model

Based on the dependency analysis for our desired P2P stack, we have decided to pivot from a traditional Debian packaging (`.deb`) model to a **"Living Application"** model.

*   **Artifact:** The application will be distributed as a single, self-contained executable binary (e.g., created with PyInstaller).
*   **Rationale:** This approach completely mitigates the risks associated with the complex and unavailable dependencies of `py-libp2p` in the Debian ecosystem. It gives us the freedom to choose our dependencies without being constrained by platform-specific packaging.
*   **Implementation:** The binary will bundle the Python interpreter, all necessary libraries, and the application code itself.

### 2.2. System Design: The Hive Host & Agent Model

The application will be structured as a **Hive Host** that loads and manages one or more **Agents**.

*   **Hive Host:** The core executable responsible for providing foundational services (P2P networking, event bus, logging) and managing the agent lifecycle.
*   **Agents:** Modular, self-contained components that implement specific features. The chat functionality itself will be our first agent.
*   **Communication:** The Hive employs multiple communication patterns:
    *   **P2P Network (libp2p):** Primary inter-agent communication, even between agents in the same host process
    *   **Event Bus (Pollen Protocol):** Structured event-driven communication for observability and coordination
    *   **WebSocket:** Real-time bidirectional communication for chat and live updates
    *   **REST API:** Synchronous request-response for CRUD operations and system management
    *   **Git Protocol:** Version control and collaboration workflows for distributed development

### 2.3. Current Agents and Services

As of the current implementation, the system consists of two primary agents:

*   **Backend Agent (`chat.py`):**
    *   **Role:** Serves as the primary backend service and a basic Hive Host.
    *   **Functionality:** Manages WebSocket connections, broadcasts messages, and persists chat history to a SQLite database.
    *   **Technology:** FastAPI (Python).

*   **Frontend Agent (`/frontend`):**
    *   **Role:** Provides the user interface and all client-side application logic.
    *   **Functionality:** Renders the chat interface, login flow, and the Python Learning Playground. Manages its own state via Pinia stores.
    *   **Key Services within the Agent:**
        *   `pythonRunner.ts`: A crucial service that provides a secure, sandboxed Python execution environment by integrating with the Pyodide (Wasm) runtime. This allows for safe, client-side execution of user-submitted code.
        *   `chat.ts` (Pinia Store): Manages all real-time state for the application, including the WebSocket connection, messages, user lists, and UI preferences (theme, language).
    *   **Technology:** Vue.js 3 (Vite), TypeScript, Pinia.

---

## Appendix A: P2P Dependency Analysis

This appendix documents the findings of the research into the `py-libp2p` dependency tree, which led to the decision to pivot away from Debian packaging.

### A.1. Executive Summary

The research concludes that packaging `py-libp2p` as a traditional Debian package is **not feasible** at this time without a significant, and likely prohibitive, amount of effort.

The primary reasons for this conclusion are:
*   **Multiple Blocking Dependencies:** Several of `py-libp2p`'s core dependencies are not available in the official Debian repositories.
*   **Git Dependency:** `py-libp2p` depends on a specific git commit of the `multiaddr` library, a practice that is incompatible with standard Debian packaging policies.
*   **Packaging Cascade:** Each unavailable dependency would need to be packaged first, and each of those may have its own complex dependency tree, leading to a "packaging cascade" of ever-increasing work.

### A.2. Detailed Dependency Analysis

The following table details the analysis of each dependency of `py-libp2p`:

| Dependency | Version | Debian Package | Status | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| `aioquic` | `>=1.2.0` | `python3-aioquic` | Available | **Available** |
| `base58` | `>=1.0.3` | `python3-base58` | Available | **Available** |
| `coincurve` | `==21.0.0` | `python3-coincurve` | "in preparation" | **Unavailable/Blocker** |
| `exceptiongroup` | `>=1.2.0` | `python3-exceptiongroup` | Available | **Available** |
| `fastecdsa` | `==2.3.2` | `python3-fastecdsa` | Not available | **Unavailable/Blocker** |
| `grpcio` | `>=1.41.0` | `python3-grpcio` | Available | **Available** |
| `lru-dict` | `>=1.1.6` | `python3-lru-dict` | Available | **Available** |
| `multiaddr` | `git commit` | `python3-multiaddr` | Not available | **Unavailable/Blocker** |
| `mypy-protobuf` | `>=3.0.0` | `python3-mypy-protobuf` | Available | **Available** |
| `noiseprotocol` | `>=0.3.0` | `python3-noiseprotocol` | Available | **Available** |
| `protobuf` | `>=4.25.0` | `python3-protobuf` | Available | **Available** |
| `pycryptodome` | `>=3.9.2` | `python3-pycryptodome` | Available | **Available** |
| `pymultihash` | `>=0.8.2` | `python3-pymultihash` | Not available | **Unavailable/Blocker** |
| `pynacl` | `>=1.3.0` | `python3-nacl` | Available | **Available** |
| `rpcudp` | `>=3.0.0` | `python3-rpcudp` | Not available | **Unavailable/Blocker** |
| `trio-typing` | `>=0.0.4` | `python3-trio-typing` | Not available | **Unavailable/Blocker** |
| `trio` | `>=0.26.0` | `python3-trio` | Available | **Available** |
| `zeroconf` | `>=0.147.0` | `python3-zeroconf` | Available | **Available** |