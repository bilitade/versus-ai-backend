from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.schemas.chat import ChatCreate
from datetime import datetime, timezone

from typing import Optional

def create_chat(db: Session, chat: ChatCreate, user_id: int, first_message: Optional[str] = None): 

    title = chat.title if chat.title else generate_title(first_message)
    db_chat = Chat(title=title, user_id=user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chats(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Chat).filter(Chat.user_id == user_id).offset(skip).limit(limit).all()

from typing import Optional

def generate_title(first_message: Optional[str] = None) -> str: 
    if first_message:

        clean_message = "".join(c for c in first_message if c.isalnum() or c.isspace())[:30]
        return clean_message or f"Chat {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"
    return f"Chat {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"