from fastapi import APIRouter, Depends
import sqlite3
from database import get_db
from connection_manager import manager

router = APIRouter()

@router.get("/api/messages")
async def get_messages(limit: int = 50, conn: sqlite3.Connection = Depends(get_db)):
    messages = conn.execute("""
        SELECT id, user_id, username, content, timestamp
        FROM messages
        WHERE user_id IS NOT NULL AND username IS NOT NULL AND content IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,)).fetchall()

    return [
        {
            "id": msg[0],
            "user_id": msg[1],
            "username": msg[2],
            "content": msg[3],
            "timestamp": msg[4],
            "color": "#4ECDC4"
        }
        for msg in reversed(messages)
    ]

@router.get("/api/users")
async def get_users():
    return {"users": [user.model_dump() for user in manager.users.values()]}
