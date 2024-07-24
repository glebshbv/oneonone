from datetime import datetime

from pydantic import BaseModel
from typing import Dict, Any


class MessageHistoryBase(BaseModel):
    role: str
    content: str
    class Config:
        arbitrary_types_allowed = True


class MessageHistoryCreate(MessageHistoryBase):
    user_id: int
    pass


class MessageHistory(MessageHistoryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True