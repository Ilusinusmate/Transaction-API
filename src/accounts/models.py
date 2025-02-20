from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Column, Integer, String, DateTime, ForeignKey, Relationship
from authuser.models import Users
from transactions.models import Operations


class AccountsBase(SQLModel):
    bank_name: str = Field(min_length=1, max_length=25)
    


class AccountsCreate(AccountsBase):
    pass

class Accounts(AccountsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: Decimal = Field(default=0, max_digits=15, decimal_places=2, ge=Decimal('0.00'))
    active: bool = Field(default=True)

    operations_released: List["Operations"] = Relationship(back_populates="account")
    
    user_id: int = Field(foreign_key='users.id')
    user: "Users" = Relationship(back_populates="accounts")
    
class AccountsPublic(AccountsBase):
    id: int
    balance: Decimal = Field(default=0, max_digits=15, decimal_places=2, ge=Decimal('0.00'))
    operations_released: List["Operations"]
    user_id: int
    active: bool