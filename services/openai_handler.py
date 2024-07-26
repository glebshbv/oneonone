from sqlalchemy.orm import Session
from api.utils.message_history import get_message_history_by_user_id, create_message_history
from schemas.message_history import MessageHistoryCreate
from openai import OpenAI


class OpenAIHandler:
    def __init__(self, user_id: int, db: Session):
        self.db = db
        self.client = OpenAI()
        self.user_id = user_id
        self.message_history = {}
        self.chat_response = None

    async def messages(self):
        return self._ask_openai()

    def _retrieve_messages(self):
        message_history_objects = get_message_history_by_user_id(db=self.db, user_id=self.user_id)
        self.message_history = [message.dict() for message in message_history_objects]
        return self.message_history

    def _ask_openai(self):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self._retrieve_messages(),
            temperature=0.8
        )
        self.chat_response = response.choices[0].message.content.strip()
        self._update_message_history()
        return self.chat_response

    def _update_message_history(self):
        message = MessageHistoryCreate(
            role="assistant",
            content=self.chat_response,
            user_id=self.user_id
        )
        create_message_history(db=self.db, message_history=message)
        return message