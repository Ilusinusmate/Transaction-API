from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlmodel import Session

from server.db import get_session
from server.oauth import get_current_user, Users
from transactions.models import Transactions
from transactions.repositories.transactions import TransactionRepository
from transactions.services.transactions import ValidationService
from transactions.schemas.transactions import TransferMoneyBetweenAccountsIn
from transactions.background_taks.transactions import TransactionsBackgroundTasks

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/{sender_id}/{receiver_id}", status_code=202)
def transfer_money_between_accounts(
    *,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
    body: TransferMoneyBetweenAccountsIn,
    sender_id: int,
    receiver_id: int,
    background_tasks: BackgroundTasks
):
    
    if not ValidationService.validate_user_account_posses(
        sender_id,
        current_user,
        session,
    ):
        raise HTTPException(status_code=403, detail="Action not allowed")
    
    if not ValidationService.validate_transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=body.amount,
        session=session
    ):
        raise HTTPException(status_code=400, detail="Invalid transaction")

    background_tasks.add_task(
        TransactionsBackgroundTasks.start_transaction,
        sender_id,
        receiver_id,
        body.amount,
        session,
    )

    return Response(status_code=202)

@router.get("/list", response_model=list[Transactions])
async def list_transactions(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return TransactionRepository.get_user_transactions(current_user, session)