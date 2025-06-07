from sqlalchemy.ext.asyncio import AsyncSession
from api_service.src.posts.schemas import PostCreate
from src.posts.models import Post


class PostServise:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(
        self,
        post_in: PostCreate,
    ) -> Post:
        post = Post(**post_in.model_dump())
        self.session.add(post)
        await self.session.commit()
        return post
