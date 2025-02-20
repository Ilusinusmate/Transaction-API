from pydantic import BaseModel, EmailStr

class UserCreationIn(BaseModel):
    """User creation input model"""
    email: EmailStr
    password: str


class UserLoginIn(BaseModel):
    """User login credentials"""
    email: EmailStr
    password: str
    
    
class AccessTokenModel(BaseModel):
    access_token: str
    # refresh_token: str
    # NÃO IMPLEMENTADO