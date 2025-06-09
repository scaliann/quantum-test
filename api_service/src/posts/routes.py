from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.users.auth_utils import get_current_user
from .schemas import Post, PostCreate, PostUpdate
from .services import PostService
from .dependencies import get_post_service
from .permissions import require_auth

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post)
@require_auth()
async def create_post(
    post: PostCreate,
    post_service: PostService = Depends(get_post_service),
    current_user=Depends(get_current_user),
) -> Post:
    return await post_service.create_post(post)


@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
) -> Post:
    post = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден",
        )
    return post


@router.get("/", response_model=List[Post])
async def get_posts(
    post_service: PostService = Depends(get_post_service),
) -> List[Post]:
    return await post_service.get_posts()


@router.put("/{post_id}", response_model=Post)
@require_auth()
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    post_service: PostService = Depends(get_post_service),
    current_user=Depends(get_current_user),
) -> Post:
    post = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден",
        )
    return await post_service.update_post(post_id, post_data)


@router.delete("/{post_id}")
@require_auth()
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user=Depends(get_current_user),
) -> dict:
    post = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден",
        )
    await post_service.delete_post(post_id)
    return {"message": "Пост успешно удален"}
