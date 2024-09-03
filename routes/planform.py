from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
import uuid

import os
from controller.AdminProyectController import (
    SelectAdminProyectCiudad,
    SelectGerenteCiudad,
    SelectGerenteRegional,
    SelectJefeVenta,
    SelectLiderPeloton,
)
from controller.AsignacionController import (
    ListarCanalesGRciudad,
    ListarCanalesJVCiudad,
    ListarCiudadesJVCiudad,
)
from function.excelReporte import ReporteExcel
from middleware.validacionToken import ValidacionToken

from model.channel import (
    Channel,
    Ciudad,
    Estados,
    Genero,
    Modalidad,
    Operador,
    RegistrarGerenteCiudad,
    RegistrarGerenteRegional,
    RegistrarVendedor,
    RegistroJefeVentas,
    SistemaOperativo,
)
from database.db import db

planform = APIRouter(route_class=ValidacionToken)


class Planform(BaseModel):
    channel: str
    identificationNumber: str
    cargo: str = Field(
        description="Channel",
        regex="^(vendedor|gerente_regional|gerente_ciudad|jefe_venta|distribuidor)$",
    )
    externalTransactionId: str


class ReporteExcel(BaseModel):
    id_registrar_vendedor: int
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
    # id_gerente: int = None
    # nombre_gerente: str
    id_gerente_regional: int = None
    nombre_gerente_regional: str
    id_gerente_ciudad: int = None
    nombre_gerente_ciudad: str
    id_jefe_venta: int = None
    nombre_jefe_venta: str
    nombre_admin_proyectos: Optional[str] = None
    # ciudad_gestion: str
    lider_check: bool = False
    id_lider_peloton: Optional[str] = None
    meta_volumen_internet: Optional[int] = 0
    meta_dolares_internet: Optional[float] = 0.0
    meta_volumen_telefonia: Optional[int] = 0
    meta_dolares_telefonia: Optional[float] = 0.0
    meta_volumen_television: Optional[int] = 0
    meta_dolares_television: Optional[float] = 0.0
    fecha_salida: str = None
    sector_residencia: str
    email: str
    dias_inactivo: int
    channel: str
    ciudad: str
    region: str
    estado: str
    operador: str
    genero: str
    modalidad: str
    sistema_operativo: str


@planform.post("/planform_integrate")
async def planform_integrate(data: Planform):
    try:
        if data.cargo == "vendedor":
            response = await ConsultarVendedor(data.identificationNumber, data)
            return response
        elif data.cargo == "jefe_venta":
            response = await ConsultarJefesVenta(data)
            return response
        elif data.cargo == "distribuidor":
            response = await ConsultarDistribuidor(data)
            return response
        elif data.cargo == "gerente_ciudad":
            response = await ConsultarGerenteCiudad(data)
            return response
        elif data.cargo == "gerente_regional":
            response = await ConsultarGerenteRegional(data)
            return response
        else:
            return {"code": 400, "status": "error", "message": "El cargo no existe"}
    except Exception as e:
        print(e)
        return {"status": "error"}


