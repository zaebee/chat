# Proposal: The Folding Pollen Protocol

This document proposes a new standard for communication within the Hive: the "Folding Pollen Protocol". This protocol combines the "Pollen Packet" standard with the Safe AutoEvolution Framework, creating a powerful system for managing information density and observability.

## 1. Core Concept: Information Folding

The core concept is that all communication in the Hive can exist in two states:

- **Folded:** A concise, symbolic representation of an event or a piece of information. This is designed for high-level overviews, logs, and quick scanning.
- **Unfolded:** The full, detailed representation of the information, with all the necessary context and data.

## 2. The Folding Pollen Packet Standard

The "Pollen Packet" will be the standard format for all foldable communication.

### Folded State:

A single line of text with a clear, parseable structure.
`[type]: [subject] | [status] | [key_metric_1]=[value_1], [key_metric_2]=[value_2]`

**Example:**
`evo-proposal: ReviewAggregate | pending_approval | risk=medium, safety_score=0.85`

### Unfolded State:

A rich JSON object with the full details.

**Example:**

```json
{
  "type": "evolution_proposal",
  "subject": {
    "component_id": "ReviewAggregate",
    "mutation_type": "parameter_tuning"
  },
  "status": "pending_human_approval",
  "details": {
    "description": "Adjusting the max_history_size from 1000 to 1500.",
    "code_diff": "...",
    "validation_report": {
      "trinity_score": 0.9,
      "performance_impact": "-5ms",
      "security_risk": "low"
    }
  }
}
```

## 3. Integration with the Safe AutoEvolution Framework

This protocol will be a cornerstone of the Safe AutoEvolution Framework, making the evolution process highly observable and manageable.

### Use Cases:

- **Evolution Proposals:** A new mutation proposal will be broadcast as a folded `evo-proposal` event. The `EvolutionDashboard` can display a list of these folded events. Clicking on one will "unfold" it to show the full details for human approval.
- **Status Monitoring:** The `AutoRollbackMonitor` can broadcast folded `evo-status` events, providing a real-time stream of the health of all evolving components.
- **Alerting:** If a rollback is triggered, a folded `evo-alert` event can be sent, which can be unfolded to reveal the full post-mortem of the failure.

## 4. Implementation

1.  **`FoldingPollenPacket` Class:** A new class will be created in `hive/events/` that can be instantiated with a rich data object and can serialize itself to both a "folded" string and an "unfolded" JSON object.
2.  **Frontend Component:** A generic `FoldableContent.vue` component will be created that can display a folded message and has a button to "unfold" it, revealing the detailed view.
3.  **Integration:** The Safe AutoEvolution Framework components (`SafeEvolutionController`, `AutoRollbackMonitor`, etc.) will be updated to use `FoldingPollenPacket` for all their event broadcasting.

## 5. Benefits

- **Improved Observability:** Operators can get a high-level overview of the system at a glance, and then dive into the details as needed.
- **Reduced Cognitive Load:** The folded format reduces information overload.
- **Enhanced Manageability:** The system becomes easier to manage, especially when there are many concurrent evolutions.
- **Scalability:** This protocol will scale well as the Hive grows and the number of events increases.

This re-synthesized proposal provides a much more powerful and integrated vision for our communication protocol. It's not just about sending messages; it's about managing the flow and density of information in a complex, living system.
