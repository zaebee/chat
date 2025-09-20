# Project Roadmap

This document outlines the high-level goals and planned features for the Hive Chat application.

## Version 1.0: The Hive Host

- [x] Basic real-time chat functionality
- [x] Initial packaging research and pivot to "Living Application" model
- [x] Establishment of Architectural Principles and multi-agent team

# Project Roadmap

This document outlines the high-level goals and planned features for the Hive Chat application.

## Version 1.0: The Genesis Hive

- [x] Basic real-time chat functionality
- [x] Initial packaging research and pivot to "Living Application" model
- [x] Establishment of Architectural Principles and multi-agent team
- [ ] **Core Hive Host Runtime:** Develop the main application binary that can dynamically load and manage agents.
- [ ] **Foundational Services:** The Host will provide a shared **Async Event Bus** and a **Structured Audit Logger** to all agents.
- [ ] **Agent-based Refactor:** Refactor the existing chat application to be the first, default agent, aligned with the **ATCG-Genome**.
- [ ] **P2P Agent Communication:** Implement the underlying libp2p stack.
- **τ (System Tension) Monitoring:** Implement and expose basic τ monitoring via the `/api/v1/status` endpoint.
- [ ] **Simple Management CLI:** Implement a basic command-line interface for the user to view the status of the hive.

## Version 2.0: The Expanding Hive

- [ ] **"Queen Bee" Code Generator:** Develop a tool to generate agent boilerplate from a YAML definition.
- [ ] **Agent Management API:** Implement the full CRUD API (`/api/v1/agents`) for deploying and managing agents at runtime.
- [ ] **Shared Knowledge Store:** Design and implement a shared knowledge repository for agents.
- **Secure Update Mechanism:** Implement a robust, secure self-updating mechanism for the "Living Application" binary.

## Version 3.0: The Distributed Hive

- [ ] **Hive-to-Hive Discovery:** Implement a mechanism for different Hive nodes to discover and connect with each other.
- [ ] **Agent Migration:** Allow agents to migrate from one Hive node to another.
- [ ] **Decentralized Governance:** Explore models for decentralized governance of the Hive network.

- [ ] **Foundational Services:** The Host will provide a shared **Async Event Bus** and a **Structured Audit Logger** to all agents.
- [ ] **Agent-based Refactor:** Refactor the existing chat application to be the first, default agent running on the Hive Host and using the foundational services.
- [ ] **P2P Agent Communication:** Implement the underlying libp2p stack for all inter-agent communication.
- [ ] **Basic Introspection API:** Implement the initial `/api/v1/status` endpoint.
- [ ] **Simple Management CLI:** Implement a basic command-line interface for the user to view the status of the hive and its agents.

## Version 2.0: The Expanding Hive

- [ ] **Agent Management API:** Implement the full CRUD API (`/api/v1/agents`) for deploying and managing agents at runtime.
- [ ] **Shared Knowledge Store:** Design and implement a shared knowledge repository for agents.
- **Secure Update Mechanism:** Implement a robust, secure self-updating mechanism for the "Living Application" binary.
- **Enhanced Introspection:** Expand the API to allow agents to query the host's purpose, architecture, and source code integrity.

## Version 3.0: The Distributed Hive

- [ ] **Hive-to-Hive Discovery:** Implement a mechanism for different Hive nodes to discover and connect with each other.
- [ ] **Agent Migration:** Allow agents to migrate from one Hive node to another.
- [ ] **Decentralized Governance:** Explore models for decentralized governance of the Hive network.
