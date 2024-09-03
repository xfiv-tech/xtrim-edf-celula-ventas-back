import calendar
import datetime
import io
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from controller.AdminProyectController import (SelectAdminProyectCiudad,
                                               SelectGerenteCiudad,
                                               SelectGerenteRegional,
                                               SelectJefeVenta,
                                               SelectLiderPeloton,
                                               ZonalGerente, ZonalIdGerente)
from controller.AsignacionController import (ListarCanalesAdminCiudad,
                                             ListarCanalesAPCiudad,
                                             ListarCanalesDistribuidor,
                                             ListarCanalesGCiudad,
                                             ListarCanalesGRciudad,
                                             ListarCanalesJVCiudad,
                                             ListarCiudadesAdminCiudad,
                                             ListarCiudadesAPCiudad,
                                             ListarCiudadesDistribuidor,
                                             ListarCiudadesGCiudad,
                                             ListarCiudadesGRegional,
                                             ListarCiudadesJVCiudad)
from database.db import db
from function.encrytPassword import encryptPassword
from function.excelReporte import get_tdd_excel_workbook
from function.ExtraerCiuCanl import ExtraerCiuCanl
from function.function_jwt import decode_token
from middleware.validacionToken import ValidacionToken
from model.channel import (Channel, Ciudad, Estados, Genero, Modalidad,
                           Operador, RegistrarAdminProyectos,
                           RegistrarDistribuidor, RegistrarGerenteCiudad,
                           RegistrarGerenteRegional, RegistrarGerenteZonal,
                           RegistrarVendedor, RegistroAdministrador,
                           RegistroJefeVentas, SistemaOperativo,
                           asiganacion_canal_gerente_regional,
                           asignacion_canal_admin,
                           asignacion_canal_admin_proyectos,
                           asignacion_canal_distribuidor,
                           asignacion_canal_gerente_ciudad,
                           asignacion_canal_jefe_ventas,
                           asignacion_ciudades_admin,
                           asignacion_ciudades_admin_proyectos,
                           asignacion_ciudades_distribuidor,
                           asignacion_ciudades_gerente_ciudad,
                           asignacion_ciudades_gerente_regional,
                           asignacion_ciudades_jefe_ventas)
from model.ModelExcel import ModelVendedorExcel, ModelVendedorExcelProsupuesto
from model.ModelSchema.channelModel import (RegistrarAdministradorModel,
                                            RegistrarAdministradorModelNew,
                                            RegistrarAdminProyectosModel,
                                            RegistrarDistribuidorModel,
                                            RegistrarGerenteCiudadModel,
                                            RegistrarGerenteRegionalModel,
                                            RegistrarJefeModel,
                                            RegistrarVendedorModel)
# from rabbitMQConexion.emmitRabbitMQ import EmitRabbitMQNewUser, EmitRabbitMQEditUser
from redisConexion.RedisQuerys import (AddRedis, DeleteRedis, GetterRedis,
                                       SetterRedis, UpdateRedis)

# moment.need()

# registro = APIRouter(route_class=ValidacionToken)
registro = APIRouter()

load_dotenv()
HOST = os.getenv("HOST_FTP")
USER = os.getenv("USER_FTP")
PASS = os.getenv("PASS_FTP")

# lista de vendedores


@registro.get("/reporte_ftp", tags=["Vendedor"])
async def get_reporteFtp(request: Request):
    try:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        header = request.headers
        decodeToken = decode_token(header["authorization"].split(" ")[1])
        CanalCiudad = await ExtraerCiuCanl(decodeToken["id"], decodeToken["perfil"])
        ciudad = CanalCiudad["ciudad"]
        # validar que el dia sea el ultimo del mes actual
        # Obtener la fecha actual
        today = datetime.date.today()
        # Obtener el último día del mes actual
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        # Verificar si el día actual es el último día del mes
        if today.day == last_day_of_month:
            print("El día actual es el último día del mes")
            usuario = "Celula_Ventas_" + fecha + ".xlsx"
        else:
            print("El día actual no es el último día del mes")
            usuario = "Celula_Ventas.xlsx"

        resultado = await get_tdd_excel_workbook(ciudad, usuario)
        if resultado["success"]:
            return FileResponse(
                path=usuario,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=usuario,
            )
        else:
            raise HTTPException(status_code=400, detail=resultado["error"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.args))

# lista de vendedores


@registro.get("/listar_registro", tags=["Vendedor"])
async def get_registro(request: Request):
    try:
        header = request.headers
        decodeToken = decode_token(header["authorization"].split(" ")[1])
        print("decodeToken", decodeToken)
        CanalCiudad = await ExtraerCiuCanl(decodeToken["id"], decodeToken["perfil"])
        ciudad = CanalCiudad["ciudad"]
        cod_ = decodeToken.get('exp')
        dataRedis = await GetterRedis(f"{cod_ if cod_ else ''}_vendedor")
        if dataRedis:
            return {
                "code": "0",
                "data": dataRedis
            }
        # print("Ciudades", ciudad)
        data = []
        for i in ciudad:
            query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
                Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
                Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
                Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
                SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
                Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
                Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns(
                    Channel.c.channel,
                    Ciudad.c.ciudad,
                    Ciudad.c.region,
                    Estados.c.estado,
                    Operador.c.operador,
                    Genero.c.genero,
                    Modalidad.c.modalidad,
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
                    RegistrarVendedor.c.campana,
                    RegistrarVendedor.c.isla,
                    RegistrarVendedor.c.id_gerente_zonal,
                    RegistrarVendedor.c.dias_inactivo
                ).where(RegistrarVendedor.c.id_ciudad == i["id_ciudad"])
            res = db.execute(query).fetchall()
            for i in res:
                data.append(i)

        dataInfo = []
        for i in data:
            if i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
                dataInfo.append({
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    "id_lider_peloton": i.id_lider_peloton,
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": None,
                    "nombre_gerente_regional": "Sin Gerente Regional",
                    "id_gerente_ciudad": None,
                    "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen_internet": i.meta_volumen_internet,
                    "meta_dolares_internet": i.meta_dolares_internet,
                    "meta_volumen_telefonia": i.meta_volumen_telefonia,
                    "meta_dolares_telefonia": i.meta_dolares_telefonia,
                    "meta_volumen_television": i.meta_volumen_television,
                    "meta_dolares_television": i.meta_dolares_television,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "id_gerente_zonal": i.id_gerente_zonal,
                    # "gerente_zonal": next((x["nombre"] for x in genteZonal if x["id_gerente_zonal"] == i.id_gerente_zonal), None),
                    "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
                    "sistema_operativo": i.sistema_operativo
                })

            elif i.id_gerente_regional != None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns(
                    RegistrarGerenteRegional.c.nombre_gerente,
                )
                data_gerente_regional = db.execute(
                    query_gerente_regional).fetchone()
                dataInfo.append({
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    "id_lider_peloton": i.id_lider_peloton,
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": i.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": None,
                    "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen_internet": i.meta_volumen_internet,
                    "meta_dolares_internet": i.meta_dolares_internet,
                    "meta_volumen_telefonia": i.meta_volumen_telefonia,
                    "meta_dolares_telefonia": i.meta_dolares_telefonia,
                    "meta_volumen_television": i.meta_volumen_television,
                    "meta_dolares_television": i.meta_dolares_television,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "id_gerente_zonal": i.id_gerente_zonal,
                    # "gerente_zonal": next((x["nombre"] for x in genteZonal if x["id_gerente_zonal"] == i.id_gerente_zonal), None),
                    "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
                    "sistema_operativo": i.sistema_operativo
                })

            elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta == None:
                # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns(
                #     RegistrarGerente.c.nombre_gerente,
                # )
                # data_gerente = db.execute(query_gerente).fetchone()
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns(
                    RegistrarGerenteRegional.c.nombre_gerente,
                )
                data_gerente_regional = db.execute(
                    query_gerente_regional).fetchone()
                query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns(
                    RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                )
                data_gerente_ciudad = db.execute(
                    query_gerente_ciudad).fetchone()
                dataInfo.append({
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    "id_lider_peloton": i.id_lider_peloton,
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": i.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen_internet": i.meta_volumen_internet,
                    "meta_dolares_internet": i.meta_dolares_internet,
                    "meta_volumen_telefonia": i.meta_volumen_telefonia,
                    "meta_dolares_telefonia": i.meta_dolares_telefonia,
                    "meta_volumen_television": i.meta_volumen_television,
                    "meta_dolares_television": i.meta_dolares_television,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "id_gerente_zonal": i.id_gerente_zonal,
                    # "gerente_zonal": next((x["nombre"] for x in genteZonal if x["id_gerente_zonal"] == i.id_gerente_zonal), None),
                    "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
                    "sistema_operativo": i.sistema_operativo
                })

            elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta != None:
                print("entro aca", i.id_gerente_regional,
                      i.id_gerente_ciudad, i.id_jefe_venta)

                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns(
                    RegistrarGerenteRegional.c.nombre_gerente,
                )
                data_gerente_regional = db.execute(
                    query_gerente_regional).fetchone()

                print("data_gerente_regional",
                      data_gerente_regional.nombre_gerente)
                query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns(
                    RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                )

                data_gerente_ciudad = db.execute(
                    query_gerente_ciudad).fetchone()

                query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns(
                    RegistroJefeVentas.c.nombre_jefe,
                )
                data_jefe_venta = db.execute(query_jefe_venta).fetchone()

                dataInfo.append({
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    "id_lider_peloton": i.id_lider_peloton,
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": i.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
                    "id_jefe_venta": i.id_jefe_venta,
                    "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen_internet": i.meta_volumen_internet,
                    "meta_dolares_internet": i.meta_dolares_internet,
                    "meta_volumen_telefonia": i.meta_volumen_telefonia,
                    "meta_dolares_telefonia": i.meta_dolares_telefonia,
                    "meta_volumen_television": i.meta_volumen_television,
                    "meta_dolares_television": i.meta_dolares_television,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "id_gerente_zonal": i.id_gerente_zonal,
                    # "gerente_zonal": next((x["nombre"] for x in genteZonal if x["id_gerente_zonal"] == i.id_gerente_zonal), None),
                    "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
                    "sistema_operativo": i.sistema_operativo
                })
            elif i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta != None:

                query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns(
                    RegistroJefeVentas.c.nombre_jefe,
                )
                data_jefe_venta = db.execute(query_jefe_venta).fetchone()
                dataInfo.append({
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    "id_lider_peloton": i.id_lider_peloton,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    # "id_gerente_regional": None,
                    # "nombre_gerente_regional": "Sin Gerente Regional",
                    # "id_gerente_ciudad": None,
                    # "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": i.id_jefe_venta,
                    "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen_internet": i.meta_volumen_internet,
                    "meta_dolares_internet": i.meta_dolares_internet,
                    "meta_volumen_telefonia": i.meta_volumen_telefonia,
                    "meta_dolares_telefonia": i.meta_dolares_telefonia,
                    "meta_volumen_television": i.meta_volumen_television,
                    "meta_dolares_television": i.meta_dolares_television,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "id_gerente_zonal": i.id_gerente_zonal,
                    # "gerente_zonal": next((x["nombre"] for x in genteZonal if x["id_gerente_zonal"] == i.id_gerente_zonal), None),
                    "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
                    "sistema_operativo": i.sistema_operativo
                })

            else:
                dataInfo.append({
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    "id_lider_peloton": i.id_lider_peloton,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    "id_gerente_regional": None,
                    "nombre_gerente_regional": "Sin Gerente Regional",
                    "id_gerente_ciudad": None,
                    "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen_internet": i.meta_volumen_internet,
                    "meta_dolares_internet": i.meta_dolares_internet,
                    "meta_volumen_telefonia": i.meta_volumen_telefonia,
                    "meta_dolares_telefonia": i.meta_dolares_telefonia,
                    "meta_volumen_television": i.meta_volumen_television,
                    "meta_dolares_television": i.meta_dolares_television,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "id_gerente_zonal": i.id_gerente_zonal,
                    # "gerente_zonal": next((x["nombre"] for x in genteZonal if x["id_gerente_zonal"] == i.id_gerente_zonal), None),
                    "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
                    "sistema_operativo": i.sistema_operativo
                })

        await SetterRedis(f"{cod_ if cod_ else ''}_vendedor", dataInfo)
        return {
            "code": "0",
            "data": dataInfo
        }
    except Exception as e:
        print("error", e)
        return {"error": str(e)}


