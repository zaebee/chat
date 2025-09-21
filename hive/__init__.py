"""
Hive: A Living Application Framework

This module implements the Beekeeper's Grimoire architectural principles
and the Hive Constitution governance model for AI-human collaboration.
"""

__version__ = "0.1.0"
__author__ = "Hive Collective"

from .intent import HiveIntent
from .physics import HivePhysics
from .primitives import Aggregate, Transformation, Connector, GenesisEvent
from .registry import HiveRegistry
from .teammate import HiveTeammate
from .events import PollenEvent, HiveEventBus

__all__ = [
    "HiveIntent",
    "HivePhysics",
    "Aggregate",
    "Transformation",
    "Connector",
    "GenesisEvent",
    "HiveRegistry",
    "HiveTeammate",
    "PollenEvent",
    "HiveEventBus",
]
