from fastapi import APIRouter, HTTPException, Depends
import sqlite3
import json
import logging
from datetime import datetime

from database import get_db
from models import OrganellaCreate, OrganellaUpdate
from hive.events import PollenEvent

router = APIRouter()
logger = logging.getLogger(__name__)

# Sacred Constants - Game Balance Values
ORGANELLA_XP_PER_LEVEL = 50  # XP required per level for organellas
ORGANELLA_XP_DISTRIBUTION_RATE = 0.25  # 25% of user XP goes to organellas
ALLOWED_UPDATE_FIELDS = {
    "name",
    "type",
    "stage",
    "level",
    "experience_points",
    "skills",
    "mystical_appearance",
    "last_active",
    "unlocked_sections",
}


@router.post("/api/organellas")
async def create_organella(
    organella: OrganellaCreate, conn: sqlite3.Connection = Depends(get_db)
):
    """Create a new organella"""
    timestamp = datetime.now().isoformat()
    organella_id = f"org_{int(datetime.now().timestamp())}"

    try:
        conn.execute(
            """
            INSERT INTO organellas (id, user_id, name, type, stage, level, experience_points,
                                  skills, mystical_appearance, birth_timestamp, last_active, unlocked_sections)
            VALUES (?, ?, ?, ?, ?, 1, 0, ?, ?, ?, ?, '[]')
        """,
            (
                organella_id,
                organella.user_id,
                organella.name,
                organella.type,
                organella.stage,
                json.dumps(organella.skills or {}),
                organella.mystical_appearance or "",
                timestamp,
                timestamp,
            ),
        )
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
            "unlocked_sections": [],
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
        "unlocked_sections": json.loads(row[11]) if row[11] else [],
    }


@router.put("/api/organellas/{organella_id}")
async def update_organella(
    organella_id: str,
    updates: OrganellaUpdate,
    conn: sqlite3.Connection = Depends(get_db),
):
    """Update organella data"""
    # Check if organella exists
    cursor = conn.execute("SELECT * FROM organellas WHERE id = ?", (organella_id,))
    existing_organella = cursor.fetchone()

    if not existing_organella:
        raise HTTPException(status_code=404, detail="Organella not found")

    # Sacred SQL with whitelist protection - build update using allowed fields only
    update_fields = []
    update_values = []

    # Whitelist approach - only allow trusted field updates
    update_data = updates.model_dump(exclude_unset=True)

    for field_name, field_value in update_data.items():
        if field_name not in ALLOWED_UPDATE_FIELDS:
            logger.warning(f"Attempted to update disallowed field: {field_name}")
            continue

        if field_name in ("skills", "unlocked_sections"):
            # JSON fields require serialization
            update_fields.append(f"{field_name} = ?")
            update_values.append(json.dumps(field_value))
        else:
            update_fields.append(f"{field_name} = ?")
            update_values.append(field_value)

    # Always update last_active timestamp
    update_fields.append("last_active = ?")
    update_values.append(datetime.now().isoformat())

    if not update_fields:
        logger.info(f"No valid fields to update for organella {organella_id}")
        return await get_organella(organella_id, conn)

    # Add organella_id for WHERE clause
    update_values.append(organella_id)

    # Execute sacred update with parameterized query (no f-strings)
    query = "UPDATE organellas SET " + ", ".join(update_fields) + " WHERE id = ?"

    try:
        conn.execute(query, update_values)
        conn.commit()
        logger.debug(
            f"Successfully updated organella {organella_id} with fields: {list(update_data.keys())}"
        )
    except sqlite3.Error as e:
        logger.error(f"Database error updating organella {organella_id}: {e}")
        raise HTTPException(status_code=500, detail="Database update failed")

    # Optimize: return updated data directly instead of re-fetching
    # Re-fetch is still needed due to complex JSON field handling and computed values
    return await get_organella(organella_id, conn)


