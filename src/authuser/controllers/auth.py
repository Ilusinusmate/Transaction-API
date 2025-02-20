from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import select

from server.db import get_session
from authuser.schemas import (
    AccessTokenModel,
    UserLoginIn,
)


from authuser.models import Users
from server.db import engine, Session
from server.security import check_password, generate_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=AccessTokenModel)
def login_user(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    
        
    query = select(Users).where(Users.email == user_credentials.username)
    user = session.exec(query).first()
    
    if user is None:
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)
    
    if not check_password(user_credentials.password, user):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)
    
    return AccessTokenModel(
        access_token=generate_access_token(user),
    )