import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str
    name: str
    lastname: str
    email: str
    password: str


class UserUpdate(SQLModel):
    username: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserRead(SQLModel):
    id: uuid.UUID
    username: str
    name: str
    lastname: str
    email: str
    created_at: datetime