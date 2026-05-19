from typing import List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.schemas.post import PostRead


async def posts_to_read_list(posts: List[Post], session: AsyncSession) -> List[PostRead]:
    if not posts:
        return []

    post_ids = [post.id for post in posts]

    likes_result = await session.execute(
        select(Like.post_id, func.count())
        .where(Like.post_id.in_(post_ids))
        .group_by(Like.post_id)
    )
    likes_map = {row[0]: row[1] for row in likes_result.all()}

    comments_result = await session.execute(
        select(Comment.post_id, func.count())
        .where(Comment.post_id.in_(post_ids))
        .group_by(Comment.post_id)
    )
    comments_map = {row[0]: row[1] for row in comments_result.all()}

    return [
        PostRead(
            id=post.id,
            user_id=post.user_id,
            description=post.description,
            created_at=post.created_at,
            likes_count=likes_map.get(post.id, 0),
            comments_count=comments_map.get(post.id, 0),
        )
        for post in posts
    ]
