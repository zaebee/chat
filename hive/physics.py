"""
Physics Level: Infrastructure and Environmental Constraints

This module defines the Physics Level from the Beekeeper's Grimoire -
the environmental constraints and infrastructure limitations that shape
how the system can operate.
"""

import psutil
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
import os


@dataclass
class ResourceConstraints:
    """Physical resource constraints of the environment."""

    max_memory_mb: int = 1024  # Maximum memory usage in MB
    max_cpu_percent: float = 80.0  # Maximum CPU usage percentage
    max_connections: int = 100  # Maximum concurrent connections
    max_disk_mb: int = 10240  # Maximum disk usage in MB
    network_timeout_seconds: int = 30  # Network operation timeout


@dataclass
class EnvironmentalFactors:
    """Environmental factors that affect system behavior."""

    is_development: bool = True
    has_internet: bool = True
    has_gpu: bool = False
    container_environment: Optional[str] = None  # docker, kubernetes, etc.
    deployment_stage: str = "development"  # development, staging, production


class HivePhysics:
    """
    Manages the physical constraints and environmental factors
    that govern how the Hive system can operate.

    This includes resource monitoring, constraint enforcement,
    and adaptation to environmental changes.
    """

    def __init__(self):
        self.constraints = ResourceConstraints()
        self.environment = EnvironmentalFactors()
        self._current_metrics = {}
        self._last_update = None

    async def update_metrics(self):
        """Update current resource usage metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used / (1024 * 1024)

            # Disk usage
            disk = psutil.disk_usage("/")
            disk_mb = disk.used / (1024 * 1024)

            # Network connections (approximation)
            connections = len(psutil.net_connections())

            self._current_metrics = {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb,
                "disk_mb": disk_mb,
                "connections": connections,
                "timestamp": datetime.now().isoformat(),
            }
            self._last_update = datetime.now()

        except Exception as e:
            # Graceful degradation if system metrics aren't available
            self._current_metrics = {
                "cpu_percent": 0.0,
                "memory_mb": 0.0,
                "disk_mb": 0.0,
                "connections": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def check_constraints(self) -> Dict[str, bool]:
        """Check if current resource usage violates constraints."""
        if not self._current_metrics:
            return {"status": False, "reason": "metrics_not_available"}

        violations = {}

        if (
            self._current_metrics.get("cpu_percent", 0)
            > self.constraints.max_cpu_percent
        ):
            violations["cpu"] = (
                f"CPU usage {self._current_metrics['cpu_percent']:.1f}% exceeds limit {self.constraints.max_cpu_percent}%"
            )

        if self._current_metrics.get("memory_mb", 0) > self.constraints.max_memory_mb:
            violations["memory"] = (
                f"Memory usage {self._current_metrics['memory_mb']:.1f}MB exceeds limit {self.constraints.max_memory_mb}MB"
            )

        if (
            self._current_metrics.get("connections", 0)
            > self.constraints.max_connections
        ):
            violations["connections"] = (
                f"Connections {self._current_metrics['connections']} exceeds limit {self.constraints.max_connections}"
            )

        return {"within_constraints": len(violations) == 0, "violations": violations}

    def can_accept_new_connection(self) -> bool:
        """Check if system can accept a new connection without violating constraints."""
        current_connections = self._current_metrics.get("connections", 0)
        return current_connections < self.constraints.max_connections

    def can_execute_transformation(
        self, estimated_cpu: float, estimated_memory: float
    ) -> bool:
        """Check if system can execute a transformation without violating constraints."""
        current_cpu = self._current_metrics.get("cpu_percent", 0)
        current_memory = self._current_metrics.get("memory_mb", 0)

        return (current_cpu + estimated_cpu) <= self.constraints.max_cpu_percent and (
            current_memory + estimated_memory
        ) <= self.constraints.max_memory_mb

    def detect_environment(self):
        """Detect and update environmental factors."""
        # Check if running in development
        self.environment.is_development = os.getenv("NODE_ENV") != "production"

        # Check container environment
        if os.path.exists("/.dockerenv"):
            self.environment.container_environment = "docker"
        elif os.getenv("KUBERNETES_SERVICE_HOST"):
            self.environment.container_environment = "kubernetes"

        # Check GPU availability (simplified)
        try:
            import GPUtil

            gpus = GPUtil.getGPUs()
            self.environment.has_gpu = len(gpus) > 0
        except ImportError:
            self.environment.has_gpu = False

        # Check internet connectivity (simplified)
        try:
            import socket

            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.environment.has_internet = True
        except OSError:
            self.environment.has_internet = False

    def get_adaptation_suggestions(self) -> Dict[str, str]:
        """Suggest system adaptations based on current physics."""
        suggestions = {}

        constraints_check = self.check_constraints()
        if not constraints_check["within_constraints"]:
            violations = constraints_check["violations"]

            if "cpu" in violations:
                suggestions["cpu"] = (
                    "Consider reducing concurrent operations or implementing CPU throttling"
                )

            if "memory" in violations:
                suggestions["memory"] = (
                    "Consider implementing memory cleanup or reducing cache sizes"
                )

            if "connections" in violations:
                suggestions["connections"] = (
                    "Consider implementing connection pooling or rate limiting"
                )

        # Environmental adaptations
        if not self.environment.has_internet:
            suggestions["network"] = (
                "Operating in offline mode - disable external API calls"
            )

        if self.environment.container_environment:
            suggestions["container"] = (
                f"Optimizing for {self.environment.container_environment} environment"
            )

        return suggestions

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        return {
            "component": "HivePhysics",
            "level": "Physics",
            "constraints": {
                "max_memory_mb": self.constraints.max_memory_mb,
                "max_cpu_percent": self.constraints.max_cpu_percent,
                "max_connections": self.constraints.max_connections,
            },
            "current_metrics": self._current_metrics,
            "environment": {
                "is_development": self.environment.is_development,
                "has_internet": self.environment.has_internet,
                "has_gpu": self.environment.has_gpu,
                "container_environment": self.environment.container_environment,
            },
            "constraints_check": self.check_constraints(),
            "adaptation_suggestions": self.get_adaptation_suggestions(),
            "last_update": self._last_update.isoformat() if self._last_update else None,
            "timestamp": datetime.now().isoformat(),
            "health": "active",
        }
