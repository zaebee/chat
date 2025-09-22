from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    color: str

class UserCreate(BaseModel):
    id: str
    username: str
    email: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    experience: Optional[int] = None
    level: Optional[int] = None
    stats: Optional[dict] = None

class Message(BaseModel):
    id: str
    user_id: str
    username: str
    content: str
    timestamp: str
    color: str

class OrganellaCreate(BaseModel):
    user_id: str
    name: str
    type: str
    stage: str = "egg"
    skills: Optional[dict] = None
    mystical_appearance: Optional[str] = None

class OrganellaUpdate(BaseModel):
    name: Optional[str] = None
    stage: Optional[str] = None
    level: Optional[int] = None
    experience_points: Optional[int] = None
    skills: Optional[dict] = None
    mystical_appearance: Optional[str] = None
    unlocked_sections: Optional[list] = None
