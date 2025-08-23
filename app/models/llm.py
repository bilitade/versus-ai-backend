from sqlalchemy import Column, Integer, String
from app.database import Base

class LLM(Base):
    __tablename__ = "llms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    version = Column(String, nullable=False)