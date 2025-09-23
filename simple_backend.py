#!/usr/bin/env python3
"""
Simple Backend for Testing Purified Frontend Components
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from typing import Dict, List

app = FastAPI(title="Simple Hive Backend")

# Simple connection manager for WebSocket
class SimpleConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.users[user_id] = {
            "id": user_id,
            "name": username,
            "websocket": websocket
        }
        
        # Send user list to all clients
        await self.broadcast_user_list()

    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.users:
            del self.users[user_id]

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

    async def broadcast_user_list(self):
        user_list = [{"id": uid, "name": user["name"]} for uid, user in self.users.items()]
        await self.broadcast(json.dumps({
            "type": "user_list",
            "data": user_list
        }))

manager = SimpleConnectionManager()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Simple Hive Backend Running", "status": "active"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "backend": "simple"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str, user_id: str):
    await manager.connect(websocket, user_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "message":
                # Simple message broadcast
                broadcast_data = {
                    "type": "message",
                    "data": {
                        "id": f"msg_{len(manager.active_connections)}",
                        "text": message_data.get("content", ""),
                        "sender_id": user_id,
                        "sender_name": username,
                        "timestamp": "2024-01-01T00:00:00Z",
                        "is_bot": False
                    }
                }
                await manager.broadcast(json.dumps(broadcast_data))
                
            elif message_data.get("type") == "reaction":
                # Handle reactions
                reaction_data = {
                    "type": "reaction",
                    "messageId": message_data.get("messageId"),
                    "emoji": message_data.get("emoji"),
                    "userId": message_data.get("userId"),
                    "userName": message_data.get("userName"),
                    "action": message_data.get("action")
                }
                await manager.broadcast(json.dumps(reaction_data))
                
            elif message_data.get("type") == "typing":
                # Handle typing indicators
                typing_data = {
                    "type": "typing",
                    "userId": message_data.get("userId"),
                    "userName": message_data.get("userName"),
                    "isTyping": message_data.get("isTyping")
                }
                await manager.broadcast(json.dumps(typing_data))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast_user_list()

@app.get("/api/hive/teammates")
async def get_teammates():
    return {
        "teammates": [
            {
                "id": "data_aggregator_1",
                "name": "DataAggregator",
                "type": "aggregate",
                "status": "active",
                "capabilities": ["data_organization", "structural_analysis"],
                "active_tasks": 0,
                "health": "excellent"
            },
            {
                "id": "data_transformer_1", 
                "name": "DataTransformer",
                "type": "transformation",
                "status": "active",
                "capabilities": ["data_transformation", "processing"],
                "active_tasks": 0,
                "health": "excellent"
            },
            {
                "id": "data_connector_1",
                "name": "DataConnector", 
                "type": "connector",
                "status": "active",
                "capabilities": ["websocket_communication", "protocol_translation"],
                "active_tasks": 0,
                "health": "excellent"
            },
            {
                "id": "data_generator_1",
                "name": "DataGenerator",
                "type": "generator", 
                "status": "active",
                "capabilities": ["content_generation", "data_creation"],
                "active_tasks": 0,
                "health": "excellent"
            }
        ],
        "total": 4,
        "active": 4,
        "purification_status": "complete"
    }

if __name__ == "__main__":
    print("🚀 Starting Simple Backend for Purified Frontend Testing")
    print("📊 API: http://localhost:8000")
    print("🔗 Teammates: http://localhost:8000/api/hive/teammates")
    uvicorn.run(app, host="0.0.0.0", port=8000)