# @registro.get("/listar_registro_all", tags=["Vendedor"])
# async def get_registro(request: Request):
#     try:
#         header = request.headers
#         decodeToken = decode_token(header["authorization"].split(" ")[1])
#         print("decodeToken", decodeToken)
#         CanalCiudad = await ExtraerCiuCanl(decodeToken["id"], decodeToken["perfil"])
#         ciudad = CanalCiudad["ciudad"]
#         print("Ciudades", ciudad)
#         dataRedis = await GetterRedis("vendedor")
#         if dataRedis:
#             return {
#                 "code": "0",
#                 "data": dataRedis
#             }

#         data = []
#         for i in ciudad:
#             query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
#                 Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
#                 Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
#                 Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
#                 SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
#                 Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
#                 Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns(
#                     Channel.c.channel,
#                     Ciudad.c.ciudad,
#                     Ciudad.c.region,
#                     Estados.c.estado,
#                     Operador.c.operador,
#                     Genero.c.genero,
#                     Modalidad.c.modalidad,
#                     RegistrarVendedor.c.id_sistema_operativo,
#                     SistemaOperativo.c.sistema_operativo,
#                     RegistrarVendedor.c.id_modalidad,
#                     RegistrarVendedor.c.id_lider_peloton,
#                     RegistrarVendedor.c.id_estado,
#                     RegistrarVendedor.c.id_genero,
#                     RegistrarVendedor.c.id_ciudad,
#                     RegistrarVendedor.c.id_registrar_vendedor,
#                     RegistrarVendedor.c.id_channel,
#                     RegistrarVendedor.c.id_gerente_regional,
#                     RegistrarVendedor.c.id_gerente_ciudad,
#                     RegistrarVendedor.c.id_jefe_venta,
#                     RegistrarVendedor.c.cedula,
#                     RegistrarVendedor.c.telefono,
#                     RegistrarVendedor.c.id_operador,
#                     RegistrarVendedor.c.codigo_vendedor,
#                     RegistrarVendedor.c.usuario_equifax,
#                     RegistrarVendedor.c.nombre_vendedor,
#                     RegistrarVendedor.c.fecha_ingreso,
#                     RegistrarVendedor.c.fecha_salida,
#                     RegistrarVendedor.c.sector_residencia,
#                     RegistrarVendedor.c.lider_check,
#                     RegistrarVendedor.c.meta_volumen_internet,
#                     RegistrarVendedor.c.meta_dolares_internet,
#                     RegistrarVendedor.c.meta_volumen_telefonia,
#                     RegistrarVendedor.c.meta_dolares_telefonia,
#                     RegistrarVendedor.c.meta_volumen_television,
#                     RegistrarVendedor.c.meta_dolares_television,
#                     RegistrarVendedor.c.email,
#                     RegistrarVendedor.c.campana,
#                     RegistrarVendedor.c.isla,
#                     RegistrarVendedor.c.id_gerente_zonal,
#                     RegistrarVendedor.c.dias_inactivo
#                 ).where(RegistrarVendedor.c.id_ciudad == i["id_ciudad"])
#             res = db.execute(query).fetchall()
#             for i in res:
#                 data.append(i)

#         dataInfo = []
#         for i in data:
#             if i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
#                 dataInfo.append({
#                     "id_registrar_vendedor": i.id_registrar_vendedor,
#                     "id_channel": i.id_channel,
#                     "id_ciudad": i.id_ciudad,
#                     "id_operador": i.id_operador,
#                     "id_sistema_operativo": i.id_sistema_operativo,
#                     "id_estado": i.id_estado,
#                     "id_genero": i.id_genero,
#                     "id_modalidad": i.id_modalidad,
#                     "cedula": i.cedula,
#                     "telefono": i.telefono,
#                     "codigo_vendedor": i.codigo_vendedor,
#                     "usuario_equifax": i.usuario_equifax,
#                     "nombre_vendedor": i.nombre_vendedor,
#                     "fecha_ingreso": i.fecha_ingreso,
#                     "id_lider_peloton": i.id_lider_peloton,
#                     # "id_gerente": data_gerente.id_gerente,
#                     # "nombre_gerente": data_gerente.nombre_gerente,
#                     "id_gerente_regional": None,
#                     "nombre_gerente_regional": "Sin Gerente Regional",
#                     "id_gerente_ciudad": None,
#                     "nombre_gerente_ciudad": "Sin Gerente Ciudad",
#                     "id_jefe_venta": None,
#                     "nombre_jefe_venta": "Sin Jefe de Ventas",
#                     # "ciudad_gestion": i.ciudad_gestion,
#                     "lider_check": i.lider_check,
#                     "meta_volumen_internet": i.meta_volumen_internet,
#                     "meta_dolares_internet": i.meta_dolares_internet,
#                     "meta_volumen_telefonia": i.meta_volumen_telefonia,
#                     "meta_dolares_telefonia": i.meta_dolares_telefonia,
#                     "meta_volumen_television": i.meta_volumen_television,
#                     "meta_dolares_television": i.meta_dolares_television,
#                     "fecha_salida": i.fecha_salida,
#                     "sector_residencia": i.sector_residencia,
#                     "email": i.email,
#                     "dias_inactivo": i.dias_inactivo,
#                     "channel": i.channel,
#                     "ciudad": i.ciudad,
#                     "region": i.region,
#                     "estado": i.estado,
#                     "operador": i.operador,
#                     "genero": i.genero,
#                     "modalidad": i.modalidad,
#                     "campana": i.campana,
#                     "isla": i.isla,
#                     "id_gerente_zonal": i.id_gerente_zonal,
#                     "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
#                     "sistema_operativo": i.sistema_operativo
#                 })

