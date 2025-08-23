from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.chat import ChatCreate, ChatResponse
from app.schemas.message import MessageCreate, MessageResponse
from app.crud.chat_crud import create_chat, get_chats
from app.crud.message_crud import create_message, get_messages
from app.services.chat_service import process_message
from app.models.chat import Chat

router = APIRouter(prefix="/v1/chats", tags=["chats"])

@router.post("/", response_model=ChatResponse)
def create_new_chat(chat: ChatCreate, user_id: int = 1, db: Session = Depends(get_db)):
    return create_chat(db, chat, user_id)

@router.get("/", response_model=List[ChatResponse])
def get_user_chats(user_id: int = 1, db: Session = Depends(get_db)):
    return get_chats(db, user_id)

@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = get_messages(db, chat_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat")
    return messages

@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(chat_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        chat_create = ChatCreate(title=None)
        chat = create_chat(db, chat_create, user_id=1, first_message=message.content)
    
    user_message = create_message(db, chat_id, message, is_model=False)
    
    if message.model_id:
        reply_text = await process_message(db, message.content, message.model_id) # type: ignore
        model_message = MessageCreate(content=reply_text, model_id=message.model_id)
        return create_message(db, chat_id, model_message, is_model=True)
    
    return user_message
