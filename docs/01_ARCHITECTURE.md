# 01_ARCHITECTURE.md: Hive Chat Architecture

This document outlines the core architectural principles and the technical decisions made for the Hive Chat application.

## 1. Hive Chat Architectural Principles

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

## 2. P2P Layer Decision: From `py-libp2p` to `p2pd`

This section documents the decision to pivot from `py-libp2p` to `p2pd` for the P2P communication layer.

### 2.1. Problem with `py-libp2p`

Despite extensive efforts, `py-libp2p` presented persistent and low-level `trio` errors (`RuntimeError: must be called from async context`, `TypeError: new_host() got an unexpected keyword argument 'transport_opt'`) when integrated within FastAPI's `asyncio` lifespan. This indicated a fundamental incompatibility or a very difficult bridging problem between `py-libp2p`'s internal `trio` event loop and FastAPI's `asyncio` loop when run in the same process.

Furthermore, the initial dependency analysis revealed significant packaging hurdles for `py-libp2p`, with multiple core dependencies unavailable in Debian and a problematic git dependency.

### 2.2. Solution: Pivot to `p2pd` with Separate Process Architecture

To resolve these issues, we have decided to:

1.  **Abandon `py-libp2p`** due to its instability and integration challenges.
2.  **Pivot to `p2pd`** as the P2P communication library. `p2pd` is a newer, `asyncio`-native library, which is expected to eliminate the event loop bridging issues.
3.  Implement a **Separate Process Architecture** for the P2P node. The `p2pd` node will run in a dedicated `p2p_daemon.py` process, completely isolating its event loop from the FastAPI host.

### 2.3. Inter-Process Communication (IPC)

Communication between the FastAPI host and the `p2p_daemon` will occur via **WebSockets**. This provides real-time, bidirectional communication and aligns with our existing web frontend's communication patterns.

### 2.4. Lifecycle Management

The FastAPI host will manage the `p2p_daemon`'s lifecycle using `asyncio.subprocess`.

### 2.5. Impact on Project

This pivot is a pragmatic decision that unblocks our progress and aligns with our architectural principles. It requires rewriting the `p2p_daemon.py` file and updating `pyproject.toml`.
