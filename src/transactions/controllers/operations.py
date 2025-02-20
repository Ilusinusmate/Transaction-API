from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import Response
from fastapi.exceptions import HTTPException

from server.db import get_session, Session
from server.oauth import get_current_user, Users

from accounts.repositories.accounts import AccountsRepository, Accounts
from transactions.models import Operations
from transactions.background_taks.operations import OperationsBackgroundTask
from transactions.repositories.operations import OperationsRepository
from transactions.repositories.transactions import TransactionRepository
from transactions.schemas.operations import DepositMoneyIn, WithdrawMoneyIn
from transactions.services.operations import ValidationOperationService

router = APIRouter(prefix="/operation", tags=["Operations"])

@router.post("/deposit")
async def deposit_money_into_account(
    *,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
    body: DepositMoneyIn,
    background_tasks: BackgroundTasks
):
    
    if not ValidationOperationService.validate_user_account_posses(
        body.account_id,
        current_user,
        session,
    ):
        raise HTTPException(status_code=403, detail="Action not allowed.")
    
    if not ValidationOperationService.validate_deposit(
        body.amount,
        session,
    ):
        raise HTTPException(status_code=400, detail="Invalid amount.")
    
    background_tasks.add_task(
        OperationsBackgroundTask.start_deposit,
        body.amount,
        body.account_id,
        session,
    )

    return Response(status_code=202)



@router.post("/withdraw")
async def withdraw_money_from_account(
    *,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
    body: DepositMoneyIn,
    background_tasks: BackgroundTasks
):
    
    if not ValidationOperationService.validate_user_account_posses(
        body.account_id,
        current_user,
        session,
    ):
        raise HTTPException(status_code=403, detail="Action not allowed.")
    
    if not ValidationOperationService.validate_withdraw(
        body.amount,
        body.account_id,
        session,
    ):
        raise HTTPException(status_code=400, detail="Invalid amount.")
    
    background_tasks.add_task(
        OperationsBackgroundTask.start_withdraw,
        body.amount,
        body.account_id,
        session,
    )

    return Response(status_code=202)
    



@router.get("/list/{account_id}", response_model=list[Operations])
async def get_operation(
    account_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user)
):
    account: Accounts = AccountsRepository.get_user_account_by_id(
        account_id,
        current_user,
        session
    )

    return OperationsRepository.get_account_operations(
        account,
        session,
    )

    
@router.get("/list/{account_id}/{operation_id}", response_model=Operations)
async def get_operation(
    account_id: int,
    operation_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user)
):
    
    account: Accounts = AccountsRepository.get_user_account_by_id(
        account_id,
        current_user,
        session
    )

    return OperationsRepository.get_account_operation_by_id(
        operation_id,
        account,
        session
    )
