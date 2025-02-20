from sqlmodel import Session, select, or_

from decimal import Decimal

from server.oauth import Users
from transactions.models import Transactions

class TransactionRepository:
    
    @staticmethod
    def get_user_sent_transactions(user: Users, session: Session) -> list[Transactions]:
        return session.exec(
            select(Transactions).where(Transactions.sender_id == user.id)
        ).all()
    
    @staticmethod
    def get_user_recieved_transactions(user: Users, session: Session) -> list[Transactions]:
        return session.exec(
            select(Transactions).where(Transactions.receiver_id == user.id)
        ).all()
    
    
    @staticmethod
    def get_user_transactions(user: Users, session: Session) -> list[Transactions]:
        return session.exec(
            select(Transactions).where(
                or_(
                    Transactions.receiver_id == user.id,
                    Transactions.sender_id == user.id
                )
            )
        ).all()
        
    
    @staticmethod
    def get_transaction_by_id(transaction_id: int, session: Session) -> Transactions | None:
        return session.get(Transactions, transaction_id)
    
    
    @staticmethod
    def create_transaction(
        sender_id: int,
        reciever_id: int,
        amount: Decimal,        
        session: Session,
    ) -> None:
        
        transaction = Transactions(
            sender_id=sender_id,
            receiver_id=reciever_id,
            amount=amount
        )
        
        session.add(transaction)
        session.commit()