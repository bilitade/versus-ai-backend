from fastapi import FastAPI
from app.routes import chats, users, llms


app = FastAPI(title="VersusAI Backend", version="0.1")

# Include routers
app.include_router(chats.router)
app.include_router(users.router)
app.include_router(llms.router)
