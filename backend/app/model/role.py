from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Relationship
from app.model.user_role import UsersRole

class Role(SQLModel, table=True):
    __tablename__ = "role"

    id: Optional[str] = Field(None, primary_key=True, nullable=True)
    role_name: str

    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, nullable=False)
    )
    modified_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, onupdate=datetime.now, nullable=False)
    )

    users: List["Users"] = Relationship(back_populates="roles", link_model=UsersRole)
