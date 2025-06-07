from typing import List
import aiohttp
from .schemas import Post
from .config import settings


class PostAPIClient:
    def __init__(
        self,
        base_url: str = settings.API_URL,
    ):
        self.base_url = base_url

    async def get_posts(
        self,
    ) -> List[Post]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/posts") as response:
                data = await response.json()
                return [Post(**post) for post in data]

    async def get_post(
        self,
        post_id: int,
    ) -> Post:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/posts/{post_id}") as response:
                data = await response.json()
                return Post(**data)
