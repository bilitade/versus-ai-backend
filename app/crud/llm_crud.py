from sqlalchemy.orm import Session
from app.models.llm import LLM
from app.schemas.llm import LLMCreate
from fastapi import HTTPException

def create_llm(db: Session, llm: LLMCreate):
    existing_llm = db.query(LLM).filter(LLM.name == llm.name).first()
    if existing_llm:
        raise HTTPException(status_code=400, detail="Model name already exists")
    
    db_llm = LLM(name=llm.name, version=llm.version)
    db.add(db_llm)
    db.commit()
    db.refresh(db_llm)
    return db_llm

def get_llms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LLM).offset(skip).limit(limit).all()