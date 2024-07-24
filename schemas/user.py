from datetime import datetime

from pydantic import BaseModel
from typing import Dict, Any

class UserBase(BaseModel):
    chat_id: int
    user_info: Dict[str, Any]


class UserCreate(UserBase):
    ...

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True