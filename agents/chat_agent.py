import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from pydantic import BaseModel
import logging # Added import

from agents.base_agent import BaseAgent

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

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.users: Dict[str, User] = {}

    async def connect(self, websocket: WebSocket, username: str, user_id: str, color: str):
        await websocket.accept()
        user = User(id=user_id, username=username, color=color)
        self.users[user_id] = user
        self.active_connections[user_id] = websocket
        return user

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.users:
            del self.users[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude_user_id: str = None):
        for user_id, connection in self.active_connections.items():
            if user_id != exclude_user_id:
                try:
                    await connection.send_text(message)
                except RuntimeError as e:
                    print("Unable send message:", e)

class ChatAgent(BaseAgent):
    def __init__(self, p2p_client: Any, event_bus: asyncio.Queue, logger: logging.Logger, fastapi_app: FastAPI):
        super().__init__(p2p_client, event_bus, logger)
        self.fastapi_app = fastapi_app
        self.connection_manager = ConnectionManager()
        self.setup_routes()

    def setup_routes(self):
        @self.fastapi_app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket, username: str = "Гость"):
            user_id = str(uuid.uuid4())
            color = f"#{hash(username) % 0xFFFFFF:06x}"
            user = await self.connection_manager.connect(websocket, username, user_id, color)
            self.logger.info(f"User {username} connected.")

            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)

                    if message_data["type"] == "message":
                        message = Message(
                            id=str(uuid.uuid4()),
                            text=message_data["data"]["text"],
                            sender_id=user.id,
                            sender_name=user.username,
                            timestamp=datetime.now().isoformat(),
                            is_bot=False,
                        )
                        # TODO: Save to DB
                        # TODO: Publish to P2P network

                        await self.connection_manager.broadcast(
                            json.dumps({"type": "message", "data": message.model_dump()})
                        )

            except WebSocketDisconnect:
                self.logger.info(f"User {user.username} disconnected.")
                self.connection_manager.disconnect(user.id)
                # TODO: Notify P2P network about user leaving
                # TODO: Update user list for remaining users

    def get_status(self) -> dict:
        status = super().get_status()
        status["active_connections"] = len(self.connection_manager.active_connections)
        return status