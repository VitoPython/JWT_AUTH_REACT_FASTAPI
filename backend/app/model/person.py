from datetime import date, datetime
from typing import Optional
from sqlalchemy import Enum as SQLAlchemyEnum, Column, DateTime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class Person(SQLModel, table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    birth: date
    sex: Sex = Field(sa_column=Column(SQLAlchemyEnum(Sex), nullable=False))
    profile: str
    phone_number: str

    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, nullable=False)
    )
    modified_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(DateTime, onupdate=datetime.now, nullable=False)
    )

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="person"
    )

    # Дополнительная настройка для поддержки Enum
    class Config:
        arbitrary_types_allowed = True
