from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    color: str

class Message(BaseModel):
    id: str
    user_id: str
    username: str
    content: str
    timestamp: str
    color: str
