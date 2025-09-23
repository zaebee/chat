"""
Hive Chat: Integrated Living Application

This module combines the existing chat functionality with the HiveHost runtime
to create a unified "Living Application" that demonstrates human-AI collaboration.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import List, Dict, Optional, Any
import json
import os
import uuid
from datetime import datetime
from contextlib import asynccontextmanager
import websockets.exceptions

# Import existing database functionality
from database import init_db, get_db_connection

# Import our new HiveHost
from hive_host import HiveHost
from status_api import StatusAPI

# Import Hive components
from hive.events import PollenEvent


# Data models (from original chat.py)
class User(BaseModel):
    id: str
    username: str
    color: str


class Message(BaseModel):
    id: str
    text: str
    sender_id: str
    sender_name: str
    timestamp: str
    is_bot: bool = False


class ChallengeSolution(BaseModel):
    challenge_id: str
    code: str
    user_id: str


# Global HiveHost instance
hive_host: Optional[HiveHost] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with HiveHost integration."""
    global hive_host
    
    # Initialize database
    init_db()
    
    # Initialize and start HiveHost
    hive_host = HiveHost("hive-chat-main")
    await hive_host.start()
    
    # Hive Chat started
    
    yield
    
    # Cleanup
    if hive_host:
        await hive_host.stop()
        # Hive Chat stopped


