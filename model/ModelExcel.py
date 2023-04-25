



from typing import Optional
from pydantic import BaseModel


class ModelVendedorExcel(BaseModel):
    # id_registrar_vendedor: Optional[int] = None
    id_channel: Optional[int]
    id_ciudad: Optional[int]
    id_operador: Optional[int]
    id_sistema_operativo: Optional[int]
    id_estado: Optional[int]
    id_genero: Optional[int]
    id_modalidad: Optional[int]
    codigo_vendedor: Optional[str]
    usuario_equifax: Optional[str]
    nombre_vendedor: Optional[str]
    fecha_ingreso: Optional[str]
    id_gerente_regional: Optional[int] = None
    id_gerente_ciudad: Optional[int] = None
    id_jefe_venta: Optional[int] = None
    id_lider_peloton: Optional[int] = 0
    meta_volumen_internet: Optional[int] = 0
    meta_dolares_internet: Optional[float] = 0
    meta_volumen_telefonia: Optional[int]  = 0
    meta_dolares_telefonia: Optional[float] = 0
    meta_volumen_television: Optional[int]  = 0
    meta_dolares_television: Optional[float] = 0
    fecha_salida: Optional[str] = None
    sector_residencia: Optional[str] = None
    email: Optional[str] = "noemail@xtrim.com.ec"
    cedula: Optional[str] = None
    telefono: Optional[str] = 9999999999
    dias_inactivo: Optional[int] = 0


