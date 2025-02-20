from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session

from server.db import get_session
from authuser.models import Users, UsersPublic
from server.security import hash_password
from authuser.schemas import UserCreationIn
from server.db import engine, Session

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UsersPublic)
async def register_user(
    body_user: UserCreationIn,
    session: Session = Depends(get_session),
):
    user = Users(
        password=hash_password(body_user.password),
        email=body_user.email
    )
    
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
    return user
    
    