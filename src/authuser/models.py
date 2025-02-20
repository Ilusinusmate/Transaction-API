from typing import List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
import datetime


class UsersBase(SQLModel):
    
    email: EmailStr = Field(unique=True)
    
    date_joined: datetime.date = Field(
        default_factory=datetime.datetime.now
    )


class Users(UsersBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    
    password: bytes
    accounts: List["Accounts"] = Relationship(back_populates="user")
    is_active: bool = Field(default=True)
    
    
class UsersPublic(UsersBase):
    id: int
    accounts: List[int]
    