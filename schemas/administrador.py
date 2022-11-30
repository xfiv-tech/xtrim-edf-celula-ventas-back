from typing import Optional
from pydantic import BaseModel

class Administrador(BaseModel):
    id: Optional[int]
    nombreAdministrador: str
    cedula: str
    email: str
    telefono: str
    telefono_opt: str
    data_creatd: Optional[str]
    data_update: Optional[str]