from datetime import datetime
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import SQLModel


if TYPE_CHECKING:
    from app.schemas.like import LikeRead
    from app.schemas.comment import CommentRead


class PostCreate(SQLModel):
    description: str
    user_id: uuid.UUID


class PostUpdate(SQLModel):
    description: Optional[str] = None


class PostRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0


class PostReadDetails(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    created_at: datetime
    likes: List['LikeRead'] = []
    comments: List['CommentRead'] = []


from app.schemas.like import LikeRead
from app.schemas.comment import CommentRead


PostReadDetails.model_rebuild()