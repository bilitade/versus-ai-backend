from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.config import OPENROUTER_API_KEY
from sqlalchemy.orm import Session
from app.models.llm import LLM
from fastapi import HTTPException

def create_openai_model(model_name: str) -> OpenAIModel:
    return OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        ),
    )

from typing import Optional

async def process_message(db: Session, message_content: str, model_id: Optional[int] = None):
 
    model = db.query(LLM).filter(LLM.id == model_id).first() if model_id else db.query(LLM).first()
    if not model:
        raise HTTPException(status_code=400, detail="Invalid or missing model ID")

    try:
        agent = Agent(create_openai_model(getattr(model, "name")))
        run_result = await agent.run(str(message_content))
        reply_text = str(run_result.output) if run_result.output is not None else ""
        reply_text = reply_text.replace("<think>", "").replace("</think>", "").strip()
        return reply_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")