# Initialize FastAPI with HiveHost integration
app = FastAPI(
    title="Hive Chat - Living Application",
    description="A collaborative learning platform with AI teammates",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow requests from development environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://localhost:8080",
        "https://localhost:3000",
        "https://localhost:5173",
        "https://localhost:8080",
        # Production domains
        "https://chat.zae.life",
        "https://www.chat.zae.life",
    ],
    # Regex to match Gitpod and Codespaces URLs
    allow_origin_regex=r"https://.*\.gitpod\.(dev|io)$|https://.*\.githubpreview\.dev$|https://.*\.app\.github\.dev$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users: Dict[str, User] = {}

    async def connect(self, websocket: WebSocket, user: User):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.users[user.id] = user
        
        # Publish connection event to Hive
        if hive_host:
            event = PollenEvent(
                event_type="user_connected",
                aggregate_id=user.id,
                payload={
                    "user_id": user.id,
                    "username": user.username,
                    "connection_count": len(self.active_connections)
                },
                source_component="chat_websocket",
                tags=["chat", "connection", "user_activity"]
            )
            await hive_host.event_bus.publish(event)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.users:
            del self.users[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove broken connections
                self.active_connections.remove(connection)

    def get_user_list(self):
        return [{"id": user.id, "username": user.username, "color": user.color} 
                for user in self.users.values()]


manager = ConnectionManager()


# API Routes

@app.get("/")
async def get_chat_page(request: Request):
    """Serve the main chat interface."""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/api/users")
async def get_users():
    """Get list of connected users."""
    return {"users": manager.get_user_list()}


@app.get("/api/messages")
async def get_messages():
    """Get chat message history."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, text, sender_id, sender_name, timestamp, is_bot 
            FROM messages 
            ORDER BY timestamp DESC 
            LIMIT 50
        """)
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "id": row[0],
                "text": row[1],
                "sender_id": row[2],
                "sender_name": row[3],
                "timestamp": row[4],
                "is_bot": bool(row[5])
            })
        conn.close()
        return {"messages": list(reversed(messages))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# HiveHost Status Integration
@app.get("/api/v1/status")
async def get_hive_status():
    """Get HiveHost status."""
    if not hive_host:
        raise HTTPException(status_code=503, detail="HiveHost not available")
    
    status = hive_host.get_status()
    return JSONResponse(content={
        "status": "success",
        "data": {
            "host_id": status.host_id,
            "uptime_seconds": status.uptime_seconds,
            "agent_count": status.agent_count,
            "active_agents": status.active_agents,
            "event_bus_status": status.event_bus_status,
            "metrics": status.metrics,
            "last_updated": status.last_updated,
            "chat_connections": len(manager.active_connections),
            "connected_users": len(manager.users)
        }
    })


@app.get("/api/v1/health")
async def health_check():
    """Comprehensive health check."""
    if not hive_host:
        return JSONResponse(
            content={"status": "unhealthy", "error": "HiveHost not available"},
            status_code=503
        )
    
    health = await hive_host.health_check()
    
    # Add chat-specific health info
    health["components"]["chat"] = {
        "status": "healthy",
        "details": {
            "active_connections": len(manager.active_connections),
            "connected_users": len(manager.users),
            "database_available": True  # Could add actual DB check
        }
    }
    
    status_code = 200 if health["status"] == "healthy" else 503
    return JSONResponse(content=health, status_code=status_code)


@app.get("/api/v1/metrics")
async def get_metrics():
    """Get system metrics including chat metrics."""
    if not hive_host:
        raise HTTPException(status_code=503, detail="HiveHost not available")
    
    base_metrics = hive_host.metrics
    
    # Add chat-specific metrics
    chat_metrics = {
        "chat_connections": len(manager.active_connections),
        "connected_users": len(manager.users),
        "messages_in_db": 0  # Could query actual count
    }
    
    return JSONResponse(content={
        "status": "success",
        "data": {
            **base_metrics,
            "chat": chat_metrics
        }
    })


# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat."""
    # Get user info from query params
    username = websocket.query_params.get("username", f"User_{user_id[:8]}")
    color = websocket.query_params.get("color", "#007bff")
    
    user = User(id=user_id, username=username, color=color)
    
    await manager.connect(websocket, user)
    
    # Send welcome message
    welcome_msg = {
        "type": "system",
        "message": f"🐝 Welcome to the Hive, {username}! You are now connected to the Living Application.",
        "timestamp": datetime.now().isoformat()
    }
    await manager.send_personal_message(json.dumps(welcome_msg), websocket)
    
    # Broadcast user joined
    join_msg = {
        "type": "user_joined",
        "user": {"id": user.id, "username": user.username, "color": user.color},
        "message": f"{username} joined the Hive",
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast(json.dumps(join_msg))
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "message":
                # Create message
                message = Message(
                    id=str(uuid.uuid4()),
                    text=message_data["text"],
                    sender_id=user.id,
                    sender_name=user.username,
                    timestamp=datetime.now().isoformat(),
                    is_bot=False
                )
                
                # Save to database
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO messages (id, text, sender_id, sender_name, timestamp, is_bot)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (message.id, message.text, message.sender_id, 
                          message.sender_name, message.timestamp, message.is_bot))
                    conn.commit()
                    conn.close()
                except Exception as e:
                    # Database error handled
                
                # Publish message event to Hive
                if hive_host:
                    event = PollenEvent(
                        event_type="message_sent",
                        aggregate_id=f"chat_room_main",
                        payload={
                            "message_id": message.id,
                            "text": message.text,
                            "sender_id": message.sender_id,
                            "sender_name": message.sender_name,
                            "word_count": len(message.text.split()),
                            "timestamp": message.timestamp
                        },
                        source_component="chat_websocket",
                        tags=["chat", "message", "user_interaction"]
                    )
                    await hive_host.event_bus.publish(event)
                
                # Broadcast message
                broadcast_data = {
                    "type": "message",
                    "message": message.dict(),
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast(json.dumps(broadcast_data))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
        
        # Publish disconnection event
        if hive_host:
            event = PollenEvent(
                event_type="user_disconnected",
                aggregate_id=user.id,
                payload={
                    "user_id": user.id,
                    "username": user.username,
                    "connection_count": len(manager.active_connections)
                },
                source_component="chat_websocket",
                tags=["chat", "disconnection", "user_activity"]
            )
            await hive_host.event_bus.publish(event)
        
        # Broadcast user left
        leave_msg = {
            "type": "user_left",
            "user": {"id": user.id, "username": user.username, "color": user.color},
            "message": f"{user.username} left the Hive",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(json.dumps(leave_msg))


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Hive Chat - Living Application")
    parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    args = parser.parse_args()
    
    # Starting Hive Chat server
    
    uvicorn.run(app, host=args.host, port=args.port)