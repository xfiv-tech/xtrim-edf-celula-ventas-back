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


class RegistrarVendedorModel(BaseModel):
    id_registrar_vendedor: Optional[int]
    id_channel: int
    id_ciudad: int
    id_operador: int
    id_sistema_operativo: int
    id_estado: int
    id_genero: int
    id_modalidad: int
    cedula: str
    telefono: str
    codigo_vendedor: str
    usuario_equifax: str
    nombre_vendedor: str
    fecha_ingreso: str
    # id_gerente: Optional[int] = None
    id_gerente_regional: Optional[int] = None
    id_gerente_ciudad: Optional[int] = None
    id_jefe_venta: Optional[int] = None
    id_lider_peloton: Optional[int] = None
    # ciudad_gestion: str
    lider_check: Optional[bool] = False
    meta_volumen: Optional[int] = 0
    meta_dolares: Optional[float] = 0.0
    fecha_salida: Optional[str] = None
    sector_residencia: str
    email: str
    cedula: str
    dias_inactivo: Optional[int] = 0

class ArrayRegistrarVendedorModel(BaseModel):
    data: List[RegistrarVendedorModel]


class RegistrarDistribuidorModel(BaseModel):
    id_registrar_distribuidor: Optional[int]
    id_ciudad: Optional[int]
    id_estado: int
    nombre_distribuidor: str
    responsable: str
    telefono: str
    email: str
    fecha_ingreso: str
    fecha_salida: Optional[str]

class ArrayRegistrarDistribuidor(BaseModel):
    data: List[RegistrarDistribuidorModel]


class RegistrarJefeModel(BaseModel):
    id_jefe_venta: Optional[int]
    id_channel: Optional[int]
    id_ciudad: Optional[int]
    id_estado: Optional[int] = None
    id_gerente: Optional[int] = None
    nombre_jefe: str

class ArrayRegistrarJefeModel(BaseModel):
    data: List[RegistrarJefeModel]


class RegistrarAdministradorModel(BaseModel):
    id_administrador: Optional[int]
    id_estado: int
    email: str
    password: str
    id_roles: str
    nombre_administrador: str
    perfil: str
    

class ArrayRegistrarAdministradorModel(BaseModel):
    data: List[RegistrarAdministradorModel]


class RegistrarGerenteRegionalModel(BaseModel):
    id_gerente_regional: Optional[int]
    id_channel: Optional[int]
    id_ciudad: Optional[int]
    id_estado: int
    nombre_gerente: str
class RegistrarGerenteModel(BaseModel):
    id_gerente: Optional[int]
    id_channel: Optional[int]
    id_ciudad: Optional[int]
    id_estado: int
    nombre_gerente: str

class ArrayRegistrarGerenteModel(BaseModel):
    data: List[RegistrarGerenteModel]

class RegistrarGerenteCiudadModel(BaseModel):
    id_gerente_ciudad: Optional[int]
    id_channel: Optional[int]
    id_ciudad: Optional[int]
    id_estado: int
    nombre_gerente_ciudad: str

class ArrayRegistrarGerenteCiudadModel(BaseModel):
    data: List[RegistrarGerenteCiudadModel]


class RegistrarAdminProyectosModel(BaseModel):
    id_admin_proyectos: Optional[int]
    id_channel: Optional[int]
    id_ciudad: Optional[int]
    id_estado: int
    nombre_admin_proyectos: str