# 1307087062
async def ConsultarVendedor(identificationNumber, data):
    try:
        query = (
            RegistrarVendedor.join(
                Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad
            )
            .join(Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado)
            .join(Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel)
            .join(Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador)
            .join(
                SistemaOperativo,
                RegistrarVendedor.c.id_sistema_operativo
                == SistemaOperativo.c.id_sistema_operativo,
            )
            .join(Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero)
            .join(
                RegistroJefeVentas,
                RegistrarVendedor.c.id_jefe_venta == RegistroJefeVentas.c.id_jefe_venta,
            )
            .join(
                RegistrarGerenteRegional,
                RegistrarVendedor.c.id_gerente_regional
                == RegistrarGerenteRegional.c.id_gerente_regional,
            )
            .join(
                RegistrarGerenteCiudad,
                RegistrarVendedor.c.id_gerente_ciudad
                == RegistrarGerenteCiudad.c.id_gerente_ciudad,
            )
            .join(
                Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad
            )
            .select()
            .with_only_columns(
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Operador.c.operador,
                Genero.c.genero,
                Modalidad.c.modalidad,
                # crear un alias para RegistroJefeVentas.c.cedula y no se repita el nombre
                RegistroJefeVentas.c.cedula.label("cedula_jefe_venta"),
                RegistrarGerenteRegional.c.cedula.label("cedula_gerente_regional"),
                RegistrarGerenteCiudad.c.cedula.label("cedula_gerente_ciudad"),
                RegistrarVendedor.c.id_sistema_operativo,
                SistemaOperativo.c.sistema_operativo,
                RegistrarVendedor.c.id_modalidad,
                RegistrarVendedor.c.id_lider_peloton,
                RegistrarVendedor.c.id_estado,
                RegistrarVendedor.c.id_genero,
                RegistrarVendedor.c.id_ciudad,
                RegistrarVendedor.c.id_registrar_vendedor,
                RegistrarVendedor.c.id_channel,
                RegistrarVendedor.c.id_gerente_regional,
                RegistrarVendedor.c.id_gerente_ciudad,
                RegistrarVendedor.c.id_jefe_venta,
                RegistrarVendedor.c.cedula,
                RegistrarVendedor.c.telefono,
                RegistrarVendedor.c.id_operador,
                RegistrarVendedor.c.codigo_vendedor,
                RegistrarVendedor.c.usuario_equifax,
                RegistrarVendedor.c.nombre_vendedor,
                RegistrarVendedor.c.fecha_ingreso,
                RegistrarVendedor.c.fecha_salida,
                RegistrarVendedor.c.sector_residencia,
                RegistrarVendedor.c.lider_check,
                RegistrarVendedor.c.meta_volumen_internet,
                RegistrarVendedor.c.meta_dolares_internet,
                RegistrarVendedor.c.meta_volumen_telefonia,
                RegistrarVendedor.c.meta_dolares_telefonia,
                RegistrarVendedor.c.meta_volumen_television,
                RegistrarVendedor.c.meta_dolares_television,
                RegistrarVendedor.c.email,
                RegistrarVendedor.c.dias_inactivo,
            )
            .where(RegistrarVendedor.c.cedula == identificationNumber)
        )
        res = db.execute(query).fetchone()
        if res is None:
            return {
                "code": 400,
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "Numero de cedula no existe",
            }
        else:
            return {
                "code": 200,
                "data": {
                    "codVendor": res.codigo_vendedor,
                    "identificationNumber": res.cedula,
                    "city": res.ciudad,
                    "status": res.estado,
                    "email": res.email,
                    "cellphone": res.telefono,
                    "goals": {
                        "Internet_volumen": res.meta_volumen_internet,
                        "Internet_dolar": res.meta_dolares_internet,
                        "Television_volumen": res.meta_volumen_television,
                        "Television_dolar": res.meta_dolares_television,
                        "Telefonia_volumen": res.meta_volumen_telefonia,
                        "Telefonia_dolar": res.meta_dolares_telefonia,
                    },
                    "salesChannel": res.channel,
                    "leader": 1 if res.lider_check == True else 0,
                    "in_boss": res.cedula_jefe_venta,  # cédula del jefe id_jefe_venta
                    "distributor": None,  # cédula / ruc del distribuidor / pasaporte
                    "in_manager_regional": res.cedula_gerente_regional,  # cédula del gerente regional id_gerente_regional
                    "id_manager_city": res.cedula_gerente_ciudad,  # cédula del gerente de ciudad id_gerente_ciudad
                },
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "OK",
            }
    except Exception as e:
        print(e)
        return {
            "code": 500,
            "externalTransactionId": data.externalTransactionId,
            "internalTransactionId": uuid.uuid4().hex,
            "message": "Error interno",
        }


async def ConsultarJefesVenta(data):
    try:
        query = (
            RegistroJefeVentas.join(
                Estados, Estados.c.id_estado == RegistroJefeVentas.c.id_estado
            )
            .select()
            .with_only_columns(
                Estados.c.estado,
                RegistroJefeVentas.c.id_jefe_venta,
                RegistroJefeVentas.c.id_estado,
                RegistroJefeVentas.c.id_gerente_ciudad,
                RegistroJefeVentas.c.nombre_jefe,
                RegistroJefeVentas.c.ciudad,
                RegistroJefeVentas.c.email,
                RegistroJefeVentas.c.telefono,
                RegistroJefeVentas.c.cedula,
            )
            .where(RegistroJefeVentas.c.cedula == data.identificationNumber)
        )
        res = db.execute(query).fetchone()
        if res is None:
            return {
                "code": 400,
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "Numero de cedula no existe",
            }
        else:
            channel = await ListarCanalesJVCiudad(res.id_jefe_venta)
            return {
                "code": 200,
                "data": {
                    "identificationNumber": data.identificationNumber,
                    "nameBoss": res.nombre_jefe,
                    "city": res.ciudad,
                    "status": res.estado,
                    "email": res.email,
                    "cellphone": res.telefono,
                    "salesChannel": [i["channel"] for i in channel][0],
                    "id_manager_city": res.cedula,
                },
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "OK",
            }
    except Exception as e:
        print(e)
        return {
            "code": 500,
            "externalTransactionId": data.externalTransactionId,
            "internalTransactionId": uuid.uuid4().hex,
            "message": "Error interno",
        }


