from functools import wraps
from fastapi import HTTPException, status


def require_auth():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")

            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Необходима аутентификация для выполнения операции",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
