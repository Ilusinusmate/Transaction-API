from sqlmodel import select, Session

from decimal import Decimal

from server.oauth import Users
from accounts.models import Accounts



class ValidationOperationService:

    @staticmethod
    def validate_user_account_posses(account_id: int, user: Users, session: Session) -> bool:
        return session.exec(
            select(Accounts)
            .where(Accounts.id == account_id)
            .where(Accounts.user_id == user.id)
        ).first() is not None
    
    @staticmethod
    def validate_deposit(amount: Decimal, session: Session) -> bool:
        return amount > Decimal("0.00")
    
    @staticmethod
    def validate_withdraw(amount: Decimal, account_id: int, session: Session) -> bool:
        account = session.get(Accounts, account_id)
        if account is None:
            return False
        
        return account.balance >= amount