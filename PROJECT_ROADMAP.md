# Project Roadmap

This document outlines the high-level goals and planned features for the Hive Chat application.

## Version 1.0: The Hive Host

*   [x] Basic real-time chat functionality
*   [x] Initial packaging research and pivot to "Living Application" model
*   [x] Establishment of Architectural Principles and multi-agent team
*   [ ] **Core Hive Host Runtime:** Develop the main application binary that can dynamically load and manage agents.
*   **Agent-based Refactor:** Refactor the existing chat application to be the first, default agent running on the Hive Host.
*   **P2P Agent Communication:** Implement the underlying libp2p stack for all inter-agent communication.
*   **Basic Introspection API:** Implement the initial `/api/v1/status` endpoint.

## Version 2.0: The Expanding Hive

*   [ ] **Agent Management API:** Implement the full CRUD API (`/api/v1/agents`) for deploying and managing agents at runtime.
*   **Secure Update Mechanism:** Implement a robust, secure self-updating mechanism for the "Living Application" binary.
*   **Enhanced Introspection:** Expand the API to allow agents to query the host's purpose, architecture, and source code integrity.

## Version 3.0: The Distributed Hive

*   [ ] **Hive-to-Hive Discovery:** Implement a mechanism for different Hive nodes to discover and connect with each other.
*   **Agent Migration:** Allow agents to migrate from one Hive node to another.
*   **Decentralized Governance:** Explore models for decentralized governance of the Hive network.
