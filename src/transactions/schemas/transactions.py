from pydantic import BaseModel

from decimal import Decimal

class TransferMoneyBetweenAccountsIn(BaseModel):
    """Transfer money between accounts in."""
    amount: Decimal
    