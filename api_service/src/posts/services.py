from typing import List, Optional
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.posts.schemas import PostCreate, PostUpdate
from src.posts.models import Post


class PostService:
    """
    Сервис позволяет выполнять CRUD операции над постами
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(
        self,
        post: PostCreate,
    ) -> Post:
        db_post = Post(**post.model_dump())
        self.session.add(db_post)
        await self.session.commit()
        await self.session.refresh(db_post)
        return db_post

    async def get_post(
        self,
        post_id: int,
    ) -> Optional[Post]:
        query = select(Post).where(Post.id == post_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_posts(self) -> List[Post]:
        query = select(Post).order_by(Post.created_at.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_post(
        self,
        post_id: int,
        post_data: PostUpdate,
    ) -> Optional[Post]:
        db_post = await self.get_post(post_id)
        if not db_post:
            return None

        for key, value in post_data.model_dump().items():
            setattr(db_post, key, value)

        await self.session.commit()
        await self.session.refresh(db_post)
        return db_post

    async def delete_post(
        self,
        post_id: int,
    ) -> bool:
        db_post = await self.get_post(post_id)
        if not db_post:
            return False

        await self.session.delete(db_post)
        await self.session.commit()
        return True
