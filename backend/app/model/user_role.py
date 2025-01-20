from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field

class UsersRole(SQLModel, table=True):
    __tablename__ = "user_role"

    users_id: Optional[str] = Field(default=None, foreign_key="users.id", primary_key=True)
    role_id: Optional[str] = Field(default=None, foreign_key="role.id", primary_key=True)

    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, nullable=False)
    )
    modified_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, onupdate=datetime.now, nullable=False)
    )
