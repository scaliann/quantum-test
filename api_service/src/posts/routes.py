from typing import List
from fastapi import APIRouter, Depends, HTTPException

from .schemas import Post, PostCreate, PostUpdate
from .services import PostService
from .dependencies import get_post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post)
async def create_post(
    post: PostCreate,
    post_service: PostService = Depends(get_post_service),
) -> Post:
    return await post_service.create_post(post)


@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
) -> Post:
    post = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/", response_model=List[Post])
async def get_posts(
    post_service: PostService = Depends(get_post_service),
) -> List[Post]:
    return await post_service.get_posts()


@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    post_service: PostService = Depends(get_post_service),
) -> Post:
    post = await post_service.update_post(post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
) -> dict:
    deleted = await post_service.delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