#             elif i.id_gerente_regional != None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
#                 query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns(
#                     RegistrarGerenteRegional.c.nombre_gerente,
#                 )
#                 data_gerente_regional = db.execute(
#                     query_gerente_regional).fetchone()
#                 dataInfo.append({
#                     "id_registrar_vendedor": i.id_registrar_vendedor,
#                     "id_channel": i.id_channel,
#                     "id_ciudad": i.id_ciudad,
#                     "id_operador": i.id_operador,
#                     "id_sistema_operativo": i.id_sistema_operativo,
#                     "id_estado": i.id_estado,
#                     "id_genero": i.id_genero,
#                     "id_modalidad": i.id_modalidad,
#                     "cedula": i.cedula,
#                     "telefono": i.telefono,
#                     "codigo_vendedor": i.codigo_vendedor,
#                     "usuario_equifax": i.usuario_equifax,
#                     "nombre_vendedor": i.nombre_vendedor,
#                     "fecha_ingreso": i.fecha_ingreso,
#                     "id_lider_peloton": i.id_lider_peloton,
#                     # "id_gerente": data_gerente.id_gerente,
#                     # "nombre_gerente": data_gerente.nombre_gerente,
#                     "id_gerente_regional": i.id_gerente_regional,
#                     "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
#                     "id_gerente_ciudad": None,
#                     "nombre_gerente_ciudad": "Sin Gerente Ciudad",
#                     "id_jefe_venta": None,
#                     "nombre_jefe_venta": "Sin Jefe de Ventas",
#                     # "ciudad_gestion": i.ciudad_gestion,
#                     "lider_check": i.lider_check,
#                     "meta_volumen_internet": i.meta_volumen_internet,
#                     "meta_dolares_internet": i.meta_dolares_internet,
#                     "meta_volumen_telefonia": i.meta_volumen_telefonia,
#                     "meta_dolares_telefonia": i.meta_dolares_telefonia,
#                     "meta_volumen_television": i.meta_volumen_television,
#                     "meta_dolares_television": i.meta_dolares_television,
#                     "fecha_salida": i.fecha_salida,
#                     "sector_residencia": i.sector_residencia,
#                     "email": i.email,
#                     "dias_inactivo": i.dias_inactivo,
#                     "channel": i.channel,
#                     "ciudad": i.ciudad,
#                     "region": i.region,
#                     "estado": i.estado,
#                     "operador": i.operador,
#                     "genero": i.genero,
#                     "modalidad": i.modalidad,
#                     "campana": i.campana,
#                     "isla": i.isla,
#                     "id_gerente_zonal": i.id_gerente_zonal,
#                     "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
#                     "sistema_operativo": i.sistema_operativo
#                 })

#             elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta == None:
#                 # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns(
#                 #     RegistrarGerente.c.nombre_gerente,
#                 # )
#                 # data_gerente = db.execute(query_gerente).fetchone()
#                 query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
#                     RegistrarGerenteRegional.c.nombre_gerente,
#                 ])
#                 data_gerente_regional = db.execute(
#                     query_gerente_regional).fetchone()
#                 query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns([
#                     RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
#                 ])
#                 data_gerente_ciudad = db.execute(
#                     query_gerente_ciudad).fetchone()
#                 dataInfo.append({
#                     "id_registrar_vendedor": i.id_registrar_vendedor,
#                     "id_channel": i.id_channel,
#                     "id_ciudad": i.id_ciudad,
#                     "id_operador": i.id_operador,
#                     "id_sistema_operativo": i.id_sistema_operativo,
#                     "id_estado": i.id_estado,
#                     "id_genero": i.id_genero,
#                     "id_modalidad": i.id_modalidad,
#                     "cedula": i.cedula,
#                     "telefono": i.telefono,
#                     "codigo_vendedor": i.codigo_vendedor,
#                     "usuario_equifax": i.usuario_equifax,
#                     "nombre_vendedor": i.nombre_vendedor,
#                     "fecha_ingreso": i.fecha_ingreso,
#                     "id_lider_peloton": i.id_lider_peloton,
#                     # "id_gerente": data_gerente.id_gerente,
#                     # "nombre_gerente": data_gerente.nombre_gerente,
#                     "id_gerente_regional": i.id_gerente_regional,
#                     "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
#                     "id_gerente_ciudad": i.id_gerente_ciudad,
#                     "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
#                     "id_jefe_venta": None,
#                     "nombre_jefe_venta": "Sin Jefe de Ventas",
#                     # "ciudad_gestion": i.ciudad_gestion,
#                     "lider_check": i.lider_check,
#                     "meta_volumen_internet": i.meta_volumen_internet,
#                     "meta_dolares_internet": i.meta_dolares_internet,
#                     "meta_volumen_telefonia": i.meta_volumen_telefonia,
#                     "meta_dolares_telefonia": i.meta_dolares_telefonia,
#                     "meta_volumen_television": i.meta_volumen_television,
#                     "meta_dolares_television": i.meta_dolares_television,
#                     "fecha_salida": i.fecha_salida,
#                     "sector_residencia": i.sector_residencia,
#                     "email": i.email,
#                     "dias_inactivo": i.dias_inactivo,
#                     "channel": i.channel,
#                     "ciudad": i.ciudad,
#                     "region": i.region,
#                     "estado": i.estado,
#                     "operador": i.operador,
#                     "genero": i.genero,
#                     "modalidad": i.modalidad,
#                     "campana": i.campana,
#                     "isla": i.isla,
#                     "id_gerente_zonal": i.id_gerente_zonal,
#                     "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
#                     "sistema_operativo": i.sistema_operativo
#                 })

#             elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta != None:
#                 print("entro aca", i.id_gerente_regional,
#                       i.id_gerente_ciudad, i.id_jefe_venta)
#                 # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns([
#                 #     RegistrarGerente.c.nombre_gerente,
#                 # ])
#                 # data_gerente = db.execute(query_gerente).fetchone()
#                 query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
#                     RegistrarGerenteRegional.c.nombre_gerente,
#                 ])
#                 data_gerente_regional = db.execute(
#                     query_gerente_regional).fetchone()
#                 print("data_gerente_regional",
#                       data_gerente_regional.nombre_gerente)
#                 query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns([
#                     RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
#                 ])
#                 data_gerente_ciudad = db.execute(
#                     query_gerente_ciudad).fetchone()
#                 query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns([
#                     RegistroJefeVentas.c.nombre_jefe,
#                 ])
#                 data_jefe_venta = db.execute(query_jefe_venta).fetchone()
#                 dataInfo.append({
#                     "id_registrar_vendedor": i.id_registrar_vendedor,
#                     "id_channel": i.id_channel,
#                     "id_ciudad": i.id_ciudad,
#                     "id_operador": i.id_operador,
#                     "id_sistema_operativo": i.id_sistema_operativo,
#                     "id_estado": i.id_estado,
#                     "id_genero": i.id_genero,
#                     "id_modalidad": i.id_modalidad,
#                     "cedula": i.cedula,
#                     "telefono": i.telefono,
#                     "codigo_vendedor": i.codigo_vendedor,
#                     "usuario_equifax": i.usuario_equifax,
#                     "nombre_vendedor": i.nombre_vendedor,
#                     "fecha_ingreso": i.fecha_ingreso,
#                     "id_lider_peloton": i.id_lider_peloton,
#                     # "id_gerente": data_gerente.id_gerente,
#                     # "nombre_gerente": data_gerente.nombre_gerente,
#                     "id_gerente_regional": i.id_gerente_regional,
#                     "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
#                     "id_gerente_ciudad": i.id_gerente_ciudad,
#                     "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
#                     "id_jefe_venta": i.id_jefe_venta,
#                     "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
#                     # "ciudad_gestion": i.ciudad_gestion,
#                     "lider_check": i.lider_check,
#                     "meta_volumen_internet": i.meta_volumen_internet,
#                     "meta_dolares_internet": i.meta_dolares_internet,
#                     "meta_volumen_telefonia": i.meta_volumen_telefonia,
#                     "meta_dolares_telefonia": i.meta_dolares_telefonia,
#                     "meta_volumen_television": i.meta_volumen_television,
#                     "meta_dolares_television": i.meta_dolares_television,
#                     "fecha_salida": i.fecha_salida,
#                     "sector_residencia": i.sector_residencia,
#                     "email": i.email,
#                     "dias_inactivo": i.dias_inactivo,
#                     "channel": i.channel,
#                     "ciudad": i.ciudad,
#                     "region": i.region,
#                     "estado": i.estado,
#                     "operador": i.operador,
#                     "genero": i.genero,
#                     "modalidad": i.modalidad,
#                     "campana": i.campana,
#                     "isla": i.isla,
#                     "id_gerente_zonal": i.id_gerente_zonal,
#                     "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
#                     "sistema_operativo": i.sistema_operativo
#                 })
#             elif i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta != None:

