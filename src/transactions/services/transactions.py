from sqlmodel import Session

from decimal import Decimal

from server.oauth import Users
from accounts.repositories.accounts import AccountsRepository, Accounts

class ValidationService:
    
    @staticmethod
    def validate_user_account_posses(
        sender_id: int,
        user: Users,
        session: Session
    ) -> bool:
        
        return AccountsRepository.get_user_account_by_id(
            sender_id,
            user,
            session
        ) is not None
    
    
    
    @staticmethod
    def validate_transaction(
        sender_id: int,
        receiver_id: int,
        amount: Decimal,
        session: Session
    ) -> bool:
        
        # PREVALIDATIONS
        
        if amount <= Decimal("0.01"):
            return False
        
        if receiver_id == sender_id:
            return False    
        
        # QUERIES
        
        sender: Accounts = AccountsRepository.get_account_by_id(sender_id, session)
        receiver: Accounts = AccountsRepository.get_account_by_id(receiver_id, session)
        if (sender is None) or (receiver is None):
            return False        
        
        # VALIDATIONS
        
        if sender.balance < amount:
            return False
        
        if not receiver.active:
            return False
        
        if not sender.active:
            return False
        
        return True
        