from typing import Optional
from pydantic import BaseModel

class LoginToken(BaseModel):
    code: str
    messege: str
    token: str

class DistributorLogin(BaseModel):
    dni: str
    password: str

class User(BaseModel):
    displayName: str
    userId: str

class DistributorLoginResponse(BaseModel):
    code: str
    messege: str
    user: User
