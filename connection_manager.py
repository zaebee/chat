from typing import List, Dict
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime

from models import User

try:
    from hive.events import HiveEventBus
    from hive.team_communication import SacredTeamCommunication
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False

class HiveConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users: Dict[str, User] = {}

        if HIVE_AVAILABLE:
            self.event_bus = HiveEventBus()
            self.sacred_communication = SacredTeamCommunication(self.event_bus)
            self.sacred_communication.set_websocket_callback(self.broadcast)
        else:
            self.event_bus = None
            self.sacred_communication = None

    async def connect(self, websocket: WebSocket, user_id: str, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)

        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#FF9FF3", "#54A0FF"]
        color = colors[len(self.users) % len(colors)]

        self.users[user_id] = User(id=user_id, username=username, color=color)

        await self.broadcast_user_update()

        if self.event_bus:
            await self.event_bus.publish_user_event("connected", user_id, {
                "username": username,
                "timestamp": datetime.now().isoformat()
            })

    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.users:
            username = self.users[user_id].username
            del self.users[user_id]

            if self.event_bus:
                asyncio.create_task(self.event_bus.publish_user_event("disconnected", user_id, {
                    "username": username,
                    "timestamp": datetime.now().isoformat()
                }))

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

    async def broadcast_user_update(self):
        user_list = list(self.users.values())
        update_message = {
            "type": "user_update",
            "users": [user.dict() for user in user_list]
        }
        await self.broadcast(json.dumps(update_message))

manager = HiveConnectionManager()
