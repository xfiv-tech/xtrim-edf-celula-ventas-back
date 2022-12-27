from typing import Optional
from pydantic import BaseModel

class Edificio(BaseModel):
    id: Optional[int]
    id_usuario: int
    idAdministrador: int
    id_edificio: Optional[str]
    sector: str
    ciudad: str
    coordenadas: str
    ctaReferencia: str
    cedulaReferencia: str
    nombreEdificio: str
    responsable: str
    referencia: str
    adjunto: Optional[str]
    data_creatd: Optional[str]
    data_update: Optional[str]



class EdificioIDusuario(BaseModel):
    id_usuario: int