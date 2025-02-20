from typing import Annotated

from fastapi import Request, Depends
from fastapi.security import OAuth2, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel import select

from server.security import validate_access_token
from server.db import engine, Session, get_session
from authuser.models import Users

oauth2_shceme = HTTPBearer()

async def process_header_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_shceme)]):
    """ Valida o token JWT e retorna os dados do usuário autenticado. """
    # auth_header = request.headers.get("Authorization")
    # if not auth_header or not auth_header.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Invalid token")
    user_data = validate_access_token(token.credentials)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = int(user_data)

    return user_id



async def get_current_user(
    user_id: Annotated[str, Depends(process_header_token)],
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(Users, user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
    

async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# NÃO IMPLEMENTADO
async def check_role(required_role: str):
    async def role_checker(user_data=Depends(process_header_token)):
        if user_data.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Access denied.")
        return user_data
    return role_checker