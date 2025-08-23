from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    message_sequence = Column(Integer, nullable=False)
    is_model = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    content = Column(String, nullable=False)
    chat = relationship("Chat", back_populates="messages")