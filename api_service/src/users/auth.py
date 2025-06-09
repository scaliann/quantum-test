from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import EmailStr
from src.config import get_auth_data
from src.users.services import UserService
from src.users.password import verify_password


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    return encode_jwt


async def authenticate_user(
    email: EmailStr,
    password: str,
    user_service: UserService,
):
    user = await user_service.get_user_by_email(email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user
