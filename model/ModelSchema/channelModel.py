from pydantic import BaseModel
from typing import List, Optional


class ChanellModel(BaseModel):
    id_channel: Optional[int]
    channel: str

class ArrayChanellModel(BaseModel):
    data: List[ChanellModel]


class MandoModel(BaseModel):
    id_mando: Optional[int]
    mando: str

class ArrayMandoModel(BaseModel):
    data: List[MandoModel]

class CiudadModel(BaseModel):
    id_ciudad: Optional[int]
    ciudad: str
    region: str

class ArrayCiudadModel(BaseModel):
    data: List[CiudadModel]

class OperadorModel(BaseModel):
    id_operador: Optional[int]
    operador: str

class ArrayOperadorModel(BaseModel):
    data: List[OperadorModel]

class SistemaOperativoModel(BaseModel):
    id_sistema_operativo: Optional[int]
    sistema_operativo: str

class ArraySistemaOperativoModel(BaseModel):
    data: List[SistemaOperativoModel]

class EstadosModel(BaseModel):
    id_estado: Optional[int]
    estado: str

class ArrayEstadosModel(BaseModel):
    data: List[EstadosModel]

class GeneroModel(BaseModel):
    id_genero: Optional[int]
    genero: str

class ArrayGeneroModel(BaseModel):
    data: List[GeneroModel]  


class ModalidadModel(BaseModel):
    id_modalidad: Optional[int]
    modalidad: str

class ArrayModalidadModel(BaseModel):
    data: List[ModalidadModel]