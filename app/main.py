from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.config import OPENROUTER_API_KEY

app = FastAPI(title="VersusAI Backend", version="0.1")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY must be set")

def create_openai_model(model_name: str) -> OpenAIModel:
    return OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        ),
    )

default_model = create_openai_model("openai/gpt-oss-20b:free")
agent: Agent = Agent(default_model)

class ChatRequest(BaseModel):
    model: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    active_agent: Agent
    if request.model:
        if not request.model.strip():
            raise HTTPException(status_code=400, detail="Model name cannot be empty")
        try:
            override_model = create_openai_model(request.model)
            active_agent = Agent(override_model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid model name: {str(e)}")
    else:
        active_agent = agent

    try:
        run_result = await active_agent.run(request.message)
        reply_text: str = str(run_result.output) if run_result.output is not None else ""
        reply_text = reply_text.replace("<think>", "").replace("</think>", "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")

    return ChatResponse(reply=reply_text)
