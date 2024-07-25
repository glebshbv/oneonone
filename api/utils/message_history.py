from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.models.message_history import MessageHistory
from schemas.message_history import MessageHistoryCreate, MessageHistoryBase

def get_message_history(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MessageHistory).offset(skip).limit(limit).all()


def get_message_history_by_user_id(db: Session, user_id: int) -> List[MessageHistoryBase]:
    messages = db.query(MessageHistory).filter(MessageHistory.user_id == user_id).all()
    return [MessageHistoryBase(role=message.role, content=message.content) for message in messages]


def create_message_history(db: Session, message_history: MessageHistoryCreate):
    try:
        db_message = MessageHistory(
            role=message_history.role,
            content=message_history.content,
            user_id=message_history.user_id
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except IntegrityError as e:
        db.rollback()
        print(f"IntegrityError: {str(e)}")
        return None