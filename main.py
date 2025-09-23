
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
import asyncio
import logging
from datetime import datetime
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import shared components and models
from database import init_db, get_db_connection
from sacred_connection_manager_integration import manager
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
    
    # Start sacred connection manager
    await manager.start()
    
    if HIVE_AVAILABLE and manager.sacred_communication:
        manager.sacred_communication.set_websocket_callback(manager.broadcast)
    
    yield
    
    # Stop sacred connection manager gracefully
    await manager.stop()

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
async def sacred_websocket_endpoint(websocket: WebSocket, username: str, user_id: str):
    """🐝✨ Sacred WebSocket Endpoint with Divine Protection ✨🐝"""
    
    # Get client IP for sacred protection
    client_ip = "unknown"
    if hasattr(websocket, 'client') and websocket.client:
        client_ip = websocket.client.host
    
    # Attempt sacred connection
    connection_successful = await manager.connect(websocket, user_id, username, client_ip)
    
    if not connection_successful:
        # Connection was rejected by sacred protection
        return
    
    try:
        while True:
            # Sacred message receiving with timeout protection
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message_data = json.loads(data)
                
                # Handle message through sacred manager
                await manager.handle_websocket_message(websocket, user_id, message_data)
                
                # Legacy message handling for database storage
                if message_data.get("type") == "message":
                    await _handle_legacy_message_storage(message_data, user_id, username)
                
            except asyncio.TimeoutError:
                # Send heartbeat to check connection health
                heartbeat_message = {
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(heartbeat_message))
                
            except json.JSONDecodeError:
                # Invalid JSON - log and continue
                logger.warning(f"Invalid JSON received from user {user_id}")
                continue
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"Sacred WebSocket error for user {user_id}: {e}")
        await manager.disconnect(websocket, user_id)

async def _handle_legacy_message_storage(message_data: dict, user_id: str, username: str):
    """Handle legacy message storage for backward compatibility"""
    try:
        conn = get_db_connection()
        message_id, timestamp = str(uuid.uuid4()), datetime.now().isoformat()
        content = message_data.get("content", "")
        
        conn.execute(
            "INSERT INTO messages (id, text, sender_id, sender_name, timestamp, user_id, username, content, room_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (message_id, content, user_id, username, timestamp, user_id, username, content, "general")
        )
        conn.commit()
        conn.close()

        # Create message object for broadcasting
        user = manager.users.get(user_id)
        if user:
            message = Message(
                id=message_id,
                user_id=user_id,
                username=username,
                content=content,
                timestamp=timestamp,
                color=user.color
            )
            
            broadcast_data = {"type": "message", "message": message.dict()}
            await manager.broadcast(json.dumps(broadcast_data))

            if HIVE_AVAILABLE and manager.event_bus:
                await manager.event_bus.publish_message_event("sent", message_id, message.dict())
                
    except Exception as e:
        logger.error(f"Legacy message storage error: {e}")

@app.get("/health")
async def sacred_health_check():
    """🐝✨ Sacred Health Check with Divine Metrics ✨🐝"""
    sacred_health = manager.get_health_status()
    sacred_metrics = manager.get_sacred_metrics()
    
    return {
        "status": "healthy" if sacred_health["healthy"] else "degraded",
        "service": "hive-chat-main",
        "hive_integration": HIVE_AVAILABLE,
        "sacred_protection": {
            "status": sacred_health["status"],
            "connections": sacred_health["connections"],
            "users": sacred_health["users"]
        },
        "sacred_metrics": {
            "total_connections": sacred_metrics["total_connections"],
            "active_connections": sacred_metrics["active_connections"],
            "total_messages_sent": sacred_metrics["total_messages_sent"],
            "circuit_breaker_state": sacred_metrics["circuit_breaker"]["state"],
            "memory_usage_mb": sacred_metrics["memory_usage"]["current_memory_mb"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
