from datetime import datetime

from pydantic import BaseModel
from typing import Dict, Any, List

from schemas.message_history import MessageHistory


class UserBase(BaseModel):
    chat_id: int
    user_info: Dict[str, Any]
    class Config:
        arbitrary_types_allowed = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    message_history: List[MessageHistory] = []  # Ensure this is a list of MessageHistory
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
