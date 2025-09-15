
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env'))

from fastapi import FastAPI
from .routers.chatwoot_agentbot import router as chatwoot_router

# configure logging and middlewares early
from app.core.logging import configure_logging
from app.core.middlewares import add_middlewares


configure_logging()

app = FastAPI(title="Mr. DOM SDR API")

add_middlewares(app)

app.include_router(chatwoot_router)

@app.get("/health")
def health():
    return {"ok": True}
