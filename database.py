import sqlite3
from fastapi import Depends

DATABASE_URL = "chat.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """FastAPI dependency for database connections"""
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = get_db_connection()

    # Messages table for chat functionality
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            user_id TEXT,
            username TEXT,
            content TEXT,
            room_id TEXT DEFAULT 'general',
            parent_id TEXT
        );
    """)

    # User progress for challenge tracking
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id TEXT NOT NULL,
            challenge_id TEXT NOT NULL,
            solved_at TEXT NOT NULL,
            PRIMARY KEY (user_id, challenge_id)
        );
    """)

    # Rooms table for multi-room chat support
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            type TEXT DEFAULT 'chat',
            participant_count INTEGER DEFAULT 0,
            message_count INTEGER DEFAULT 0,
            environmental_theme TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        );
    """)

    # Organellas table for Sacred Team ecosystem
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organellas (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            stage TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            experience_points INTEGER DEFAULT 0,
            skills TEXT,
            mystical_appearance TEXT,
            birth_timestamp TEXT NOT NULL,
            last_active TEXT,
            unlocked_sections TEXT
        );
    """)

    # Tales table for storytelling feature
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tales (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            organella_id TEXT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            chapter_number INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        );
    """)

    # Insert default room if none exists
    if conn.execute("SELECT COUNT(*) FROM rooms").fetchone()[0] == 0:
        from datetime import datetime
        conn.execute("INSERT INTO rooms (id, name, description, type, created_at) VALUES (?, ?, ?, ?, ?)",
                    ('general', 'General Chat', 'Main chat room for Sacred Team collaboration', 'chat', datetime.now().isoformat()))

    conn.commit()
    conn.close()
