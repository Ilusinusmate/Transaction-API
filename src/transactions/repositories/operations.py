from sqlmodel import Session, select

from transactions.models import Operations
from accounts.models import Accounts

class OperationsRepository:


    @staticmethod
    def get_account_operation_by_id(operation_id: int, account: Accounts, session: Session) -> Operations | None:
        return session.exec(
            select(Operations)
            .where(Operations.id == operation_id)
            .where(Operations.account_id == account.id),
        ).first()
    

    
    @staticmethod
    def get_account_operations(account: Accounts, session: Session) -> list[Operations]:
        return session.exec(
            select(Operations).where(Operations.account_id == account.id),
        ).all()



    @staticmethod
    def get_operations_by_id(operation_id:int, session: Session) -> Operations | None:
        return session.get(Operations, operation_id)
    


    @staticmethod
    def get_operations(session: Session) -> list[Operations]:
        return session.exec(select(Operations)).all()