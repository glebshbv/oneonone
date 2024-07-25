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

    def to_dict(self, include_id=True, include_timestamps=True, include_user_id=True):
        data = {
            "role": self.role,
            "content": self.content,
        }
        if include_id:
            data["id"] = self.id
        if include_user_id:
            data["user_id"] = self.user_id
        if include_timestamps:
            data["created_at"] = self.created_at
            data["updated_at"] = self.updated_at
        return data
