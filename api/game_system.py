from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from datetime import datetime
import json
import uuid
from pydantic import BaseModel
from typing import Optional

from database import get_db

# Import Hive components if available
try:
    import hive.events
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False

router = APIRouter()

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "chat"
    environmental_theme: Optional[dict] = None

@router.get("/api/user_progress/{user_id}")
async def get_user_progress(user_id: str, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute(
        "SELECT challenge_id FROM user_progress WHERE user_id = ?", (user_id,)
    )
    solved_challenge_ids = [row[0] for row in cursor.fetchall()]
    return {"user_id": user_id, "solved_challenge_ids": solved_challenge_ids}

@router.get("/api/rooms")
async def get_rooms(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute(
        "SELECT id, name, description, type, participant_count, message_count, environmental_theme FROM rooms WHERE is_active = 1"
    )
    rooms = []
    for row in cursor.fetchall():
        theme = json.loads(row[6]) if row[6] else {}
        rooms.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "type": row[3],
            "participant_count": row[4] or 0,
            "message_count": row[5] or 0,
            "theme": theme
        })
    return {"rooms": rooms}

@router.post("/api/rooms/create")
async def create_room(room_data: RoomCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Create a new chat room with optional environmental theme."""
    try:
        room_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()

        # Convert environmental_theme to JSON string if provided
        theme_json = json.dumps(room_data.environmental_theme) if room_data.environmental_theme else None

        # Insert new room into database
        conn.execute("""
            INSERT INTO rooms (id, name, description, type, participant_count, message_count,
                             environmental_theme, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            room_id,
            room_data.name,
            room_data.description or "",
            room_data.type,
            0,  # participant_count
            0,  # message_count
            theme_json,
            1,  # is_active
            created_at
        ))
        conn.commit()

        # Publish room creation event to Hive
        if HIVE_AVAILABLE:
            try:
                from connection_manager import manager
                if manager.event_bus:
                    await manager.event_bus.publish_system_event("room_created", {
                        "room_id": room_id,
                        "room_name": room_data.name,
                        "room_type": room_data.type,
                        "created_at": created_at
                    })
            except Exception as e:
                # Don't fail room creation if event publishing fails
                print(f"Failed to publish room creation event: {e}")

        # Return the created room data
        return {
            "success": True,
            "room": {
                "id": room_id,
                "name": room_data.name,
                "description": room_data.description or "",
                "type": room_data.type,
                "participant_count": 0,
                "message_count": 0,
                "theme": room_data.environmental_theme or {},
                "is_active": True,
                "created_at": created_at
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create room: {str(e)}")

@router.post("/solve_challenge")
async def solve_challenge(solution: dict, conn: sqlite3.Connection = Depends(get_db)):
    user_id = solution.get("user_id")
    challenge_id = solution.get("challenge_id")

    if not user_id or not challenge_id:
        raise HTTPException(status_code=400, detail="Missing user_id or challenge_id")

    cursor = conn.execute(
        "SELECT 1 FROM user_progress WHERE user_id = ? AND challenge_id = ?",
        (user_id, challenge_id)
    )
    if cursor.fetchone():
        return {"message": "Challenge already solved", "user_id": user_id, "challenge_id": challenge_id}

    timestamp = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO user_progress (user_id, challenge_id, solved_at) VALUES (?, ?, ?)",
        (user_id, challenge_id, timestamp)
    )
    conn.commit()

    return {"message": "Challenge solved successfully", "user_id": user_id, "challenge_id": challenge_id}
