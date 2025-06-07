from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi import Depends
from .services import PostServise


async def get_post_service(
    session: AsyncSession = Depends(get_async_session),
) -> PostServise:
    post_service = PostServise(session=session)
    return post_service
