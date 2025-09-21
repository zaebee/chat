from fastapi import APIRouter
from datetime import datetime

from connection_manager import manager

router = APIRouter()

try:
    from hive.events import HiveEventBus
    from hive.team_communication import SacredTeamCommunication
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False

@router.get("/api/hive/status")
async def get_hive_status():
    if not HIVE_AVAILABLE:
        return {"status": "unavailable", "reason": "Hive components not loaded"}

    return {
        "status": "active",
        "components": {
            "event_bus": manager.event_bus is not None,
            "sacred_communication": manager.sacred_communication is not None
        }
    }

@router.get("/api/hive/teammates")
async def get_teammates():
    if not HIVE_AVAILABLE:
        return {"teammates": []}

    # This would integrate with the actual Hive teammate registry
    return {"teammates": ["bee.jules", "bee.chronicler"]}

@router.get("/api/sacred_team/presence")
async def get_sacred_presence():
    return {
        "present": ["bee.jules", "bee.chronicler"],
        "last_activity": datetime.now().isoformat()
    }
