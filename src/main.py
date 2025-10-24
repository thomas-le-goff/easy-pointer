from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import actions as auth_actions
from .user import actions as user_actions
from .editor import actions as editor_actions

from .database import setup


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_actions.router)
app.include_router(user_actions.router)
app.include_router(editor_actions.router)
