from pydantic import BaseModel
from typing import List, Optional



class RoleBase(BaseModel):
    id: Optional[int] = 0
    rol: str
    descripcion: Optional[str] = None