#                 query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns([
#                     RegistroJefeVentas.c.nombre_jefe,
#                 ])
#                 data_jefe_venta = db.execute(query_jefe_venta).fetchone()
#                 dataInfo.append({
#                     "id_registrar_vendedor": i.id_registrar_vendedor,
#                     "id_channel": i.id_channel,
#                     "id_ciudad": i.id_ciudad,
#                     "id_operador": i.id_operador,
#                     "id_sistema_operativo": i.id_sistema_operativo,
#                     "id_estado": i.id_estado,
#                     "id_genero": i.id_genero,
#                     "id_modalidad": i.id_modalidad,
#                     "cedula": i.cedula,
#                     "telefono": i.telefono,
#                     "codigo_vendedor": i.codigo_vendedor,
#                     "usuario_equifax": i.usuario_equifax,
#                     "nombre_vendedor": i.nombre_vendedor,
#                     "fecha_ingreso": i.fecha_ingreso,
#                     "id_lider_peloton": i.id_lider_peloton,
#                     # "id_gerente": None,
#                     # "nombre_gerente": "Sin Gerente",
#                     # "id_gerente_regional": None,
#                     # "nombre_gerente_regional": "Sin Gerente Regional",
#                     # "id_gerente_ciudad": None,
#                     # "nombre_gerente_ciudad": "Sin Gerente Ciudad",
#                     "id_jefe_venta": i.id_jefe_venta,
#                     "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
#                     # "ciudad_gestion": i.ciudad_gestion,
#                     "lider_check": i.lider_check,
#                     "meta_volumen_internet": i.meta_volumen_internet,
#                     "meta_dolares_internet": i.meta_dolares_internet,
#                     "meta_volumen_telefonia": i.meta_volumen_telefonia,
#                     "meta_dolares_telefonia": i.meta_dolares_telefonia,
#                     "meta_volumen_television": i.meta_volumen_television,
#                     "meta_dolares_television": i.meta_dolares_television,
#                     "fecha_salida": i.fecha_salida,
#                     "sector_residencia": i.sector_residencia,
#                     "email": i.email,
#                     "dias_inactivo": i.dias_inactivo,
#                     "channel": i.channel,
#                     "ciudad": i.ciudad,
#                     "region": i.region,
#                     "estado": i.estado,
#                     "operador": i.operador,
#                     "genero": i.genero,
#                     "modalidad": i.modalidad,
#                     "campana": i.campana,
#                     "isla": i.isla,
#                     "id_gerente_zonal": i.id_gerente_zonal,
#                     "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
#                     "sistema_operativo": i.sistema_operativo
#                 })

#             else:
#                 dataInfo.append({
#                     "id_registrar_vendedor": i.id_registrar_vendedor,
#                     "id_channel": i.id_channel,
#                     "id_ciudad": i.id_ciudad,
#                     "id_operador": i.id_operador,
#                     "id_sistema_operativo": i.id_sistema_operativo,
#                     "id_estado": i.id_estado,
#                     "id_genero": i.id_genero,
#                     "id_modalidad": i.id_modalidad,
#                     "cedula": i.cedula,
#                     "telefono": i.telefono,
#                     "codigo_vendedor": i.codigo_vendedor,
#                     "usuario_equifax": i.usuario_equifax,
#                     "nombre_vendedor": i.nombre_vendedor,
#                     "fecha_ingreso": i.fecha_ingreso,
#                     "id_lider_peloton": i.id_lider_peloton,
#                     # "id_gerente": None,
#                     # "nombre_gerente": "Sin Gerente",
#                     "id_gerente_regional": None,
#                     "nombre_gerente_regional": "Sin Gerente Regional",
#                     "id_gerente_ciudad": None,
#                     "nombre_gerente_ciudad": "Sin Gerente Ciudad",
#                     "id_jefe_venta": None,
#                     "nombre_jefe_venta": "Sin Jefe de Ventas",
#                     # "ciudad_gestion": i.ciudad_gestion,
#                     "lider_check": i.lider_check,
#                     "meta_volumen_internet": i.meta_volumen_internet,
#                     "meta_dolares_internet": i.meta_dolares_internet,
#                     "meta_volumen_telefonia": i.meta_volumen_telefonia,
#                     "meta_dolares_telefonia": i.meta_dolares_telefonia,
#                     "meta_volumen_television": i.meta_volumen_television,
#                     "meta_dolares_television": i.meta_dolares_television,
#                     "fecha_salida": i.fecha_salida,
#                     "sector_residencia": i.sector_residencia,
#                     "email": i.email,
#                     "dias_inactivo": i.dias_inactivo,
#                     "channel": i.channel,
#                     "ciudad": i.ciudad,
#                     "region": i.region,
#                     "estado": i.estado,
#                     "operador": i.operador,
#                     "genero": i.genero,
#                     "modalidad": i.modalidad,
#                     "campana": i.campana,
#                     "isla": i.isla,
#                     "id_gerente_zonal": i.id_gerente_zonal,
#                     "gerente_zonal": await ZonalIdGerente(i.id_gerente_zonal),
#                     "sistema_operativo": i.sistema_operativo
#                 })

#         await SetterRedis("vendedor", dataInfo)
#         return {
#             "code": "0",
#             "data": dataInfo
#         }
#     except Exception as e:
#         return {"error": str(e)}


@registro.get("/listar_registro_id/{id_registrar_vendedor}", tags=["Vendedor"])
async def get_registroID(id_registrar_vendedor: int, request: Request):
    try:
        if id_registrar_vendedor == 0 or id_registrar_vendedor == None:
            return {"code": "-1", "error": "id_registrar_vendedor no puede ser 0 o nulo"}
        header = request.headers
        print("Headre", header["authorization"].split(" ")[1])
        decodeToken = decode_token(header["authorization"].split(" ")[1])
        print("decodeToken", decodeToken)

        query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
            Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
            Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
            Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
            SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
            Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
            Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns(
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Operador.c.operador,
                Genero.c.genero,
                Modalidad.c.modalidad,
                RegistrarVendedor.c.id_sistema_operativo,
                SistemaOperativo.c.sistema_operativo,
                RegistrarVendedor.c.id_modalidad,
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
                RegistrarVendedor.c.meta_volumen,
                RegistrarVendedor.c.meta_dolares,
                RegistrarVendedor.c.campana,
                RegistrarVendedor.c.email,
                RegistrarVendedor.c.isla,
                RegistrarVendedor.c.dias_inactivo
            ).where(RegistrarVendedor.c.id_registrar_vendedor == id_registrar_vendedor)
        data = db.execute(query).fetchall()

        if data == None:
            return {"code": "-1", "error": "No se encontraron datos"}
        if len(data) == 0:
            return {"code": "-1", "error": "No se encontraron datos"}
        print("data", data)

        dataInfo = {}
        for i in data:
            query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns(
                RegistrarGerenteRegional.c.nombre_gerente,
            )
            data_gerente_regional = db.execute(
                query_gerente_regional).fetchone()

            query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns(
                RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
            )
            data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()

            query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns(
                RegistroJefeVentas.c.nombre_jefe,
            )
            data_jefe_venta = db.execute(query_jefe_venta).fetchone()

            if i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
                dataInfo = {
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    "id_gerente_regional": None,
                    "nombre_gerente_regional": "Sin Gerente Regional",
                    "id_gerente_ciudad": None,
                    "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen": i.meta_volumen,
                    "meta_dolares": i.meta_dolares,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "campana": i.isla,
                    "sistema_operativo": i.sistema_operativo
                }
            elif i.id_gerente_regional != None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:

                dataInfo = {
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    "id_gerente_regional": i.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": None,
                    "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen": i.meta_volumen,
                    "meta_dolares": i.meta_dolares,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "sistema_operativo": i.sistema_operativo
                }
            elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta == None:
                dataInfo = {
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    "id_gerente_regional": i.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen": i.meta_volumen,
                    "meta_dolares": i.meta_dolares,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "sistema_operativo": i.sistema_operativo
                }
            elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta != None:
                dataInfo = {
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    "id_gerente_regional": i.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
                    "id_jefe_venta": i.id_jefe_venta,
                    "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen": i.meta_volumen,
                    "meta_dolares": i.meta_dolares,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "sistema_operativo": i.sistema_operativo
                }
            else:
                dataInfo = {
                    "id_registrar_vendedor": i.id_registrar_vendedor,
                    "id_channel": i.id_channel,
                    "id_ciudad": i.id_ciudad,
                    "id_operador": i.id_operador,
                    "id_sistema_operativo": i.id_sistema_operativo,
                    "id_estado": i.id_estado,
                    "id_genero": i.id_genero,
                    "id_modalidad": i.id_modalidad,
                    "cedula": i.cedula,
                    "telefono": i.telefono,
                    "codigo_vendedor": i.codigo_vendedor,
                    "usuario_equifax": i.usuario_equifax,
                    "nombre_vendedor": i.nombre_vendedor,
                    "fecha_ingreso": i.fecha_ingreso,
                    # "id_gerente": None,
                    # "nombre_gerente": "Sin Gerente",
                    "id_gerente_regional": None,
                    "nombre_gerente_regional": "Sin Gerente Regional",
                    "id_gerente_ciudad": None,
                    "nombre_gerente_ciudad": "Sin Gerente Ciudad",
                    "id_jefe_venta": None,
                    "nombre_jefe_venta": "Sin Jefe de Ventas",
                    # "ciudad_gestion": i.ciudad_gestion,
                    "lider_check": i.lider_check,
                    "meta_volumen": i.meta_volumen,
                    "meta_dolares": i.meta_dolares,
                    "fecha_salida": i.fecha_salida,
                    "sector_residencia": i.sector_residencia,
                    "email": i.email,
                    "dias_inactivo": i.dias_inactivo,
                    "channel": i.channel,
                    "ciudad": i.ciudad,
                    "region": i.region,
                    "estado": i.estado,
                    "operador": i.operador,
                    "genero": i.genero,
                    "modalidad": i.modalidad,
                    "campana": i.campana,
                    "isla": i.isla,
                    "sistema_operativo": i.sistema_operativo
                }

            if dataInfo:
                return {
                    "code": "0",
                    "data": dataInfo
                }
            else:
                return {
                    "code": "1",
                    "data": "No se encontraron datos"
                }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_registro", tags=["Vendedor"])