async def ConsultarDistribuidor(data):
    try:
        return {
            "code": 200,
            "data": {
                "codVendor": None,
                "identificationNumber": None,
                "nameVendor": None,
                "city": None,
                "status": None,
                "email": None,
                "cellphone": None,
                "goals": {
                    "Internet_volumen": None,
                    "Internet_dolar": None,
                    "Television_volumen": None,
                    "Television_dolar": None,
                    "Telefonia_volumen": None,
                    "Telefonia_dolar": None,
                },
                "salesChannel": None,
                "leader": 0,
                "in_boss": None,  # cédula del jefe
            },
            "externalTransactionId": data.externalTransactionId,
            "internalTransactionId": uuid.uuid4().hex,
            "message": "OK",
        }
    except Exception as e:
        print(e)
        return {"status": "error"}


async def ConsultarGerenteRegional(data):
    try:
        query = (
            RegistrarGerenteRegional.join(
                Estados, Estados.c.id_estado == RegistrarGerenteRegional.c.id_estado
            )
            .select()
            .with_only_columns(
                Estados.c.estado,
                RegistrarGerenteRegional.c.id_gerente_regional,
                RegistrarGerenteRegional.c.id_estado,
                RegistrarGerenteRegional.c.nombre_gerente,
                RegistrarGerenteRegional.c.ciudad,
                RegistrarGerenteRegional.c.email,
                RegistrarGerenteRegional.c.telefono,
                RegistrarGerenteRegional.c.cedula,
            )
            .where(RegistrarGerenteRegional.c.cedula == data.identificationNumber)
        )
        res = db.execute(query).fetchone()
        if res is None:
            return {
                "code": 400,
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "Numero de cedula no existe",
            }
        else:
            channel = await ListarCanalesGRciudad(res.id_gerente_regional)
            return {
                "code": 200,
                "data": {
                    "identificationNumber": data.identificationNumber,
                    "nameManager": res.nombre_gerente,
                    "city": res.ciudad,
                    "status": res.estado,
                    "email": res.email,
                    "cellphone": res.telefono,
                    "salesChannel": [i["channel"] for i in channel][0],
                    "position": data.cargo,
                },
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "OK",
            }
    except Exception as e:
        print(e)
        return {
            "code": 500,
            "externalTransactionId": data.externalTransactionId,
            "internalTransactionId": uuid.uuid4().hex,
            "message": "Error interno",
        }


async def ConsultarGerenteCiudad(data):
    try:
        query = (
            RegistrarGerenteCiudad.join(
                Estados, Estados.c.id_estado == RegistrarGerenteCiudad.c.id_estado
            )
            .select()
            .with_only_columns(
                RegistrarGerenteCiudad.c.id_gerente_ciudad,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                RegistrarGerenteCiudad.c.ciudad,
                RegistrarGerenteCiudad.c.email,
                RegistrarGerenteCiudad.c.telefono,
                RegistrarGerenteCiudad.c.cedula,
            )
        )
        res = db.execute(query).fetchone()
        if res is None:
            return {
                "code": 400,
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "Numero de cedula no existe",
            }
        else:
            return {
                "code": 200,
                "data": {
                    "identificationNumber": data.identificationNumber,
                    "nameManager": res.nombre_gerente_ciudad,
                    "city": res.ciudad,
                    "status": res.estado,
                    "email": res.email,
                    "cellphone": res.telefono,
                    "salesChannel": None,
                    "position": data.cargo,
                },
                "externalTransactionId": data.externalTransactionId,
                "internalTransactionId": uuid.uuid4().hex,
                "message": "OK",
            }
    except Exception as e:
        print(e)
        return {
            "code": 500,
            "externalTransactionId": data.externalTransactionId,
            "internalTransactionId": uuid.uuid4().hex,
            "message": "Error interno",
        }
