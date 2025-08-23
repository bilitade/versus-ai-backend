from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.llm import LLMCreate, LLMResponse
from app.crud.llm_crud import create_llm, get_llms
from typing import List

router = APIRouter(prefix="/v1/llms", tags=["llms"])

@router.post("/", response_model=LLMResponse)
def create_new_llm(llm: LLMCreate, db: Session = Depends(get_db)):
    return create_llm(db, llm)

@router.get("/", response_model=List[LLMResponse])
def get_llms_list(db: Session = Depends(get_db)):
    llms = get_llms(db)
    if not llms:
        return []
    return llms