async def post_registro(request: RegistrarVendedorModel):
    try:
        print("\n")
        print("request: ", request)
        print("\n")
        query = RegistrarVendedor.insert().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_operador=request.id_operador,
            id_sistema_operativo=request.id_sistema_operativo,
            id_estado=request.id_estado,
            id_genero=request.id_genero,
            id_modalidad=request.id_modalidad,
            cedula=request.cedula,
            telefono=request.telefono,
            codigo_vendedor=request.codigo_vendedor,
            usuario_equifax=request.usuario_equifax,
            nombre_vendedor=request.nombre_vendedor,
            fecha_ingreso=request.fecha_ingreso,
            # id_gerente=request.id_gerente,
            id_gerente_regional=request.id_gerente_regional,
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_jefe_venta=request.id_jefe_venta,
            id_lider_peloton=0 if request.id_lider_peloton == None else request.id_lider_peloton,
            # ciudad_gestion=request.ciudad_gestion,
            lider_check=request.lider_check,
            meta_volumen_internet=request.meta_volumen_internet,
            meta_dolares_internet=request.meta_dolares_internet,
            meta_volumen_telefonia=request.meta_volumen_telefonia,
            meta_dolares_telefonia=request.meta_dolares_telefonia,
            meta_volumen_television=request.meta_volumen_television,
            meta_dolares_television=request.meta_dolares_television,
            fecha_salida=request.fecha_salida,
            sector_residencia=request.sector_residencia,
            campana=request.campana,
            email=request.email,
            isla=request.isla,
            id_gerente_zonal=request.id_gerente_zonal,
            dias_inactivo=0 if request.dias_inactivo == None else request.dias_inactivo,
        )
        data = db.execute(query).lastrowid

        query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == request.id_gerente_regional).with_only_columns(
            RegistrarGerenteRegional.c.nombre_gerente,
        )
        data_gerente_regional = db.execute(
            query_gerente_regional).fetchone()

        # print("data_gerente_regional", data_gerente_regional.nombre_gerente)
        query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == request.id_gerente_ciudad).with_only_columns(
            RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
        )

        data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()

        query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == request.id_jefe_venta).with_only_columns(
            RegistroJefeVentas.c.nombre_jefe,
            RegistroJefeVentas.c.cedula,
        )
        data_jefe_venta = db.execute(query_jefe_venta).fetchone()

        # consultar el ultimo id insertado para guardarlo en redis con todas sus relaciones
        query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
            Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
            Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
            Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
            SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
            Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
            Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns(
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Operador.c.operador,
                Genero.c.genero,
                Modalidad.c.modalidad,
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
                RegistrarVendedor.c.campana,
                RegistrarVendedor.c.isla,
                RegistrarVendedor.c.id_gerente_zonal,
                RegistrarVendedor.c.dias_inactivo
            ).where(RegistrarVendedor.c.id_registrar_vendedor == data)
        data_ = db.execute(query).fetchall()
        # serializar el objeto para guardarlo en redis
        serializable = {
            "id_registrar_vendedor": data_[0].id_registrar_vendedor,
            "id_channel": data_[0].id_channel,
            "id_ciudad": data_[0].id_ciudad,
            "id_operador": data_[0].id_operador,
            "id_sistema_operativo": data_[0].id_sistema_operativo,
            "id_estado": data_[0].id_estado,
            "id_genero": data_[0].id_genero,
            "id_modalidad": data_[0].id_modalidad,
            "cedula": data_[0].cedula,
            "telefono": data_[0].telefono,
            "codigo_vendedor": data_[0].codigo_vendedor,
            "usuario_equifax": data_[0].usuario_equifax,
            "nombre_vendedor": data_[0].nombre_vendedor,
            "fecha_ingreso": data_[0].fecha_ingreso,
            "id_lider_peloton": data_[0].id_lider_peloton,
            # "id_gerente": data_gerente.id_gerente,
            # "nombre_gerente": data_gerente.nombre_gerente,
            "id_gerente_regional": data_[0].id_gerente_regional,
            "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
            "id_gerente_ciudad": data_[0].id_gerente_ciudad,
            "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
            "id_jefe_venta": data_[0].id_jefe_venta,
            "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
            # "ciudad_gestion": i.ciudad_gestion,
            "lider_check": data_[0].lider_check,
            "meta_volumen_internet": data_[0].meta_volumen_internet,
            "meta_dolares_internet": data_[0].meta_dolares_internet,
            "meta_volumen_telefonia": data_[0].meta_volumen_telefonia,
            "meta_dolares_telefonia": data_[0].meta_dolares_telefonia,
            "meta_volumen_television": data_[0].meta_volumen_television,
            "meta_dolares_television": data_[0].meta_dolares_television,
            "fecha_salida": data_[0].fecha_salida,
            "sector_residencia": data_[0].sector_residencia,
            "email": data_[0].email,
            "dias_inactivo": data_[0].dias_inactivo,
            "channel": data_[0].channel,
            "ciudad": data_[0].ciudad,
            "region": data_[0].region,
            "estado": data_[0].estado,
            "operador": data_[0].operador,
            "genero": data_[0].genero,
            "modalidad": data_[0].modalidad,
            "campana": data_[0].campana,
            "isla": data_[0].isla,
            "id_gerente_zonal": data_[0].id_gerente_zonal,
            "gerente_zonal": await ZonalIdGerente(data_[0].id_gerente_zonal),
            "sistema_operativo": data_[0].sistema_operativo
        }
        await AddRedis(f"{data_jefe_venta[1]}_vendedor", serializable)
        # Enviar registro a xtrim por rabbitMQ
        # SE COMENTA POR ERRORES EN PROD
        # body_new = {
        #     "enable": request.id_estado != 2,
        #     "attributes": {
        #         "seller_code": f"{request.codigo_vendedor}", "boss_sales_manager": f"{data_jefe_venta[1]}",
        #         "cedula": f"{request.cedula}", "ciudad": f"{data_[0].ciudad}",
        #         "telefono": f"{data_[0].telefono}",
        #         "channel": f"{data_[0].channel}", "operador": f"{data_[0].operador}",
        #         "modalidad": f"{data_[0].modalidad}",
        #         "usuario_equipax": f"{data_[0].usuario_equifax}", "fecha_ingreso": f"{data_[0].fecha_ingreso}",
        #         "fecha_salida": f"{data_[0].fecha_salida}",
        #         "sector_residencia": f"{data_[0].sector_residencia}"
        #     },
        #     "email": f"{data_[0].email}", "last_name": "", "name": f"{data_[0].nombre_vendedor}",
        #     "rol": "vendedor",
        #     "user_name": f"{request.codigo_vendedor}"
        # }
        # a = EmitRabbitMQNewUser(body_new)
        # a.start()
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        print("error", e)
        return {"error": str(e)}


