from sqlmodel import Session

from decimal import Decimal

from transactions.repositories.transactions import TransactionRepository


class TransactionsBackgroundTasks:
    
    
    @staticmethod
    def start_transaction(
        receiver_id: int,
        sender_id: int,
        amount: Decimal,
        session: Session,
    ): 
        TransactionRepository.create_transaction(
            receiver_id=receiver_id,
            sender_id=sender_id,
            amount=amount,
            session=session,
        )