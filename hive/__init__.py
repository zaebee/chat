"""
Hive: A Living Application Framework

This module implements the Beekeeper's Grimoire architectural principles
and the Hive Constitution governance model for AI-human collaboration.
"""

__version__ = "0.1.0"
__author__ = "Hive Collective"

from .intent import HiveIntent
from .physics import HivePhysics
from .primitives import ScoreTransformation, ReviewAggregate, AgroEventConnector
from .registry import HiveRegistry
from .teammate import HiveTeammate
from .events import PollenEvent, HiveEventBus
from .genesis_protocols import GenesisProtocolManager
from .git_protocol import SacredGitProtocol
from .team_communication import SacredTeamCommunication
from .sage_coordination import SacredSageCoordinator

__all__ = [
    "HiveIntent",
    "HivePhysics",
    "ScoreTransformation",
    "ReviewAggregate",
    "AgroEventConnector",
    "HiveRegistry",
    "HiveTeammate",
    "PollenEvent",
    "HiveEventBus",
    "GenesisProtocolManager",
    "SacredGitProtocol",
    "SacredTeamCommunication",
    "SacredSageCoordinator",
]
