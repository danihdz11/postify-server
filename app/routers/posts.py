from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostRead])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostRead)
async def get_post_by_id(post_id: UUID, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("/", response_model=PostCreate, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate, session: AsyncSession = Depends(get_session)):
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: UUID,
    data: PostUpdate,
    session: AsyncSession = Depends(get_session),
):
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: UUID, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await session.delete(post)
    await session.commit()
