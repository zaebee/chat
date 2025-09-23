
#!/usr/bin/env python3
"""
Main Hive Application Entry Point

This script initializes the FastAPI application, includes all modular API routers,
and sets up the primary WebSocket endpoint.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
from datetime import datetime
from contextlib import asynccontextmanager
from collections import defaultdict
import time

# Import shared components and models
from database import init_db, get_db_connection
from connection_manager import manager
from models import Message

# Import API routers
from api.game_system import router as game_system_router
from api.chat import router as chat_router
from api.hive_status import router as hive_status_router
from api.data_access import router as data_access_router

# Import Hive components if available
try:
    import hive.events
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False

# Simple rate limiting storage
rate_limit_storage: defaultdict[str, list[float]] = defaultdict(list)

def is_rate_limited(client_ip: str, max_requests: int = 60, window_seconds: int = 60) -> bool:
    """Simple rate limiting: max_requests per window_seconds."""
    now = time.time()
    requests = rate_limit_storage[client_ip]

    # Remove old requests outside the window
    requests[:] = [req_time for req_time in requests if now - req_time < window_seconds]

    # Check if limit exceeded
    if len(requests) >= max_requests:
        return True

    # Add current request
    requests.append(now)
    return False

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

# Correlation ID middleware for request tracing
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"

    # Skip rate limiting for local development
    if client_ip in ["127.0.0.1", "localhost", "::1"]:
        response = await call_next(request)
        return response

    # Apply stricter rate limiting to suspicious patterns
    if request.url.path in ["/security.txt", "/robots.txt"]:
        max_requests, window = 10, 60  # Very limited for these endpoints
    elif request.url.path.startswith("/api/"):
        max_requests, window = 100, 60  # Standard API rate limit
    else:
        max_requests, window = 200, 60  # More generous for web pages

    if is_rate_limited(client_ip, max_requests, window):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(max_requests)
    response.headers["X-RateLimit-Window"] = str(window)
    return response

# Add CORS middleware - Secure configuration for Sacred Hive
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React development server
        "http://localhost:5173",    # Vite development server
        "http://localhost:5174",    # Vite development server (alt)
        "http://localhost:5175",    # Vite development server (alt2)
        "http://localhost:8080",    # Alternative dev server
        "https://chat.zae.life",    # Production domain
        "https://zae.life",         # Root domain
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

# Core HTML and WebSocket endpoints
# Security and standard web endpoints
@app.get("/favicon.ico")
async def get_favicon():
    """Serve favicon to prevent 404 errors."""
    return FileResponse("static/favicon.ico")

@app.get("/security.txt")
@app.get("/.well-known/security.txt")
async def get_security_txt():
    """Provide security contact information."""
    content = """Contact: mailto:security@zae.life
Expires: 2025-12-31T23:59:59Z
Acknowledgments: https://zae.life/security/acknowledgments
Preferred-Languages: en
Canonical: https://zae.life/.well-known/security.txt"""
    return PlainTextResponse(content, media_type="text/plain")

@app.get("/robots.txt")
async def get_robots_txt():
    """Provide robots.txt for web crawlers."""
    content = """User-agent: *
Allow: /
Sitemap: https://zae.life/sitemap.xml

# Hive Chat - A Living Application Ecosystem
# See https://github.com/zaebee/chat for more information"""
    return PlainTextResponse(content, media_type="text/plain")

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
                content = message_data.get("content", "")
                conn.execute("INSERT INTO messages (id, user_id, username, content, timestamp, room_id, sender_id, sender_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (message_id, user_id, username, content, timestamp, "general", user_id, username))
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
                    broadcast_data = {"type": "message", "message": message.model_dump()}
                    await manager.broadcast(json.dumps(broadcast_data))

                    if HIVE_AVAILABLE and manager.event_bus:
                        await manager.event_bus.publish_message_event("sent", message_id, message.model_dump())

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast_user_update()

@app.get("/health")
async def health_check():
    health_data = {
        "status": "healthy",
        "service": "hive-chat-main",
        "timestamp": datetime.now().isoformat(),
        "hive_integration": HIVE_AVAILABLE,
        "active_connections": len(manager.active_connections),
        "active_users": len(manager.users)
    }

    # Add detailed Hive status if available
    if HIVE_AVAILABLE and manager.event_bus:
        try:
            hive_status = manager.event_bus.get_status()
            health_data["hive_event_bus"] = {
                "subscriptions": hive_status.get("subscriptions_count", 0),
                "total_events": hive_status.get("total_events_processed", 0),
                "error_rate": hive_status.get("error_rate", 0),
                "health": hive_status.get("health", "unknown")
            }
        except Exception as e:
            health_data["hive_event_bus"] = {"error": str(e)}

    return health_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
