from pydantic import BaseModel

class LLMCreate(BaseModel):
    name: str
    version: str

class LLMResponse(BaseModel):
    id: int
    name: str
    version: str

    class Config:
        from_attributes = True