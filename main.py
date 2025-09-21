
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for simplicity, can be restricted later
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
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
                message_id = str(uuid.uuid4())
                timestamp = datetime.now().isoformat()

                conn.execute("""
                    INSERT INTO messages (id, user_id, username, content, timestamp, room_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (message_id, user_id, username, message_data.get("content", ""), timestamp, "general"))
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
