from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi import Depends
from .services import PostService


async def get_post_service(
    session: AsyncSession = Depends(get_async_session),
) -> PostService:
    post_service = PostService(session=session)
    return post_service
