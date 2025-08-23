from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.message import MessageResponse

class ChatCreate(BaseModel):
    title: Optional[str] = None  
class ChatResponse(BaseModel):
    id: int
    timestamp: datetime
    user_id: int
    title: str
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True