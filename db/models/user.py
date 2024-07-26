from sqlalchemy import Column, Integer, String, JSON, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db.database import Base
from .mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, unique=True)
    user_info = Column(JSON)

    message_history = relationship("MessageHistory", back_populates="owner")

