from sqlmodel import Session

from decimal import Decimal

from accounts.repositories.accounts import AccountsRepository, Accounts
from transactions.repositories.transactions import TransactionRepository

class TransactionsBackgroundTasks:
    
    
    @staticmethod
    def start_transaction(
        receiver_id: int,
        sender_id: int,
        amount: Decimal,
        session: Session,
    ) -> bool: 
        TransactionRepository.create_transaction(
            receiver_id=receiver_id,
            sender_id=sender_id,
            amount=amount,
            session=session,
        )

        sender: Accounts = AccountsRepository.get_account_by_id(
            account_id=sender_id,
            session=session
        )

        receiver: Accounts = AccountsRepository.get_account_by_id(
            account_id=receiver_id,
            session=session
        )


        sender.balance -= amount
        receiver.balance += amount
        session.add(sender)
        session.add(receiver)
        
        session.commit()
        session.close()

        return True

