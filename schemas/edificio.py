from typing import Optional
from pydantic import BaseModel

class Edificio(BaseModel):
    idAdministrador: int
    coordenadas: str
    ctaReferencia: str
    nombreEdificio: str
    referencia: str
    adjunto: Optional[str]
    data_creatd: Optional[str]
    data_update: Optional[str]