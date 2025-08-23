from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate
from sqlalchemy.sql import func

def create_message(db: Session, chat_id: int, message: MessageCreate, is_model: bool = False):
    # Get the next sequence number for the chat
    max_sequence = db.query(func.max(Message.message_sequence)).filter(Message.chat_id == chat_id).scalar() or 0
    db_message = Message(
        chat_id=chat_id,
        message_sequence=max_sequence + 1,
        is_model=is_model,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, chat_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.message_sequence).offset(skip).limit(limit).all()