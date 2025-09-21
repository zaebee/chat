from fastapi import APIRouter, HTTPException, Depends
import sqlite3
import json
from database import get_db

router = APIRouter()

@router.get("/api/organellas/{user_id}")
async def get_user_organellas(user_id: str, conn: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM organellas WHERE user_id = ? ORDER BY birth_timestamp DESC",
            (user_id,)
        )
        organellas = [{
            "id": row[0], "user_id": row[1], "name": row[2], "type": row[3], "stage": row[4],
            "level": row[5], "experience_points": row[6], "skills": json.loads(row[7]) if row[7] else {},
            "mystical_appearance": row[8], "birth_timestamp": row[9], "last_active": row[10],
            "unlocked_sections": json.loads(row[11]) if row[11] else []
        } for row in cursor.fetchall()]
        return {"organellas": organellas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/tales/{user_id}")
async def get_user_tales(user_id: str, conn: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tales WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        tales = [{
            "id": row[0], "user_id": row[1], "organella_id": row[2], "title": row[3],
            "content": row[4], "chapter_number": row[5], "created_at": row[6]
        } for row in cursor.fetchall()]
        return {"tales": tales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
