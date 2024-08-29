from schemas.telegram_message import TelegramMessage
from schemas.message_history import MessageHistoryCreate
from api.utils.users import get_user_by_chat_id, create_user
from api.utils.message_history import create_message_history
from db.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate
import os
from dotenv import load_dotenv
load_dotenv()

class MessageHandler:

    DEFAULT_TEXT = os.getenv('DEFAULT_PROMPT')

    def __init__(self, telegram_message: TelegramMessage, db: Session):
        self.db = db
        self.telegram_message = telegram_message
        self.chat_id = None
        self.text = None
        self.user_id = None
        self.user_info = None
        self.default_text = MessageHandler.DEFAULT_TEXT

    async def receive_message(self) -> int:
        self._extract_data_from_telegram_message(self.telegram_message)
        if not self._check_if_user_exist():
            self._create_new_user()
            self._create_context_message()
        if not self._check_remaining_tokens():
            print("not enough tokens")
            raise HTTPException(status_code=400, detail="Insufficient tokens")
        self._add_user_message_to_db()
        return int(self.user_id) if self.user_id else None

    def _create_new_user(self):
        user = UserCreate(chat_id=self.chat_id, user_info=self.user_info)
        new_user = create_user(db=self.db, user=user)
        self.user_id = new_user.id if new_user else None
        return new_user

    def _create_context_message(self):
        message = MessageHistoryCreate(
            role="assistant",
            content=self.default_text,
            user_id=self.user_id
        )
        create_message_history(db=self.db, message_history=message)
        return message

    def _extract_data_from_telegram_message(self, telegram_message: TelegramMessage):
        self.chat_id = telegram_message['message']['chat']['id']
        self.text = telegram_message['message'].get('text', '')
        self.user_info = telegram_message['message']['from']
        return self.chat_id, self.text

    def _check_if_user_exist(self):
        user = get_user_by_chat_id(db=self.db, chat_id=self.chat_id)
        self.user_id = user.id if user else None
        return self.user_id

    def _add_user_message_to_db(self):
        message = MessageHistoryCreate(
            role="user",
            content=self.text,
            user_id=self.user_id
        )
        create_message_history(db=self.db, message_history=message)
        return message

    def _check_remaining_tokens(self):
        return True

