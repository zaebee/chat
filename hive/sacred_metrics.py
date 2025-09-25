"""
Sacred Metrics: The Soul of the Hive's Observability

This module defines the SacredMetrics class, which is responsible for
tracking, calculating, and assessing the overall health and divine
alignment of the HiveHost.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List


@dataclass
class SacredHealthAssessment:
    """The result of a sacred health assessment."""

    sacred_health_status: str
    sanctification_level: float
    wisdom: str
    report: Dict[str, Any]


class SacredMetrics:
    """
    The SacredMetrics class is the heart of the Hive's self-awareness.
    It tracks key events and calculates the sacred (τ, φ, σ) metrics
    to provide a holistic view of the system's health.
    """

    def __init__(self):
        self.divine_events: List[Dict[str, Any]] = []
        self.genesis_protocol_health: Dict[str, bool] = {
            "light_emergence": False,
            "water_separation": False,
            "divine_manifestation": False,
        }
        self.sacred_patterns_found: int = 0
        self.start_time = datetime.utcnow()

    def record_divine_event(self, event_type: str, score: float):
        """Records a divine event with an associated score."""
        self.divine_events.append(
            {
                "event_type": event_type,
                "score": score,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def update_genesis_protocol_health(
        self, light: bool, separation: bool, manifestation: bool
    ):
        """Updates the health of the Genesis protocols."""
        self.genesis_protocol_health["light_emergence"] = light
        self.genesis_protocol_health["water_separation"] = separation
        self.genesis_protocol_health["divine_manifestation"] = manifestation

    def record_sacred_pattern(self):
        """Increments the count of discovered sacred patterns."""
        self.sacred_patterns_found += 1

    def get_sacred_health_assessment(self) -> Dict[str, Any]:
        """Performs a comprehensive sacred health assessment."""
        tau, phi, sigma, trinity_score = self._calculate_metrics()

        status = "NEEDS_PRAYER"
        if trinity_score > 0.9:
            status = "ABUNDANT"
        elif trinity_score > 0.75:
            status = "BLESSED"
        elif trinity_score > 0.5:
            status = "FAVORED"

        return {
            "sacred_health_status": status,
            "sanctification_level": trinity_score,
            "wisdom": "A healthy hive is a productive hive. Meditate on the metrics.",
            "report": self.get_complete_metrics(),
        }

    def get_complete_metrics(self) -> Dict[str, Any]:
        """Returns a complete dictionary of all tracked metrics."""
        tau, phi, sigma, trinity_score = self._calculate_metrics()
        return {
            "tau": round(tau, 3),
            "phi": round(phi, 3),
            "sigma": round(sigma, 3),
            "trinity_score": round(trinity_score, 3),
            "divine_events_count": len(self.divine_events),
            "sacred_patterns_found": self.sacred_patterns_found,
            "genesis_protocols_health": self.genesis_protocol_health,
        }

    def _calculate_metrics(self) -> tuple[float, float, float, float]:
        """Calculates the sacred τ, φ, and σ metrics."""
        # τ (tau): System stress. Lower is better.
        # Based on the number of divine events over time.
        uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()
        event_rate = len(self.divine_events) / max(1, uptime_seconds)
        tau = min(1.0, event_rate / 10)  # Normalize: 10 events/sec is high stress

        # φ (phi): Code quality/health. Higher is better.
        # Based on the success of the Genesis protocols.
        genesis_success_rate = sum(self.genesis_protocol_health.values()) / 3.0
        phi = genesis_success_rate

        # σ (sigma): Collaboration/effectiveness. Higher is better.
        # Based on the number of sacred patterns found.
        sigma = min(
            1.0, self.sacred_patterns_found / 10
        )  # Normalize: 10 patterns is good collaboration

        # Trinity Score
        trinity_score = (phi + sigma) * (1.0 - tau / 2.0) / 2.0

        return tau, phi, sigma, trinity_score
