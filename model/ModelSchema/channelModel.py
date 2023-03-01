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