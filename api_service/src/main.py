from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.models import Base
from src.database import engine
from src.posts.routes import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(title="Posts API", lifespan=lifespan)

app.include_router(posts_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Posts API"}
