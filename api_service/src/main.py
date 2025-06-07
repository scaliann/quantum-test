from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.models import Base
from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI()


@app.get("/")
async def start_message():
    return {"message": "hello"}
