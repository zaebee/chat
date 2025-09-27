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
from models import Message

# Import API routers
from api.game_system import router as game_system_router
from api.chat import router as chat_router
from api.hive_status import router as hive_status_router
from api.data_access import router as data_access_router
from api.user_management import router as user_management_router
from api.real_hive_analysis import router as real_hive_analysis_router

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
    lifespan=lifespan,
)

# Add CORS middleware - Secure configuration for Sacred Hive
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://localhost:5173",  # Vite development server
        "http://localhost:8080",  # Alternative dev server
        "https://chat.zae.life",  # Production domain
        "https://zae.life",  # Root domain
        # Add specific domains only - never use wildcard "*" in production
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
app.include_router(user_management_router)
app.include_router(real_hive_analysis_router)

# Set up XP broadcasting for API routers
from api.game_system import set_xp_broadcast_manager as set_game_xp_manager
from api.user_management import set_xp_broadcast_manager as set_user_xp_manager

set_game_xp_manager(manager)
set_user_xp_manager(manager)


# Core HTML and WebSocket endpoints
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


async def handle_sacred_command(
    command_text: str, user_id: str, username: str, websocket: WebSocket
):
    """Handle Sacred Team commands like /bee.chronicler.echo"""
    try:
        # Parse command and arguments
        parts = command_text.strip().split(" ", 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        # Process the command through Sacred Team Communication
        result = await manager.sacred_communication.process_sacred_command(
            command, args, user_id
        )

        # Send command acknowledgment back to user
        if result.get("success", True):
            ack_message = {
                "type": "sacred_command_ack",
                "data": {
                    "id": str(uuid.uuid4()),
                    "command": command,
                    "status": result.get("status", "processed"),
                    "message": result.get("message", "Sacred command processed"),
                    "timestamp": datetime.now().isoformat(),
                    "sender_name": "Sacred System",
                    "is_sacred": True,
                },
            }
            await websocket.send_text(json.dumps(ack_message))
        else:
            # Send error message
            error_message = {
                "type": "sacred_command_error",
                "data": {
                    "id": str(uuid.uuid4()),
                    "command": command,
                    "error": result.get("error", "Unknown error"),
                    "timestamp": datetime.now().isoformat(),
                    "sender_name": "Sacred System",
                    "is_sacred": True,
                },
            }
            await websocket.send_text(json.dumps(error_message))

        # Log the sacred command usage
        if HIVE_AVAILABLE and manager.event_bus:
            from hive.events import PollenEvent

            await manager.event_bus.publish(
                PollenEvent(
                    event_type="sacred_command_executed",
                    aggregate_id=f"user:{user_id}",
                    payload={
                        "command": command,
                        "args": args,
                        "user_id": user_id,
                        "username": username,
                        "success": result.get("success", True),
                    },
                    source_component="websocket_handler",
                    tags=["sacred_command", "chat_interface"],
                )
            )

    except Exception as e:
        print(f"Error handling Sacred command: {e}")
        # Send error response
        error_message = {
            "type": "sacred_command_error",
            "data": {
                "id": str(uuid.uuid4()),
                "command": command_text,
                "error": f"Command processing failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "sender_name": "Sacred System",
                "is_sacred": True,
            },
        }
        await websocket.send_text(json.dumps(error_message))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str, user_id: str):
    await manager.connect(websocket, user_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data.get("type") == "message":
                message_content = message_data.get("content", "")

                # Check if this is a Sacred command
                if (
                    message_content.startswith("/")
                    and HIVE_AVAILABLE
                    and manager.sacred_communication
                ):
                    await handle_sacred_command(
                        message_content, user_id, username, websocket
                    )
                else:
                    # Handle regular message
                    conn = get_db_connection()
                    message_id, timestamp = (
                        str(uuid.uuid4()),
                        datetime.now().isoformat(),
                    )
                    conn.execute(
                        """
                        INSERT INTO messages (id, user_id, username, content, text, sender_id, sender_name, timestamp, room_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            message_id,
                            user_id,
                            username,
                            message_content,
                            message_content,
                            user_id,
                            username,
                            timestamp,
                            "general",
                        ),
                    )
                    conn.commit()
                    conn.close()

                    user = manager.users.get(user_id)
                    if user:
                        message = Message(
                            id=message_id,
                            user_id=user_id,
                            username=username,
                            content=message_content,
                            timestamp=timestamp,
                            color=user.color,
                        )
                        broadcast_data = {"type": "message", "message": message.dict()}
                        await manager.broadcast(json.dumps(broadcast_data))

                        if HIVE_AVAILABLE and manager.event_bus:
                            await manager.event_bus.publish_message_event(
                                "sent", message_id, message.dict()
                            )

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast_user_update()


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "hive-chat-main",
        "hive_integration": HIVE_AVAILABLE,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
