"""
Status Mixin for Hive Components

This module provides a reusable status mixin that eliminates redundancy
in get_status implementations across all Hive components.

Following the DRY principle and the Legibility requirement from the
Beekeeper's Grimoire Constitution.
"""

from abc import ABC
from typing import Dict, Any
from datetime import datetime


class StatusMixin:
    """
    Mixin class providing common status functionality for all Hive components.

    This eliminates redundancy by providing base status fields that are
    common across all components in the Hive ecosystem.
    """

    def _get_base_status(self) -> Dict[str, Any]:
        """
        Get common status fields shared by all components.

        Returns:
            Dict containing standard status fields:
            - id: Component unique identifier
            - name: Human-readable component name
            - created_at: ISO timestamp of creation
            - timestamp: Current ISO timestamp
            - metadata: Component-specific metadata
        """
        base_status = {
            "timestamp": datetime.now().isoformat(),
        }

        # Add id if available
        if hasattr(self, 'id'):
            base_status["id"] = self.id

        # Add name if available
        if hasattr(self, 'name'):
            base_status["name"] = self.name

        # Add created_at if available
        if hasattr(self, 'created_at'):
            base_status["created_at"] = self.created_at.isoformat()

        # Add metadata if available
        if hasattr(self, 'metadata'):
            base_status["metadata"] = self.metadata

        return base_status

    def _merge_status(self, specific_status: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge specific status fields with base status fields.

        Args:
            specific_status: Component-specific status fields

        Returns:
            Dict containing merged base + specific status
        """
        base_status = self._get_base_status()
        base_status.update(specific_status)
        return base_status


class LegibilityProtocol(ABC):
    """
    Protocol ensuring all Hive components implement the Legibility principle.

    All components must be self-describing through standardized status reporting.
    """

    def get_status(self) -> Dict[str, Any]:
        """Return structured status for observability."""
        raise NotImplementedError("Components must implement get_status for Legibility")

    async def health_check(self) -> bool:
        """Perform health check and return status."""
        raise NotImplementedError("Components must implement health_check for monitoring")