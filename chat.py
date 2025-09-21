import uvicorn
<<<<<<< HEAD
import asyncio
from typing import List, Dict, Optional
import json
import os
import uuid
import argparse
from datetime import datetime
from contextlib import asynccontextmanager
from database import init_db, get_db_connection
import websockets.exceptions
from host import HiveHost


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation de la base de données au démarrage
    init_db()
    yield


# Инициализация FastAPI
app = FastAPI(lifespan=lifespan)

# Настройка шаблонов и статики
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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


class ChallengeSolution(BaseModel):
    user_id: str
    challenge_id: str


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.users: Dict[str, User] = {}

    async def connect(self, websocket: WebSocket, username: str, user_id: Optional[str] = None):
        await websocket.accept()
        if user_id is None:
            user_id = str(uuid.uuid4())
        color = f"#{hash(username) % 0xFFFFFF:06x}"
        user = User(id=user_id, username=username, color=color)
        self.users[user_id] = user
        self.active_connections[user_id] = websocket

        # Отправляем историю сообщений новому пользователю
        conn = get_db_connection()
        messages = conn.execute(
            "SELECT * FROM messages ORDER BY timestamp ASC"
        ).fetchall()
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
        await manager.broadcast(
            json.dumps(
                {
                    "type": "user_list",
                    "data": [u.model_dump() for u in manager.users.values()],
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
                except (RuntimeError, websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError) as e:
                    print("Unable send message:", e)

    async def add_message(self, message: Message):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO messages (id, text, sender_id, sender_name, timestamp) VALUES (?, ?, ?, ?, ?)",
            (
                message.id,
                message.text,
                message.sender_id,
                message.sender_name,
                message.timestamp,
            ),
        )
        conn.commit()
        conn.close()


manager = ConnectionManager()


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/solve_challenge")
async def solve_challenge(solution: ChallengeSolution):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO user_progress (user_id, challenge_id, solved_at) VALUES (?, ?, ?)",
            (solution.user_id, solution.challenge_id, datetime.now().isoformat()),
        )
        conn.commit()
        return {"message": "Challenge solution recorded successfully"}
    except sqlite3.IntegrityError:
        return {"message": "Challenge already solved by this user"}
    finally:
        conn.close()


@app.get("/api/user_progress/{user_id}")
async def get_user_progress(user_id: str):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT challenge_id FROM user_progress WHERE user_id = ?", (user_id,)
        )
        solved_challenge_ids = [row[0] for row in cursor.fetchall()]
        return {"user_id": user_id, "solved_challenge_ids": solved_challenge_ids}
    finally:
        conn.close()


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str = "Гость", user_id: Optional[str] = None):
    user = await manager.connect(websocket, username, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data["type"] == "message":
                # Создаем сообщение
                message = Message(
                    id=str(uuid.uuid4()),
                    text=message_data["data"]["text"],
                    sender_id=user.id,
                    sender_name=user.username,
                    timestamp=datetime.now().isoformat(),
                    is_bot=False,
                )

                # Добавляем сообщение в историю и обрабатываем
                await manager.add_message(message)

                # Отправляем сообщение всем пользователям
                await manager.broadcast(
                    json.dumps({"type": "message", "data": message.model_dump()})
                )

    except WebSocketDisconnect:
        # Уведомляем других пользователей о выходе
        await manager.broadcast(
            json.dumps({"type": "user_left", "data": user.model_dump()})
        )
        manager.disconnect(user.id)
        await manager.broadcast(
            json.dumps(
                {
                    "type": "user_list",
                    "data": [u.model_dump() for u in manager.users.values()],
                }
            )
        )


# Запуск сервера
=======
import argparse
from host import app, host

>>>>>>> main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the web server on")
    args = parser.parse_args()

<<<<<<< HEAD
    # Create HiveHost instance
    host = HiveHost()

=======
>>>>>>> main
    async def startup():
        await host.lifespan_startup()

    app.add_event_handler("startup", startup)

    async def shutdown():
        await host.lifespan_shutdown()

    app.add_event_handler("shutdown", shutdown)

    uvicorn.run(app, host="0.0.0.0", port=args.port)