@registro.put("/actualizar_registro", tags=["Vendedor"])
async def put_registro(request: RegistrarVendedorModel):
    try:
        print("lo que e llegas", request)
        query = RegistrarVendedor.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_operador=request.id_operador,
            id_sistema_operativo=request.id_sistema_operativo,
            id_estado=request.id_estado,
            id_genero=request.id_genero,
            id_modalidad=request.id_modalidad,
            cedula=request.cedula,
            telefono=request.telefono,
            codigo_vendedor=request.codigo_vendedor,
            usuario_equifax=request.usuario_equifax,
            nombre_vendedor=request.nombre_vendedor,
            fecha_ingreso=request.fecha_ingreso,
            id_gerente_regional=request.id_gerente_regional,
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_jefe_venta=request.id_jefe_venta,
            id_lider_peloton=0 if request.id_lider_peloton == None else request.id_lider_peloton,
            lider_check=request.lider_check,
            meta_volumen_internet=request.meta_volumen_internet,
            meta_dolares_internet=request.meta_dolares_internet,
            meta_volumen_telefonia=request.meta_volumen_telefonia,
            meta_dolares_telefonia=request.meta_dolares_telefonia,
            meta_volumen_television=request.meta_volumen_television,
            meta_dolares_television=request.meta_dolares_television,
            fecha_salida=request.fecha_salida,
            sector_residencia=request.sector_residencia,
            email=request.email,
            campana=request.campana,
            isla=request.isla,
            id_gerente_zonal=request.id_gerente_zonal,
            dias_inactivo=0 if request.dias_inactivo == None else request.dias_inactivo,
        ).where(RegistrarVendedor.c.id_registrar_vendedor == request.id_registrar_vendedor)
        data = db.execute(query).lastrowid

        print("data", data)

        query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == request.id_gerente_regional).with_only_columns(
            RegistrarGerenteRegional.c.nombre_gerente,
        )
        data_gerente_regional = db.execute(
            query_gerente_regional).fetchone()

        print("data_gerente_regional", data_gerente_regional.nombre_gerente)
        query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == request.id_gerente_ciudad).with_only_columns(
            RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
        )

        data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()

        query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == request.id_jefe_venta).with_only_columns(
            RegistroJefeVentas.c.nombre_jefe,
            RegistroJefeVentas.c.cedula,
        )
        data_jefe_venta = db.execute(query_jefe_venta).fetchone()
        # consultar el ultimo id insertado para guardarlo en redis con todas sus relaciones
        query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
            Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
            Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
            Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
            SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
            Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
            Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns(
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Operador.c.operador,
                Genero.c.genero,
                Modalidad.c.modalidad,
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
                RegistrarVendedor.c.campana,
                RegistrarVendedor.c.isla,
                RegistrarVendedor.c.id_gerente_zonal,
                RegistrarVendedor.c.dias_inactivo
            ).where(RegistrarVendedor.c.id_registrar_vendedor == request.id_registrar_vendedor)
        data = db.execute(query).fetchall()
        # serializar el objeto para guardarlo en redis
        serializable = {
            "id_registrar_vendedor": data[0].id_registrar_vendedor,
            "id_channel": data[0].id_channel,
            "id_ciudad": data[0].id_ciudad,
            "id_operador": data[0].id_operador,
            "id_sistema_operativo": data[0].id_sistema_operativo,
            "id_estado": data[0].id_estado,
            "id_genero": data[0].id_genero,
            "id_modalidad": data[0].id_modalidad,
            "cedula": data[0].cedula,
            "telefono": data[0].telefono,
            "codigo_vendedor": data[0].codigo_vendedor,
            "usuario_equifax": data[0].usuario_equifax,
            "nombre_vendedor": data[0].nombre_vendedor,
            "fecha_ingreso": data[0].fecha_ingreso,
            "id_lider_peloton": data[0].id_lider_peloton,
            # "id_gerente": data_gerente.id_gerente,
            # "nombre_gerente": data_gerente.nombre_gerente,
            "id_gerente_regional": data[0].id_gerente_regional,
            "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
            "id_gerente_ciudad": data[0].id_gerente_ciudad,
            "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
            "id_jefe_venta": data[0].id_jefe_venta,
            "nombre_jefe_venta": data_jefe_venta.nombre_jefe,
            # "ciudad_gestion": i.ciudad_gestion,
            "lider_check": data[0].lider_check,
            "meta_volumen_internet": data[0].meta_volumen_internet,
            "meta_dolares_internet": data[0].meta_dolares_internet,
            "meta_volumen_telefonia": data[0].meta_volumen_telefonia,
            "meta_dolares_telefonia": data[0].meta_dolares_telefonia,
            "meta_volumen_television": data[0].meta_volumen_television,
            "meta_dolares_television": data[0].meta_dolares_television,
            "fecha_salida": data[0].fecha_salida,
            "sector_residencia": data[0].sector_residencia,
            "email": data[0].email,
            "dias_inactivo": data[0].dias_inactivo,
            "channel": data[0].channel,
            "ciudad": data[0].ciudad,
            "region": data[0].region,
            "estado": data[0].estado,
            "operador": data[0].operador,
            "genero": data[0].genero,
            "modalidad": data[0].modalidad,
            "campana": data[0].campana,
            "isla": data[0].isla,
            "id_gerente_zonal": data[0].id_gerente_zonal,
            "gerente_zonal": await ZonalIdGerente(data[0].id_gerente_zonal),
            "sistema_operativo": data[0].sistema_operativo
        }
        await UpdateRedis(f"{data_jefe_venta[1]}_vendedor", serializable)
        # SE COMENTA POR ERRORES EN PROD
        # body_new = {
        #     "edited": {"enable": request.id_estado != 2,
        #                "attributes": {
        #                    "seller_code": f"{request.codigo_vendedor}", "boss_sales_manager": f"{data_jefe_venta[1]}",
        #                    "cedula": f"{request.cedula}", "ciudad": f"{data[0].ciudad}",
        #                    "telefono": f"{data[0].telefono}",
        #                    "channel": f"{data[0].channel}", "operador": f"{data[0].operador}",
        #                    "modalidad": f"{data[0].modalidad}",
        #                    "usuario_equipax": f"{data[0].usuario_equifax}", "fecha_ingreso": f"{data[0].fecha_ingreso}",
        #                    "fecha_salida": f"{data[0].fecha_salida}",
        #                    "sector_residencia": f"{data[0].sector_residencia}"
        #                },
        #                "email": f"{data[0].email}", "last_name": "", "name": f"{data[0].nombre_vendedor}",
        #                "rol": "vendedor",
        #                "user_name": f"{request.codigo_vendedor}"
        #                },
        #     "cedula": f"{request.cedula}",
        # }
        # a = EmitRabbitMQEditUser(body_new)
        # a.start()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        print("error", e)
        return {"error": e.args}


@registro.delete("/eliminar_registro/{id_registrar_vendedor}", tags=["Vendedor"])
async def delete_registro(id_registrar_vendedor: int):
    try:
        query = RegistrarVendedor.delete().where(
            RegistrarVendedor.c.id_registrar_vendedor == id_registrar_vendedor)
        data = db.execute(query)
        await DeleteRedis("vendedor", id_registrar_vendedor)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Reistrar Distribuidor
