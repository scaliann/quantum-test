from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.users.auth import authenticate_user, create_access_token
from src.users.auth_utils import get_current_user, get_user_service
from src.users.schemas import UserAuth, UserCreate, UserRead, UserResponse
from src.users.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Зарегистрироваться",
    description="""
Регистрация осуществляется путем ввода email и пароля.
""",
)
async def register_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    user = await user_service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )
    user = await user_service.create_user(user_data)
    return user


@router.post(
    "/login/",
    summary="Войти в аккаунт",
    description="""
Вход осуществляется путем ввода email и пароля.
""",
)
async def auth_user(
    response: Response,
    user_data: UserAuth,
    user_service: UserService = Depends(get_user_service),
):
    user = await authenticate_user(
        email=user_data.email, password=user_data.password, user_service=user_service
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Только для HTTPS
        samesite="lax",  # Защита от CSRF
    )
    return {"access_token": access_token, "refresh_token": None}


@router.post(
    "/logout",
    summary="Выйти из аккаунта",
)
async def logout(
    response: Response,
    current_user=Depends(get_current_user),
):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Успешный выход из системы"}
