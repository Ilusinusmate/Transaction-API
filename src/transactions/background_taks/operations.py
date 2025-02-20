from sqlmodel import Session

from decimal import Decimal

from transactions.models import Operations
from accounts.repositories.accounts import AccountsRepository, Accounts

class OperationsBackgroundTask:
    

    @staticmethod
    def start_deposit(
        amount: Decimal,
        account_id: int,
        session: Session,
    ):
        
        deposit = Operations(
            account_id=account_id,
            amount=amount,
            operation_type=Operations.OperationType.DEPOSIT
        )

        account: Accounts = AccountsRepository.get_account_by_id(account_id, session)
        AccountsRepository.update_balance(account, account.balance + amount, session)

        session.add(deposit)
        session.commit()
        session.close()

    @staticmethod
    def start_withdraw(
        amount: Decimal,
        account_id: int,
        session: Session,
    ):
        withdraw = Operations(
            account_id=account_id,
            amount=amount,
            operation_type=Operations.OperationType.WITHDRAWL
        )

        account: Accounts = AccountsRepository.get_account_by_id(account_id, session)
        AccountsRepository.update_balance(account, account.balance - amount, session)
        
        session.add(withdraw)
        session.commit()
        session.close()