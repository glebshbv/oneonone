from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from db.database  import Base
from .mixins import Timestamp

class MessageHistory(Timestamp, Base):
    __tablename__ = "message_history"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="message_history")