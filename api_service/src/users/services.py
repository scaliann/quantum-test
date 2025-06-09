from sqlalchemy import Result, select
from src.users.models import User
from src.users.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.password import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        user_data: UserCreate,
    ) -> User:
        email: str = user_data.email
        password: str = get_password_hash(user_data.password)
        user = User(email=email, password=password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(
        self,
        email: str,
    ) -> User:
        query = select(User).where(User.email == email)
        reusult: Result = await self.session.execute(query)
        user: User = reusult.scalar_one_or_none()
        return user

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User:
        query = select(User).where(User.id == user_id)
        result: Result = await self.session.execute(query)
        user: User = result.scalar_one_or_none()
        return user