@router.post("/api/organellas/{organella_id}/add_xp")
async def add_organella_xp(
    organella_id: str, xp_data: dict, conn: sqlite3.Connection = Depends(get_db)
):
    """Add XP to organella and handle progression"""
    xp_gain = xp_data.get("xp", 0)

    if xp_gain <= 0:
        raise HTTPException(status_code=400, detail="XP gain must be positive")

    # Get current organella data
    organella = await get_organella(organella_id, conn)

    # Calculate new XP and level using sacred constants
    new_experience = organella["experience_points"] + xp_gain
    new_level = max(1, (new_experience // ORGANELLA_XP_PER_LEVEL) + 1)

    # Update organella
    updates = OrganellaUpdate(
        experience_points=new_experience,
        level=new_level,
        skills={
            **organella["skills"],
            "totalXP": new_experience,
            "lastXPGain": xp_gain,
            "lastXPGainAt": datetime.now().isoformat(),
        },
    )

    updated_organella = await update_organella(organella_id, updates, conn)

    # Sacred Pollen Protocol Events for system observability
    leveled_up = new_level > organella["level"]

    # Emit XP gained event
    xp_event = PollenEvent(
        event_type="organella_xp_gained",
        aggregate_id=organella_id,
        payload={
            "organella_id": organella_id,
            "xp_gained": xp_gain,
            "total_xp": new_experience,
            "previous_level": organella["level"],
            "current_level": new_level,
        },
        source_component="OrganellaAPI",
    )
    logger.info(f"🌸 Pollen Event: {xp_event.event_type} for organella {organella_id}")

    # Emit level up event if applicable
    if leveled_up:
        levelup_event = PollenEvent(
            event_type="organella_leveled_up",
            aggregate_id=organella_id,
            payload={
                "organella_id": organella_id,
                "previous_level": organella["level"],
                "new_level": new_level,
                "total_xp": new_experience,
                "sacred_milestone": f"✨ Organella ascended to level {new_level} ✨",
            },
            source_component="OrganellaAPI",
        )
        logger.info(
            f"🎉 Pollen Event: {levelup_event.event_type} - Level {organella['level']} → {new_level}"
        )

    return {
        "organella": updated_organella,
        "xp_gained": xp_gain,
        "new_level": new_level,
        "leveled_up": leveled_up,
    }


async def distribute_xp_to_organellas(
    user_id: str, xp_amount: int, conn: sqlite3.Connection
):
    """
    Distribute XP to user's organellas when user gains XP.
    Uses sacred constants for balance and proper error handling for observability.
    """
    try:
        # Get all user's organellas
        cursor = conn.execute("SELECT id FROM organellas WHERE user_id = ?", (user_id,))
        organella_ids = [row[0] for row in cursor.fetchall()]

        if not organella_ids:
            logger.debug(
                f"No organellas found for user {user_id} - skipping XP distribution"
            )
            return  # No organellas to distribute XP to

        # Distribute XP evenly among organellas using sacred constant
        organella_xp = max(
            1, int(xp_amount * ORGANELLA_XP_DISTRIBUTION_RATE / len(organella_ids))
        )

        logger.info(
            f"Distributing {organella_xp} XP to {len(organella_ids)} organellas for user {user_id}"
        )

        # Update each organella with proper error tracking
        successful_distributions = 0
        for organella_id in organella_ids:
            try:
                await add_organella_xp(organella_id, {"xp": organella_xp}, conn)
                successful_distributions += 1
            except HTTPException as e:
                logger.warning(
                    f"XP distribution failed for organella {organella_id}: {e.detail}"
                )
                continue
            except Exception as e:
                logger.error(
                    f"Unexpected error distributing XP to organella {organella_id}: {e}"
                )
                continue

        logger.info(
            f"Successfully distributed XP to {successful_distributions}/{len(organella_ids)} organellas"
        )

    except sqlite3.Error as e:
        logger.error(f"Database error during XP distribution for user {user_id}: {e}")
        # Re-raise database errors as they indicate serious issues
        raise
    except Exception as e:
        logger.error(f"Unexpected error during XP distribution for user {user_id}: {e}")
        # Don't re-raise general errors to avoid breaking the parent operation
