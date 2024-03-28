from typing import Optional
from pydantic import BaseModel
from enum import Enum

class DistributorEnum(str, Enum):
    Mardis = "Mardis"
    XtrimPro = "XtrimPro"

class LoginToken(BaseModel):
    code: str
    messege: str
    token: str

class DistributorLogin(BaseModel):
    dni: str
    password: str
    distributor: DistributorEnum


class DistributorLoginDecrypt(BaseModel):
    dni: str
    password: str
    distributor: str

class User(BaseModel):
    displayName: str
    userId: str

class DistributorLoginResponse(BaseModel):
    code: str
    messege: str
    user: User
