import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.db import init_db
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    # before api starts
    init_db()
    yield
    # after api starts

app = FastAPI(lifespan=lifespan)

app.include_router(chat_router, prefix="/api/chats", tags=["chats"])

API_KEY = os.environ.get('API_KEY')
MY_PROJECT = os.environ.get('MY_PROJECT') or "This is my project"

if not API_KEY:
    raise NotImplementedError('API KEY not set')

@app.get("/")
def read_index():
    return {'hello': "Hello World", "project_name": MY_PROJECT}

# @app.get("/health")
# def read_index():
#     return {'hello': "Hello World", "project_name": MY_PROJECT}