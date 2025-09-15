
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env'))

from fastapi import FastAPI
from .routers.chatwoot_agentbot import router as chatwoot_router

app = FastAPI(title="Mr. DOM SDR API")
app.include_router(chatwoot_router)

@app.get("/health")
def health():
    return {"ok": True}
