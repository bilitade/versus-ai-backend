from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    model_id: Optional[int] = None  

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    message_sequence: int
    is_model: bool
    timestamp: datetime
    content: str

    class Config:
        from_attributes = True