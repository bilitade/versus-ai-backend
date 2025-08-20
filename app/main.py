from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
from app.config import OPENROUTER_API_KEY


app = FastAPI(title="VersusAI Backend", version="0.1")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


class ChatRequest(BaseModel):
    model: str
    message: str

class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not set")

 
    messages = [
        {"role": "system", "content": "Your are AI Model. Your main Task is to answer"
        " anything the user asks!, Keep the answer simple & short"},
        {"role": "user", "content": request.message},
    ]

    try:
     
        completion = client.chat.completions.create(
            model=request.model,
            messages=messages,  # type: ignore
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "VersusAI",
            },
            extra_body={},
        )

        message_obj = completion.choices[0].message
        reply_text: str = getattr(message_obj, "content", "") or ""
        reply_text = reply_text.replace("<think>", "").replace("</think>", "").strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API Error: {str(e)}")

    return ChatResponse(reply=reply_text)
