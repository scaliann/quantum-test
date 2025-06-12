from datetime import datetime, timezone
from typing import Optional, Tuple

from fastapi import Cookie, Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from src.config import settings
from src.database import get_async_session
from src.users.services import UserService


def get_cookie_signer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.SECRET_KEY, salt="cookie-salt")


def sign_data(data: str) -> str:
    signer = get_cookie_signer()
    return signer.dumps(data)


def unsign_data(signed_data: str, max_age: int = 30 * 24 * 60 * 60) -> Tuple[str, bool]:
    signer = get_cookie_signer()
    try:
        data = signer.loads(signed_data, max_age=max_age)
        return data, True
    except SignatureExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cookie истекла")
    except BadSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидная cookie")


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)


async def get_current_user_id(
    request: Request,
    access_token: Optional[str] = Cookie(None),
) -> int:
    # Пытаемся получить токен
    token = access_token

    # Если нет токена, пытаемся получить из заголовка
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходима аутентификация для выполнения операции",
        )

    try:
        # Если токен из cookie, проверяем его подпись
        if access_token:
            token, _ = unsign_data(token)

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось подтвердить учетные данные",
            )
        # Проверяем срок действия токена
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) >= exp_datetime:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось подтвердить учетные данные"
        )


async def get_current_user(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    access_token: Optional[str] = Cookie(None),
):
    user_id = await get_current_user_id(request, access_token)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден"
        )
    return user
