from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime, String
from sqlmodel import SQLModel, Field, Relationship
from app.model.user_role import UsersRole

class Users(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str

    person_id: Optional[str] = Field(default=None, foreign_key="person.id")
    person: Optional["Person"] = Relationship(back_populates="users")

    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, nullable=False)
    )
    modified_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, onupdate=datetime.now, nullable=False)
    )

    roles: List["Role"] = Relationship(back_populates="users", link_model=UsersRole)
