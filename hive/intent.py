"""
Intent Level: The Philosophical Purpose of the Hive

This module defines the Intent Level from the Beekeeper's Grimoire -
the philosophical purpose that drives the entire system.
"""

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


@dataclass
class HiveIntent:
    """
    The philosophical purpose and driving force of the Hive system.

    According to the Grimoire, this is the highest level of abstraction -
    the "why" that gives meaning to all lower levels.
    """

    # Core mission statement
    mission: str = (
        "To cultivate a Living Application that serves as a collaborative "
        "habitat for human and AI teammates, enabling sovereign, self-sustaining "
        "digital organisms that can reproduce, evolve, and learn together."
    )

    # Core values from the Hive Constitution
    values: Dict[str, str] = None

    # Current incarnation goals
    current_focus: str = (
        "Building a collaborative chat environment with integrated Python "
        "learning playground that demonstrates human-AI symbiosis principles."
    )

    # Metrics that align with our purpose
    success_metrics: Dict[str, str] = None

    def __post_init__(self):
        if self.values is None:
            self.values = {
                "sovereignty": "The application does not depend on central authority",
                "reproduction": "Enable self-replication and specialized evolution",
                "symbiosis": "Human and AI agents as first-class citizens",
                "legibility": "System state should be self-describing",
                "observability": "Emit structured events for all teammates",
                "modularity": "Loosely coupled, composable components",
                "api_first": "All functionality accessible programmatically",
            }

        if self.success_metrics is None:
            self.success_metrics = {
                "tau": "System complexity and health (lower is better)",
                "phi": "Code quality and maintainability (higher is better)",
                "sigma": "Collaborative efficiency between teammates",
                "reproduction_rate": "Ability to spawn new specialized instances",
                "teammate_satisfaction": "Both human and AI agent experience",
            }

    def get_current_purpose(self) -> str:
        """Returns the current driving purpose of the system."""
        return f"{self.mission}\n\nCurrent Focus: {self.current_focus}"

    def evaluate_alignment(self, action: str, outcome: Dict[str, Any]) -> float:
        """
        Evaluate how well an action/outcome aligns with our intent.

        Returns a score from 0.0 (completely misaligned) to 1.0 (perfectly aligned).
        """
        # This is a simplified alignment evaluator
        # In a full implementation, this would use more sophisticated metrics

        alignment_score = 0.5  # neutral baseline

        # Check if action promotes key values
        action_lower = action.lower()

        if "collaborate" in action_lower or "teammate" in action_lower:
            alignment_score += 0.2  # promotes symbiosis

        if "autonomous" in action_lower or "self" in action_lower:
            alignment_score += 0.1  # promotes sovereignty

        if "api" in action_lower or "interface" in action_lower:
            alignment_score += 0.1  # promotes accessibility

        if "event" in action_lower or "observable" in action_lower:
            alignment_score += 0.1  # promotes observability

        return min(1.0, alignment_score)

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        return {
            "component": "HiveIntent",
            "level": "Intent",
            "mission": self.mission,
            "current_focus": self.current_focus,
            "values": self.values,
            "success_metrics": list(self.success_metrics.keys()),
            "timestamp": datetime.now().isoformat(),
            "health": "active",
        }
