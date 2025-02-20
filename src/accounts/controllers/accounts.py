from fastapi import APIRouter, Security, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlmodel import select


from accounts.repositories.accounts import AccountsRepository
from accounts.models import AccountsCreate, Accounts, AccountsPublic
from server.oauth import get_current_user, Users
from server.db import get_session, Session

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/create", response_model=AccountsPublic, status_code=201)
def create_account(
    *,
    session: Session = Depends(get_session),
    current_user: Users = Security(get_current_user),
    body_account: AccountsCreate
):
    account = Accounts(
        user=current_user,
        bank_name=body_account.bank_name
    )
    
    session.add(account)
    session.commit()
    session.refresh(account)
    
    return account



@router.get("/list", response_model=list[AccountsPublic])
def list_accounts(
    *,
    session: Session = Depends(get_session),
    current_user: Users = Security(get_current_user)
):
    return AccountsRepository.get_user_accounts(current_user, session)



@router.get("/list/{account_id}", response_model=AccountsPublic)
def list_accounts(
    *,
    account_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Security(get_current_user)
):
    account = AccountsRepository.get_user_account_by_id(account_id, current_user, session)
    
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    return account



@router.delete("/deactivate/{account_id}", status_code=204)
def deactivate_account(
    *,
    account_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Security(get_current_user)
):
    account: Accounts = AccountsRepository.get_user_account_by_id(account_id, current_user, session)
    
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account.active = False
    session.add(account)
    session.commit()
    
    return  Response(status_code=204)



@router.patch("/reactivate/{account_id}", response_model=Accounts, status_code=200)
def reactivate_account(
    *,
    account_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Security(get_current_user)
):
    account: Accounts = AccountsRepository.get_user_account_by_id(account_id, current_user, session)
    
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    if account.active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already active.")
    
    account.active = True
    session.add(account)
    session.commit()
    
    return account