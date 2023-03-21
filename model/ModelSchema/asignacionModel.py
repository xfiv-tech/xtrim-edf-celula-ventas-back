from pydantic import BaseModel
from typing import List, Optional

#Gerente regional
class AsigancionCiudadGreginal(BaseModel):
    id_asignacion_ciudad_greginal: Optional[int] = None
    id_ciudad: int
    id_gerente_regional: int

class ArrayAsigancionCiudadGreginal(BaseModel):
    data: List[AsigancionCiudadGreginal]


class AsigancionCanalGregional(BaseModel):
    id_asignacion_canal: Optional[int] = None
    id_channel: int
    id_gerente_regional: int

class ArrayAsigancionCanalGregional(BaseModel):
    data: List[AsigancionCanalGregional]

#Gerente ciudad
class AsigancionCiudadGciudad(BaseModel):
    id_asignacion_ciudades_gerente_ciudad: Optional[int] = None
    id_ciudad: int
    id_gerente_ciudad: int

class ArrayAsigancionCiudadGciudad(BaseModel):
    data: List[AsigancionCiudadGciudad]

class AsigancionCanalGciudad(BaseModel):
    id_asignacion_canal_gerente_ciudad: Optional[int] = None
    id_channel: int
    id_gerente_ciudad: int

class ArrayAsigancionCanalGciudad(BaseModel):
    data: List[AsigancionCanalGciudad]

#Jefe de venta
class AsigancionCiudadJefe(BaseModel):
    id_asignacion_ciudades_jefe_ventas: Optional[int] = None
    id_ciudad: int
    id_jefe_venta: int

class ArrayAsigancionCiudadJefe(BaseModel):
    data: List[AsigancionCiudadJefe]

class AsigancionCanalJefe(BaseModel):
    id_asignacion_canal_jefe_ventas: Optional[int] = None
    id_channel: int
    id_jefe_venta: int

class ArrayAsigancionCanalJefe(BaseModel):
    data: List[AsigancionCanalJefe]

#Administrador de proyectos
class AsigancionCiudadAdmin(BaseModel):
    id_asignacion_ciudades_admin_proyectos: Optional[int] = None
    id_ciudad: int
    id_admin_proyectos: int

class ArrayAsigancionCiudadAdmin(BaseModel):
    data: List[AsigancionCiudadAdmin]

class AsigancionCanalAdmin(BaseModel):
    id_asignacion_canal_admin_proyectos: Optional[int] = None
    id_channel: int
    id_admin_proyectos: int

class ArrayAsigancionCanalAdmin(BaseModel):
    data: List[AsigancionCanalAdmin]

#Distriuidor
class AsigancionCiudadDistribuidor(BaseModel):
    id_asignacion_ciudades_distribuidor: Optional[int] = None
    id_ciudad: int
    id_registrar_distribuidor: int

class ArrayAsigancionCiudadDistribuidor(BaseModel):
    data: List[AsigancionCiudadDistribuidor]

class AsigancionCanalDistribuidor(BaseModel):
    id_asignacion_canal_distribuidor: Optional[int] = None
    id_channel: int
    id_registrar_distribuidor: int

class ArrayAsigancionCanalDistribuidor(BaseModel):
    data: List[AsigancionCanalDistribuidor]