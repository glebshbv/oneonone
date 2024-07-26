import os
from dotenv import load_dotenv
import httpx
from fastapi import HTTPException

from api.utils.users import get_chat_id_by_user_id
from sqlalchemy.orm import Session
load_dotenv()

class TelegramHandler:
    def __init__(self, user_id: int, db: Session):
        self.db = db
        self.telegram_api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
        self.telegram_voice_api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendVoice"
        self.user_id = user_id
        self.voice_file_url = None
        self.chat_id = self._get_chat_id()

    def send_voice_message(self, voice_file_url: str):
        self.voice_file_url = voice_file_url
        return self._execute_telegram_voice_message()

    def _get_chat_id(self):
        return get_chat_id_by_user_id(db=self.db, user_id=self.user_id)

    async def _execute_telegram_voice_message(self):
        async with httpx.AsyncClient() as asyncclient:
            data = {
                'chat_id': self.chat_id,
                'voice': self.voice_file_url
            }
            response = await asyncclient.post(self.telegram_voice_api_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to send voice message")
        return response.json()

    async def send_telegram_message(self, chat_id: int, text: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.telegram_api_url,
                json={"chat_id": chat_id, "text": text}
            )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to send voice message")
        return response.json()
