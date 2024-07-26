from pydantic import BaseModel

class TelegramMessage(BaseModel):
    update_id: int
    message: dict