from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from datetime import datetime
import json
from typing import Optional
from pydantic import BaseModel

from database import get_db
from models import UserCreate, UserUpdate

router = APIRouter()

@router.post("/api/users")
async def create_user(user: UserCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Create a new user"""
    timestamp = datetime.now().isoformat()

    try:
        conn.execute("""
            INSERT INTO users (id, username, email, experience, level, stats, created_at, updated_at)
            VALUES (?, ?, ?, 0, 1, '{}', ?, ?)
        """, (user.id, user.username, user.email, timestamp, timestamp))
        conn.commit()

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "experience": 0,
            "level": 1,
            "stats": {},
            "created_at": timestamp,
            "updated_at": timestamp
        }
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")

@router.get("/api/users/{user_id}")
async def get_user(user_id: str, conn: sqlite3.Connection = Depends(get_db)):
    """Get user by ID"""
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "experience": row[3],
        "level": row[4],
        "stats": json.loads(row[5]) if row[5] else {},
        "created_at": row[6],
        "updated_at": row[7]
    }

@router.put("/api/users/{user_id}")
async def update_user(user_id: str, updates: UserUpdate, conn: sqlite3.Connection = Depends(get_db)):
    """Update user data"""
    # Check if user exists
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Build update query dynamically
    update_fields = []
    update_values = []

    if updates.username is not None:
        update_fields.append("username = ?")
        update_values.append(updates.username)

    if updates.email is not None:
        update_fields.append("email = ?")
        update_values.append(updates.email)

    if updates.experience is not None:
        update_fields.append("experience = ?")
        update_values.append(updates.experience)

    if updates.level is not None:
        update_fields.append("level = ?")
        update_values.append(updates.level)

    if updates.stats is not None:
        update_fields.append("stats = ?")
        update_values.append(json.dumps(updates.stats))

    # Always update timestamp
    update_fields.append("updated_at = ?")
    update_values.append(datetime.now().isoformat())

    # Add user_id for WHERE clause
    update_values.append(user_id)

    # Execute update
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
    conn.execute(query, update_values)
    conn.commit()

    # Return updated user
    return await get_user(user_id, conn)

@router.post("/api/users/{user_id}/add_xp")
async def add_user_xp(user_id: str, xp_data: dict, conn: sqlite3.Connection = Depends(get_db)):
    """Add XP to user and handle level progression"""
    xp_gain = xp_data.get("xp", 0)

    if xp_gain <= 0:
        raise HTTPException(status_code=400, detail="XP gain must be positive")

    # Get current user data
    user = await get_user(user_id, conn)

    # Calculate new XP and level
    new_experience = user["experience"] + xp_gain
    new_level = max(1, (new_experience // 100) + 1)  # Level up every 100 XP

    # Update user
    updates = UserUpdate(
        experience=new_experience,
        level=new_level,
        stats={
            **user["stats"],
            "totalXP": new_experience,
            "lastXPGain": xp_gain,
            "lastXPGainAt": datetime.now().isoformat()
        }
    )

    updated_user = await update_user(user_id, updates, conn)

    # Trigger organella XP distribution if enabled
    try:
        from api.organellas import distribute_xp_to_organellas
        await distribute_xp_to_organellas(user_id, xp_gain, conn)
    except ImportError:
        # Organella distribution not available
        pass

    return {
        "user": updated_user,
        "xp_gained": xp_gain,
        "new_level": new_level,
        "leveled_up": new_level > user["level"]
    }
