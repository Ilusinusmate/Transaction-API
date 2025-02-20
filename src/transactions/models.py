import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
import enum

from sqlmodel import SQLModel, Field, Relationship, Column, Enum

if TYPE_CHECKING:
    from accounts.models import Accounts



class TransactionCreate(SQLModel):
    pass


class Transactions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Keys
    sender_id: int  = Field(foreign_key="accounts.id")
    receiver_id: int = Field(foreign_key="accounts.id")
    
    amount: Decimal = Field(ge=Decimal('0.01'))
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    
    
class Operations(SQLModel, table=True):
    class OperationType(int, enum.Enum):
        DEPOSIT = 1
        WITHDRAWL = 2
    
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: Decimal = Field(ge=Decimal('0.01'))
    op_type: OperationType = Column(Enum(OperationType))
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    account_id: int = Field(foreign_key="accounts.id")
    account: "Accounts" = Relationship(back_populates="operations_released")