from fastapi import APIRouter, HTTPException, Depends
import sqlite3
import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from database import get_db
from models import OrganellaCreate, OrganellaUpdate

router = APIRouter()


@router.post("/api/organellas")
async def create_organella(organella: OrganellaCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Create a new organella"""
    timestamp = datetime.now().isoformat()
    organella_id = f"org_{int(datetime.now().timestamp())}"

    try:
        conn.execute("""
            INSERT INTO organellas (id, user_id, name, type, stage, level, experience_points,
                                  skills, mystical_appearance, birth_timestamp, last_active, unlocked_sections)
            VALUES (?, ?, ?, ?, ?, 1, 0, ?, ?, ?, ?, '[]')
        """, (
            organella_id, organella.user_id, organella.name, organella.type, organella.stage,
            json.dumps(organella.skills or {}), organella.mystical_appearance or "",
            timestamp, timestamp
        ))
        conn.commit()

        return {
            "id": organella_id,
            "user_id": organella.user_id,
            "name": organella.name,
            "type": organella.type,
            "stage": organella.stage,
            "level": 1,
            "experience_points": 0,
            "skills": organella.skills or {},
            "mystical_appearance": organella.mystical_appearance or "",
            "birth_timestamp": timestamp,
            "last_active": timestamp,
            "unlocked_sections": []
        }
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Organella creation failed")

@router.get("/api/organellas/{organella_id}")
async def get_organella(organella_id: str, conn: sqlite3.Connection = Depends(get_db)):
    """Get organella by ID"""
    cursor = conn.execute("SELECT * FROM organellas WHERE id = ?", (organella_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Organella not found")

    return {
        "id": row[0],
        "user_id": row[1],
        "name": row[2],
        "type": row[3],
        "stage": row[4],
        "level": row[5],
        "experience_points": row[6],
        "skills": json.loads(row[7]) if row[7] else {},
        "mystical_appearance": row[8],
        "birth_timestamp": row[9],
        "last_active": row[10],
        "unlocked_sections": json.loads(row[11]) if row[11] else []
    }

@router.put("/api/organellas/{organella_id}")
async def update_organella(organella_id: str, updates: OrganellaUpdate, conn: sqlite3.Connection = Depends(get_db)):
    """Update organella data"""
    # Check if organella exists
    cursor = conn.execute("SELECT * FROM organellas WHERE id = ?", (organella_id,))
    existing_organella = cursor.fetchone()

    if not existing_organella:
        raise HTTPException(status_code=404, detail="Organella not found")

    # Build update query dynamically
    update_fields = []
    update_values = []

    if updates.name is not None:
        update_fields.append("name = ?")
        update_values.append(updates.name)

    if updates.stage is not None:
        update_fields.append("stage = ?")
        update_values.append(updates.stage)

    if updates.level is not None:
        update_fields.append("level = ?")
        update_values.append(updates.level)

    if updates.experience_points is not None:
        update_fields.append("experience_points = ?")
        update_values.append(updates.experience_points)

    if updates.skills is not None:
        update_fields.append("skills = ?")
        update_values.append(json.dumps(updates.skills))

    if updates.mystical_appearance is not None:
        update_fields.append("mystical_appearance = ?")
        update_values.append(updates.mystical_appearance)

    if updates.unlocked_sections is not None:
        update_fields.append("unlocked_sections = ?")
        update_values.append(json.dumps(updates.unlocked_sections))

    # Always update last_active
    update_fields.append("last_active = ?")
    update_values.append(datetime.now().isoformat())

    # Add organella_id for WHERE clause
    update_values.append(organella_id)

    # Execute update
    query = f"UPDATE organellas SET {', '.join(update_fields)} WHERE id = ?"
    conn.execute(query, update_values)
    conn.commit()

    # Return updated organella
    return await get_organella(organella_id, conn)

@router.post("/api/organellas/{organella_id}/add_xp")
async def add_organella_xp(organella_id: str, xp_data: dict, conn: sqlite3.Connection = Depends(get_db)):
    """Add XP to organella and handle progression"""
    xp_gain = xp_data.get("xp", 0)

    if xp_gain <= 0:
        raise HTTPException(status_code=400, detail="XP gain must be positive")

    # Get current organella data
    organella = await get_organella(organella_id, conn)

    # Calculate new XP and level
    new_experience = organella["experience_points"] + xp_gain
    new_level = max(1, (new_experience // 50) + 1)  # Level up every 50 XP for organellas

    # Update organella
    updates = OrganellaUpdate(
        experience_points=new_experience,
        level=new_level,
        skills={
            **organella["skills"],
            "totalXP": new_experience,
            "lastXPGain": xp_gain,
            "lastXPGainAt": datetime.now().isoformat()
        }
    )

    updated_organella = await update_organella(organella_id, updates, conn)

    return {
        "organella": updated_organella,
        "xp_gained": xp_gain,
        "new_level": new_level,
        "leveled_up": new_level > organella["level"]
    }

async def distribute_xp_to_organellas(user_id: str, xp_amount: int, conn: sqlite3.Connection):
    """Distribute XP to user's organellas when user gains XP"""
    try:
        # Get all user's organellas
        cursor = conn.execute("SELECT id FROM organellas WHERE user_id = ?", (user_id,))
        organella_ids = [row[0] for row in cursor.fetchall()]

        if not organella_ids:
            return  # No organellas to distribute XP to

        # Distribute XP evenly among organellas (25% of user XP)
        organella_xp = max(1, int(xp_amount * 0.25 / len(organella_ids)))

        # Update each organella
        for organella_id in organella_ids:
            try:
                await add_organella_xp(organella_id, {"xp": organella_xp}, conn)
            except Exception as e:
                print(f"Failed to distribute XP to organella {organella_id}: {e}")
                continue

    except Exception as e:
        print(f"Failed to distribute XP to organellas for user {user_id}: {e}")
