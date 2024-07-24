from sqlalchemy.orm import Session

from db.models.user import User
from schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_chat_id(db: Session, chat_id: str):
    return db.query(User).filter(User.chat_id == chat_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(chat_id=user.chat_id, user_info=user.user_info)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
