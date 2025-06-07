from fastapi import FastAPI
from contextlib import asynccontextmanager

from api_service.src.models import Base
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI()
