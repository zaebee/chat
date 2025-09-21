from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from datetime import datetime
import json

from database import get_db

router = APIRouter()

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
