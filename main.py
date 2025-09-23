
#!/usr/bin/env python3
"""
Main Hive Application Entry Point

This script initializes the FastAPI application, includes all modular API routers,
and sets up the primary WebSocket endpoint.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
from datetime import datetime
from contextlib import asynccontextmanager

# Import shared components and models
from database import init_db, get_db_connection
from connection_manager import manager
from models import User, Message

# Import API routers
from api.game_system import router as game_system_router
from api.chat import router as chat_router
from api.hive_status import router as hive_status_router
from api.data_access import router as data_access_router

# Import Hive components if available
try:
    from hive.events import HiveEventBus
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    if HIVE_AVAILABLE and manager.sacred_communication:
        manager.sacred_communication.set_websocket_callback(manager.broadcast)
    yield

# Initialize FastAPI
app = FastAPI(
    title="Hive Chat System",
    description="AI-Human Collaborative Chat Platform",
    lifespan=lifespan
)

# Add CORS middleware - Secure configuration for Sacred Hive
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React development server
        "http://localhost:5173",    # Vite development server
        "http://localhost:8080",    # Alternative dev server
        "https://chat.zae.life",    # Production domain
        "https://zae.life",         # Root domain
        # Add specific domains only - never use wildcard "*" in production
	"https://5173--01996650-5be4-7cf0-a882-a28cca500054.eu-central-1-01.gitpod.dev",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Removed OPTIONS for security
    allow_headers=["Content-Type", "Authorization", "Accept"],  # Specific headers only
)

# Mount static files and templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all the modular API routers
app.include_router(game_system_router)
app.include_router(chat_router)
app.include_router(hive_status_router)
app.include_router(data_access_router)

# Core HTML and WebSocket endpoints
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str, user_id: str):
    await manager.connect(websocket, user_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data.get("type") == "message":
                conn = get_db_connection()
                message_id, timestamp = str(uuid.uuid4()), datetime.now().isoformat()
                conn.execute("INSERT INTO messages (id, text, sender_id, sender_name, timestamp, user_id, username, content, room_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (message_id, message_data.get("content", ""), user_id, username, timestamp, user_id, username, message_data.get("content", ""), "general"))
                conn.commit()
                conn.close()

                user = manager.users.get(user_id)
                if user:
                    message = Message(
                        id=message_id,
                        user_id=user_id,
                        username=username,
                        content=message_data.get("content", ""),
                        timestamp=timestamp,
                        color=user.color
                    )
                    broadcast_data = {"type": "message", "message": message.dict()}
                    await manager.broadcast(json.dumps(broadcast_data))

                    if HIVE_AVAILABLE and manager.event_bus:
                        await manager.event_bus.publish_message_event("sent", message_id, message.dict())

            elif message_data.get("type") == "reaction":
                # Handle message reactions
                reaction_data = {
                    "type": "reaction",
                    "messageId": message_data.get("messageId"),
                    "emoji": message_data.get("emoji"),
                    "userId": message_data.get("userId"),
                    "userName": message_data.get("userName"),
                    "action": message_data.get("action")
                }
                
                # Broadcast reaction to all connected users
                await manager.broadcast(json.dumps(reaction_data))
                
                # TODO: Store reactions in database for persistence
                # For now, reactions are only stored in memory/frontend

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast_user_update()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "hive-chat-main",
        "hive_integration": HIVE_AVAILABLE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
