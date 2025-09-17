# Project Roadmap

This document outlines the high-level goals and planned features for the Hive Chat application.

## Version 1.0: The Foundation

*   [x] Basic real-time chat functionality
*   [x] Initial packaging research and pivot to "Living Application" model
*   [ ] Separate frontend assets (CSS/JS) from HTML
*   [ ] Persistent message history with SQLite
*   [ ] P2P messaging with libp2p (Hybrid Model)
*   [ ] Basic machine-readable introspection API (`/api/v1/status`)

## Version 2.0: The Single-Node Hive

*   [ ] **Agent Management API:** Implement a full CRUD API (`/api/v1/agents`) for deploying, monitoring, and managing other agents within the application.
*   **Inter-Agent Communication:** Use the underlying libp2p network for communication between hosted agents.
*   **Enhanced Introspection:** The API will be expanded to allow agents to query the host's purpose, architecture, and source code integrity.
*   **Secure Update Mechanism:** Implement a robust, secure self-updating mechanism for the "Living Application" binary.

## Version 3.0: The Distributed Hive

*   [ ] **Hive-to-Hive Discovery:** Implement a mechanism for different Hive nodes to discover and connect with each other.
*   **Agent Migration:** Allow agents to migrate from one Hive node to another.
*   **Decentralized Governance:** Explore models for decentralized governance of the Hive network.
