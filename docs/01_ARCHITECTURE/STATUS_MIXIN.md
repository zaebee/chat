---
title: "StatusMixin: Standardizing Component Status"
description: "Details the StatusMixin, a reusable component for consistent status reporting across Hive components."
category: "architecture"
audience: "developer|ai-agent"
complexity: "beginner"
last_updated: "2025-09-22"
related_docs: ["./ATCG_PRIMITIVES.md", "./AGENT_FRAMEWORK.md"]
code_examples: true
---

# StatusMixin: Standardizing Component Status

## Overview

The `StatusMixin` is a foundational component introduced to standardize the `get_status()` method across various Hive components. Its primary purpose is to reduce code duplication and ensure a consistent, legible format for status reporting, aligning with the Hive's Principle of Legibility.

## Purpose

- **Reduce Redundancy:** Eliminates repetitive code in `get_status()` implementations.
- **Enhance Ontological Purity:** Provides a pure, non-redundant representation of a component's core status attributes.
- **Improve Consistency:** Ensures all components report their basic status information in a uniform manner.
- **Facilitate Observability:** Makes it easier for both human and AI teammates to parse and understand component states.

## Usage

To use the `StatusMixin`, a class simply needs to inherit from it and ensure it has `id`, `name`, `created_at`, and `metadata` attributes (which are typically present in `HiveComponent` or `TeammateProfile`).

```python
from hive.status_mixin import StatusMixin
from datetime import datetime

class MyComponent(StatusMixin):
    def __init__(self, id: str, name: str, metadata: dict = None):
        self.id = id
        self.name = name
        self.created_at = datetime.now()
        self.metadata = metadata or {}

    def get_status(self) -> dict:
        base_status = self._get_base_status()
        # Add component-specific status fields
        base_status.update({
            "custom_field": "value",
            "another_metric": 123
        })
        return base_status

    async def health_check(self) -> bool:
        # Component-specific health check logic
        return True
```

## Benefits

- **DRY (Don't Repeat Yourself):** Centralizes common status logic.
- **Architectural Elegance:** Promotes a cleaner, more modular codebase.
- **Human-AI Symbiosis:** Provides a predictable and machine-readable interface for status queries.
- **Maintainability:** Easier to update or extend status reporting across the entire system.

## Related Components

- **ATCG Primitives:** `Aggregate`, `Transformation`, `Connector`, `GenesisEvent` (in `hive/primitives.py`) now utilize the `StatusMixin`.
- **HiveTeammate:** The base class for AI teammates (in `hive/teammate.py`) also benefits from this standardized approach.

This ensures that the core building blocks and the AI agents of the Hive consistently report their status, contributing to a more legible and observable Living Application.