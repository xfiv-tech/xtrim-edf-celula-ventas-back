from typing import Optional
from pydantic import BaseModel

class Usuario(BaseModel):
    id: Optional[str]
    nombreCompleto: str
    email: str
    usuario: str
    password: str
    data_creatd: Optional[str]
    data_update: Optional[str]