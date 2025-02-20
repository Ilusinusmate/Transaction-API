from sqlmodel import Session, select

from accounts.models import Accounts
from authuser.models import Users


class AccountsRepository:
    
    @staticmethod
    def get_account_by_id(account_id: int, session: Session) -> Accounts | None:
        return session.get(Accounts, account_id)
    
    @staticmethod
    def get_user_accounts(user: Users, session: Session) -> list[Accounts]:
        return session.exec(
            select(Accounts).where(Accounts.user_id == user.id)
        ).all()
        
    @staticmethod
    def get_user_account_by_id(account_id: int, user: Users, session: Session) -> Accounts | None:
        return session.exec(
            select(Accounts).where(Accounts.id == account_id).where(Accounts.user_id == user.id)
        ).first()