@registro.get("/listar_distribuidor", tags=["Distribuidor"])
async def get_distribuidor():
    try:
        query = RegistrarDistribuidor.join(
            Estados, Estados.c.id_estado == RegistrarDistribuidor.c.id_estado).select().with_only_columns(
                RegistrarDistribuidor.c.id_registrar_distribuidor,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarDistribuidor.c.nombre_distribuidor,
                RegistrarDistribuidor.c.responsable,
                RegistrarDistribuidor.c.telefono,
                RegistrarDistribuidor.c.email,
                RegistrarDistribuidor.c.fecha_ingreso,
                RegistrarDistribuidor.c.fecha_salida
            )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_registrar_distribuidor": i.id_registrar_distribuidor,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "nombre_distribuidor": i.nombre_distribuidor,
                "responsable": i.responsable,
                "telefono": i.telefono,
                "email": i.email,
                "fecha_ingreso": i.fecha_ingreso,
                "fecha_salida": i.fecha_salida,
                "ciudades_asignadas": await ListarCiudadesDistribuidor(i.id_registrar_distribuidor),
                "canales_asignados": await ListarCanalesDistribuidor(i.id_registrar_distribuidor)
            })
        return {
            "code": "0",
            "data": infoData
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_distribuidor", tags=["Distribuidor"])
async def post_distribuidor(request: RegistrarDistribuidorModel):
    try:
        query = RegistrarDistribuidor.insert().values(
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_distribuidor=request.nombre_distribuidor,
            responsable=request.responsable,
            telefono=request.telefono,
            email=request.email,
            fecha_ingreso=request.fecha_ingreso,
            fecha_salida=request.fecha_salida
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_distribuidor", tags=["Distribuidor"])
async def put_distribuidor(request: RegistrarDistribuidorModel):
    try:
        query = RegistrarDistribuidor.update().values(
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_distribuidor=request.nombre_distribuidor,
            responsable=request.responsable,
            telefono=request.telefono,
            email=request.email,
            fecha_ingreso=request.fecha_ingreso,
            fecha_salida=request.fecha_salida
        ).where(RegistrarDistribuidor.c.id_registrar_distribuidor == request.id_registrar_distribuidor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_distribuidor/{id_registrar_distribuidor}", tags=["Distribuidor"])
async def delete_distribuidor(id_registrar_distribuidor: int):
    try:

        db.execute(asignacion_ciudades_distribuidor.delete().where(
            asignacion_ciudades_distribuidor.c.id_registrar_distribuidor == id_registrar_distribuidor))

        db.execute(asignacion_canal_distribuidor.delete().where(
            asignacion_canal_distribuidor.c.id_registrar_distribuidor == id_registrar_distribuidor))

        query = RegistrarDistribuidor.delete().where(
            RegistrarDistribuidor.c.id_registrar_distribuidor == id_registrar_distribuidor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Registrar Jefe de Venta
@registro.get("/listar_jefe_venta", tags=["Jefe de Venta"])
async def get_jefe_venta():
    try:
        query = RegistroJefeVentas.select().with_only_columns(
            RegistroJefeVentas.c.id_jefe_venta,
            RegistroJefeVentas.c.id_estado,
            RegistroJefeVentas.c.id_gerente_ciudad,
            RegistroJefeVentas.c.nombre_jefe,
            RegistroJefeVentas.c.ciudad,
            RegistroJefeVentas.c.email,
            RegistroJefeVentas.c.telefono,
            RegistroJefeVentas.c.cedula,
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            estado = db.execute(Estados.select().where(
                Estados.c.id_estado == i.id_estado)).first()
            print(i.id_gerente_ciudad)
            if i.id_gerente_ciudad == None:
                infoData.append({
                    "id_jefe_venta": i.id_jefe_venta,
                    "id_estado": i.id_estado,
                    "estado": estado.estado,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_jefe": i.nombre_jefe,
                    "ciudad": i.ciudad,
                    "email": i.email,
                    "telefono": i.telefono,
                    "cedula": i.cedula,
                    "nombre_gerente": "Sin asignar",
                    "ciudades_asignadas": await ListarCiudadesJVCiudad(i.id_jefe_venta),
                    "canales_asignados": await ListarCanalesJVCiudad(i.id_jefe_venta)
                })
            else:
                query = RegistrarGerenteCiudad.select().where(
                    RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad)
                data = db.execute(query).first()
                infoData.append({
                    "id_jefe_venta": i.id_jefe_venta,
                    "id_estado": i.id_estado,
                    "estado": estado.estado,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_jefe": i.nombre_jefe,
                    "nombre_gerente": data.nombre_gerente_ciudad,
                    "ciudad": i.ciudad,
                    "email": i.email,
                    "telefono": i.telefono,
                    "cedula": i.cedula,
                    "ciudades_asignadas": await ListarCiudadesJVCiudad(i.id_jefe_venta),
                    "canales_asignados": await ListarCanalesJVCiudad(i.id_jefe_venta)
                })

        return {
            "code": "0",
            "data": infoData
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_jefe_venta", tags=["Jefe de Venta"])
async def post_jefe_venta(request: RegistrarJefeModel):
    try:
        query = RegistroJefeVentas.insert().values(
            id_estado=request.id_estado,
            id_gerente_ciudad=request.id_gerente_ciudad,
            nombre_jefe=request.nombre_jefe,
            ciudad=request.ciudad,
            email=request.email,
            telefono=request.telefono,
            cedula=request.cedula,
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_jefe_venta", tags=["Jefe de Venta"])
async def put_jefe_venta(request: RegistrarJefeModel):
    try:
        query = RegistroJefeVentas.update().values(
            id_jefe_venta=request.id_jefe_venta,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            id_gerente_ciudad=request.id_gerente_ciudad,
            nombre_jefe=request.nombre_jefe,
            ciudad=request.ciudad,
            email=request.email,
            telefono=request.telefono,
            cedula=request.cedula,
        ).where(RegistroJefeVentas.c.id_jefe_venta == request.id_jefe_venta)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_jefe_venta/{id_jefe_venta}", tags=["Jefe de Venta"])
async def delete_jefe_venta(id_jefe_venta: int):
    try:
        db.execute(asignacion_ciudades_jefe_ventas.delete().where(
            asignacion_ciudades_jefe_ventas.c.id_jefe_venta == id_jefe_venta))

        db.execute(asignacion_canal_jefe_ventas.delete().where(
            asignacion_canal_jefe_ventas.c.id_jefe_venta == id_jefe_venta))

        query = RegistroJefeVentas.delete().where(
            RegistroJefeVentas.c.id_jefe_venta == id_jefe_venta)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Registrar Administrador


@registro.get("/listar_administrador", tags=["Administrador"])
async def get_administrador():
    try:
        query = RegistroAdministrador.join(
            Estados, Estados.c.id_estado == RegistroAdministrador.c.id_estado).select().with_only_columns(
                RegistroAdministrador.c.id_administrador,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistroAdministrador.c.id_roles,
                RegistroAdministrador.c.email,
                RegistroAdministrador.c.perfil,
                RegistroAdministrador.c.nombre_administrador
            )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_administrador": i.id_administrador,
                "id_roles": i.id_roles,
                "email": i.email,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "perfil": i.perfil,
                "nombre_administrador": i.nombre_administrador,
                "ciudades_asignadas": await ListarCiudadesAdminCiudad(i.id_administrador),
                "canales_asignados": await ListarCanalesAdminCiudad(i.id_administrador)
            })
        return {
            "code": "0",
            "data": infoData
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_administrador", tags=["Administrador"])
async def post_administrador(request: RegistrarAdministradorModel):
    try:
        query = RegistroAdministrador.insert().values(
            id_estado=request.id_estado,
            email=request.email,
            password=encryptPassword(request.password),
            id_roles=request.id_roles,
            perfil=request.perfil,
            nombre_administrador=request.nombre_administrador,
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_administrador", tags=["Administrador"])
async def put_administrador(request: RegistrarAdministradorModelNew):
    try:
        if request.new_password == "" or request.new_password == None:
            data = db.execute(RegistroAdministrador.update().values(
                id_estado=request.id_estado,
                id_roles=request.id_roles,
                email=request.email,
                perfil=request.perfil,
                nombre_administrador=request.nombre_administrador
            ).where(RegistroAdministrador.c.id_administrador == request.id_administrador))
            return {
                "code": "0",
                "data": data
            }
        else:
            data = db.execute(RegistroAdministrador.update().values(
                id_estado=request.id_estado,
                id_roles=request.id_roles,
                email=request.email,
                password=encryptPassword(request.new_password),
                nombre_administrador=request.nombre_administrador
            ).where(RegistroAdministrador.c.id_administrador == request.id_administrador))
            return {
                "code": "0",
                "data": data
            }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_administrador", tags=["Administrador"])
async def delete_administrador(id_administrador: int):
    try:
        db.execute(asignacion_ciudades_admin.delete().where(
            asignacion_ciudades_admin.c.id_administrador == id_administrador))
        db.execute(asignacion_canal_admin.delete().where(
            asignacion_canal_admin.c.id_administrador == id_administrador))

        query = RegistroAdministrador.delete().where(
            RegistroAdministrador.c.id_administrador == id_administrador)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Registrar gerente regional
@registro.get("/listar_gerente_regional", tags=["Gerente Regional"])
async def get_gerente_regional():
    try:
        query = RegistrarGerenteRegional.join(
            Estados, Estados.c.id_estado == RegistrarGerenteRegional.c.id_estado).select().with_only_columns(
                RegistrarGerenteRegional.c.id_gerente_regional,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteRegional.c.nombre_gerente,
                RegistrarGerenteRegional.c.ciudad,
                RegistrarGerenteRegional.c.email,
                RegistrarGerenteRegional.c.telefono,
                RegistrarGerenteRegional.c.cedula
            )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_gerente_regional": i.id_gerente_regional,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "nombre_gerente": i.nombre_gerente,
                "ciudad": i.ciudad,
                "email": i.email,
                "telefono": i.telefono,
                "cedula": i.cedula,
                "ciudades_asignadas": await ListarCiudadesGRegional(i.id_gerente_regional),
                "canales_asignados": await ListarCanalesGRciudad(i.id_gerente_regional)
            })
        return {
            "code": "0",
            "data": infoData
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_gerente_regional", tags=["Gerente Regional"])
async def post_gerente_regional(request: RegistrarGerenteRegionalModel):
    try:
        query = RegistrarGerenteRegional.insert().values(
            id_gerente_regional=request.id_gerente_regional,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente=request.nombre_gerente,
            ciudad=request.ciudad,
            email=request.email,
            telefono=request.telefono,
            cedula=request.cedula,
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_gerente_regional", tags=["Gerente Regional"])
async def put_gerente_regional(request: RegistrarGerenteRegionalModel):
    try:
        db.execute(RegistrarGerenteRegional.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente=request.nombre_gerente,
            ciudad=request.ciudad,
            email=request.email,
            telefono=request.telefono,
            cedula=request.cedula,
        ).where(RegistrarGerenteRegional.c.id_gerente_regional == request.id_gerente_regional))
        return {
            "code": "0"
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_gerente_regional/{id_gerente_regional}", tags=["Gerente Regional"])
async def delete_gerente_regional(id_gerente_regional: int):
    try:
        db.execute(asignacion_ciudades_gerente_regional.delete().where(
            asignacion_ciudades_gerente_regional.c.id_gerente_regional == id_gerente_regional))
        db.execute(asiganacion_canal_gerente_regional.delete().where(
            asiganacion_canal_gerente_regional.c.id_gerente_regional == id_gerente_regional))

        query = RegistrarGerenteRegional.delete().where(
            RegistrarGerenteRegional.c.id_gerente_regional == id_gerente_regional)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Registrar gerente de ciudad
@registro.get("/listar_gerente_ciudad", tags=["Gerente de Ciudad"])
async def get_gerente_ciudad():
    try:
        query = RegistrarGerenteCiudad.join(
            Estados, Estados.c.id_estado == RegistrarGerenteCiudad.c.id_estado).select().with_only_columns(
                RegistrarGerenteCiudad.c.id_gerente_ciudad,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                RegistrarGerenteCiudad.c.ciudad,
                RegistrarGerenteCiudad.c.email,
                RegistrarGerenteCiudad.c.telefono,
                RegistrarGerenteCiudad.c.cedula,
            )
        data = db.execute(query).fetchall()
        infodata = []
        for i in data:
            infodata.append({
                "id_gerente_ciudad": i.id_gerente_ciudad,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "nombre_gerente_ciudad": i.nombre_gerente_ciudad,
                "ciudad": i.ciudad,
                "email": i.email,
                "telefono": i.telefono,
                "cedula": i.cedula,
                "ciudades_asignadas": await ListarCiudadesGCiudad(i.id_gerente_ciudad),
                "canales_asignados": await ListarCanalesGCiudad(i.id_gerente_ciudad)
            })
        return {
            "code": "0",
            "data": infodata
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_gerente_ciudad", tags=["Gerente de Ciudad"])
async def post_gerente_ciudad(request: RegistrarGerenteCiudadModel):
    try:
        query = RegistrarGerenteCiudad.insert().values(
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente_ciudad=request.nombre_gerente_ciudad,
            ciudad=request.ciudad,
            email=request.email,
            telefono=request.telefono,
            cedula=request.cedula
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_gerente_ciudad", tags=["Gerente de Ciudad"])
async def put_gerente_ciudad(request: RegistrarGerenteCiudadModel):
    try:
        db.execute(RegistrarGerenteCiudad.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente_ciudad=request.nombre_gerente_ciudad,
            ciudad=request.ciudad,
            email=request.email,
            telefono=request.telefono,
            cedula=request.cedula
        ).where(RegistrarGerenteCiudad.c.id_gerente_ciudad == request.id_gerente_ciudad))
        return {
            "code": "0"
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_gerente_ciudad/{id_gerente_ciudad}", tags=["Gerente de Ciudad"])
async def delete_gerente_ciudad(id_gerente_ciudad: int):
    try:
        db.execute(asignacion_ciudades_gerente_ciudad.delete().where(
            asignacion_ciudades_gerente_ciudad.c.id_gerente_ciudad == id_gerente_ciudad))

        db.execute(asignacion_canal_gerente_ciudad.delete().where(
            asignacion_canal_gerente_ciudad.c.id_gerente_ciudad == id_gerente_ciudad))

        query = RegistrarGerenteCiudad.delete().where(
            RegistrarGerenteCiudad.c.id_gerente_ciudad == id_gerente_ciudad)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Administrador de proyectos
@registro.get("/listar_administrador_proyectos", tags=["Administrador de Proyectos"])
async def get_administrador_proyectos():
    try:
        query = RegistrarAdminProyectos.join(Estados, Estados.c.id_estado == RegistrarAdminProyectos.c.id_estado).select().with_only_columns(
            RegistrarAdminProyectos.c.id_admin_proyectos,
            Estados.c.estado,
            Estados.c.id_estado,
            RegistrarAdminProyectos.c.nombre_admin_proyectos
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_admin_proyectos": i.id_admin_proyectos,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "nombre_admin_proyectos": i.nombre_admin_proyectos,
                "ciudades_asignadas": await ListarCiudadesAPCiudad(i.id_admin_proyectos),
                "canales_asignados": await ListarCanalesAPCiudad(i.id_admin_proyectos)
            })
        return {
            "code": "0",
            "data": infoData
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_administrador_proyectos", tags=["Administrador de Proyectos"])
async def post_administrador_proyectos(request: RegistrarAdminProyectosModel):
    try:
        query = RegistrarAdminProyectos.insert().values(
            id_admin_proyectos=request.id_admin_proyectos,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_admin_proyectos=request.nombre_admin_proyectos
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_administrador_proyectos", tags=["Administrador de Proyectos"])
async def put_administrador_proyectos(request: RegistrarAdminProyectosModel):
    try:
        data = db.execute(RegistrarAdminProyectos.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_admin_proyectos=request.nombre_admin_proyectos
        ).where(RegistrarAdminProyectos.c.id_admin_proyectos == request.id_admin_proyectos))
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_administrador_proyectos/{id_admin_proyectos}", tags=["Administrador de Proyectos"])
async def delete_administrador_proyectos(id_admin_proyectos: int):
    try:

        db.execute(asignacion_ciudades_admin_proyectos.delete().where(
            asignacion_ciudades_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos))

        db.execute(asignacion_canal_admin_proyectos.delete().where(
            asignacion_canal_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos))

        query = RegistrarAdminProyectos.delete().where(
            RegistrarAdminProyectos.c.id_admin_proyectos == id_admin_proyectos)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Cargar excel con los datos de vendedor y registras en la base de datos
@registro.post("/cargar_excel_vendedores", tags=["Vendedores"])
async def cargar_excel_vendedores(request: Request):
    try:
        form = await request.form()
        file = form['file']
        filename = file.filename
        extension = filename.split(".")[-1]
        df = None
        if extension == "xlsx":
            file = await file.read()
            df = pd.read_excel(file)
            df = df.to_dict(orient="records")
        elif extension == "csv":
            file = await file.read()
            df = pd.read_csv(file)
            df = df.to_dict(orient="records")
            print(df)
        else:
            return {
                "code": "1",
                "message": "El archivo debe ser de tipo excel"
            }
        nueva_lista = []
        for i in df:
            print(i["usuario_equifax"] == None)
            print(type(i["usuario_equifax"]))

            i["id_gerente_regional"] = None if i["id_gerente_regional"] == "SIN REGISTRO" else int(
                i["id_gerente_regional"])
            i["usuario_equifax"] = None if i["usuario_equifax"] == "SIN USUARIO" else i["usuario_equifax"]
            i["fecha_ingreso"] = None if i["fecha_ingreso"] == "SIN REGISTRO" else i["fecha_ingreso"]
            i["id_lider_peloton"] = 0 if i["id_lider_peloton"] == "SIN REGISTRO" else i["id_lider_peloton"]
            i["id_jefe_venta"] = None if i["id_jefe_venta"] == "SIN REGISTRO" else i["id_jefe_venta"]
            i["fecha_salida"] = None if i["fecha_salida"] == "SIN REGISTRO" else None
            i["sector_residencia"] = "SIN REGISTRO" if i["sector_residencia"] == "SIN REGISTRO" else str(
                i["sector_residencia"])
            i["meta_dolares_internet"] = float(
                str(i["meta_dolares_internet"]).replace(",", "."))
            i["meta_dolares_telefonia"] = float(
                str(i["meta_dolares_telefonia"]).replace(",", "."))
            i["meta_dolares_television"] = float(
                str(i["meta_dolares_television"]).replace(",", "."))
            i["fecha_salida"] = None if i["fecha_salida"] == "SIN REGISTRO" else None
            print(ModelVendedorExcel(**i))
            nueva_lista.append(ModelVendedorExcel(**i))

        for i in nueva_lista:
            query = RegistrarVendedor.insert().values(
                id_channel=i.id_channel,
                id_ciudad=i.id_ciudad,
                id_operador=i.id_operador,
                id_sistema_operativo=i.id_sistema_operativo,
                id_estado=i.id_estado,
                id_genero=i.id_genero,
                id_modalidad=i.id_modalidad,
                codigo_vendedor=i.codigo_vendedor,
                usuario_equifax=i.usuario_equifax,
                nombre_vendedor=i.nombre_vendedor,
                fecha_ingreso=i.fecha_ingreso,
                id_gerente_regional=i.id_gerente_regional,
                id_gerente_ciudad=i.id_gerente_ciudad,
                id_jefe_venta=i.id_jefe_venta,
                id_lider_peloton=i.id_lider_peloton,
                meta_volumen_internet=i.meta_volumen_internet,
                meta_dolares_internet=i.meta_dolares_internet,
                meta_volumen_telefonia=i.meta_volumen_telefonia,
                meta_dolares_telefonia=i.meta_dolares_telefonia,
                meta_volumen_television=i.meta_volumen_television,
                meta_dolares_television=i.meta_dolares_television,
                fecha_salida=i.fecha_salida,
                sector_residencia=i.sector_residencia,
                email=i.email,
                cedula=i.cedula,
                telefono=i.telefono,
                dias_inactivo=i.dias_inactivo,
            )
            db.execute(query)

        return {
            "code": "0",
            "data": nueva_lista
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# descargar ejemplo de excel prosupuesto
@registro.get("/descargar_excel_prosupuesto", tags=["Vendedores"])
async def descargar_excel_prosupuesto():
    try:
        df = pd.read_excel("static/ejemplo_prosupuesto.xlsx")
        df.to_csv("static/ejemplo_prosupuesto.xlsx", index=False)
        return FileResponse("static/ejemplo_prosupuesto.xlsx", media_type="application/octet-stream", filename="ejemplo_prosupuesto.xlsx")
    except Exception as e:
        return {
            "error": str(e)
        }

# Cargar excel con los datos de vendedor y registras en la base de datos


@registro.post("/cargar_excel_vendedores_presupuesto", tags=["Vendedores"])
async def cargar_excel_vendedores_presupuesto(request: Request):
    try:
        form = await request.form()
        file = form['file']
        filename = file.filename
        extension = filename.split(".")[-1]
        df = None
        if extension == "xlsx":
            file = await file.read()
            df = pd.read_excel(file)
            df = df.to_dict(orient="records")
        elif extension == "csv":
            file = await file.read()
            df = pd.read_csv(file)
            df = df.to_dict(orient="records")
            print(df)
        else:
            return {
                "code": "1",
                "message": "El archivo debe ser de tipo excel"
            }
        nueva_lista = []
        for i in df:
            print(ModelVendedorExcelProsupuesto(**i))
            nueva_lista.append(ModelVendedorExcelProsupuesto(**i))

        for i in nueva_lista:
            # acutalizar vendedor
            query = RegistrarVendedor.update().values(
                meta_volumen_internet=i.meta_volumen_internet,
                meta_dolares_internet=i.meta_dolares_internet,
                meta_volumen_telefonia=i.meta_volumen_telefonia,
                meta_dolares_telefonia=i.meta_dolares_telefonia,
                meta_volumen_television=i.meta_volumen_television,
                meta_dolares_television=i.meta_dolares_television,
            ).where(RegistrarVendedor.c.codigo_vendedor == i.codigo_vendedor)
            insert = db.execute(query).rowcount
            print(insert)

        return {
            "code": "0",
            "data": nueva_lista
        }

    except Exception as e:
        return {
            "error": str(e)
        }
