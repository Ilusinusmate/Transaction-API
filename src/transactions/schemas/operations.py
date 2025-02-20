from pydantic import BaseModel

from decimal import Decimal

class DepositMoneyIn(BaseModel):
    account_id: int
    amount: Decimal

class WithdrawMoneyIn(BaseModel):
    account_id: int
    amount: Decimal

