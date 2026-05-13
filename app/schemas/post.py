from datetime import datetime
import uuid
from typing import Optional

from sqlmodel import SQLModel


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
