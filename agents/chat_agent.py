from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from database import get_db_connection

# Модели данных
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

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        user_id = str(uuid.uuid4())
        color = f"#{hash(username) % 0xFFFFFF:06x}"
        user = User(id=user_id, username=username, color=color)
        self.users[user_id] = user
        self.active_connections[user_id] = websocket

        # Отправляем историю сообщений новому пользователю
        conn = get_db_connection()
        messages = conn.execute("SELECT * FROM messages ORDER BY timestamp ASC").fetchall()
        conn.close()

        for message in messages:
            await self.send_personal_message(
                json.dumps({"type": "message", "data": dict(message)}), websocket
            )

        # Уведомляем других пользователей о новом участнике
        await self.broadcast(
            json.dumps({"type": "user_joined", "data": user.model_dump()}),
            exclude_user_id=user_id,
        )
        await self.broadcast(
            json.dumps(
                {
                    "type": "user_list",
                    "data": [u.model_dump() for u in self.users.values()],
                }
            ),
            exclude_user_id=user_id,
        )

        # Отправляем список активных пользователей
        await self.send_personal_message(
            json.dumps(
                {
                    "type": "user_list",
                    "data": [u.model_dump() for u in self.users.values()],
                }
            ),
            websocket,
        )

        return user

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.users:
            del self.users[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude_user_id: Optional[str] = None):
        for user_id, connection in self.active_connections.items():
            if user_id != exclude_user_id:
                try:
                    await connection.send_text(message)
                except RuntimeError as e:
                    print("Unable send message:", e)

    async def add_message(self, message: Message):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO messages (id, text, sender_id, sender_name, timestamp) VALUES (?, ?, ?, ?, ?)",
            (message.id, message.text, message.sender_id, message.sender_name, message.timestamp)
        )
        conn.commit()
        conn.close()

class ChatAgent:
    def __init__(self, event_bus, logger, app: FastAPI):
        self.event_bus = event_bus
        self.logger = logger
        self.app = app
        self.manager = ConnectionManager()
        self.templates = Jinja2Templates(directory="templates")

    def start(self):
        self.logger.info("ChatAgent started.")
        self.add_routes()

    def get_status(self):
        return {
            "name": "ChatAgent",
            "status": "running",
            "connected_users": len(self.manager.users)
        }

    def add_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def get_chat_page(request: Request):
            return self.templates.TemplateResponse("chat.html", {"request": request})

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket, username: str = "Гость"):
            user = await self.manager.connect(websocket, username)
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
                        await self.manager.add_message(message)
                        await self.manager.broadcast(
                            json.dumps({"type": "message", "data": message.model_dump()})
                        )

            except WebSocketDisconnect:
                await self.manager.broadcast(
                    json.dumps({"type": "user_left", "data": user.model_dump()})
                )
                self.manager.disconnect(user.id)
                await self.manager.broadcast(
                    json.dumps(
                        {
                            "type": "user_list",
                            "data": [u.model_dump() for u in self.manager.users.values()],
                        }
                    )
                )
