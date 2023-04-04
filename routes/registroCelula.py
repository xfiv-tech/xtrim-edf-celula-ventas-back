from controller.AsignacionController import ListarCanalesAPCiudad, ListarCanalesAdminCiudad, ListarCanalesDistribuidor, ListarCanalesGCiudad, ListarCanalesGRciudad, ListarCanalesJVCiudad, ListarCiudadesAPCiudad, ListarCiudadesAdminCiudad, ListarCiudadesDistribuidor, ListarCiudadesGCiudad, ListarCiudadesGRegional, ListarCiudadesJVCiudad
from function.ExtraerCiuCanl import ExtraerCiuCanl
from function.encrytPassword import encryptPassword
from function.excelReporte import get_tdd_excel_workbook
from function.ftp import ftp_connect, ftp_list
from function.function_jwt import decode_token
from middleware.validacionToken import ValidacionToken
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from model.ModelSchema.channelModel import RegistrarAdminProyectosModel, RegistrarAdministradorModel, RegistrarAdministradorModelNew, RegistrarDistribuidorModel, RegistrarGerenteCiudadModel, RegistrarGerenteRegionalModel, RegistrarJefeModel, RegistrarVendedorModel
from model.channel import Channel, Ciudad, Estados, Genero, Modalidad, Operador, RegistrarAdminProyectos, RegistrarDistribuidor, RegistrarGerenteCiudad, RegistrarGerenteRegional, RegistrarVendedor, RegistroAdministrador, RegistroJefeVentas, SistemaOperativo
from model.channel import asignacion_ciudades_admin, asignacion_canal_admin
from model.channel import asiganacion_canal_gerente_regional, asignacion_ciudades_gerente_regional
from model.channel import asignacion_ciudades_gerente_ciudad, asignacion_canal_gerente_ciudad
from model.channel import asignacion_ciudades_jefe_ventas, asignacion_canal_jefe_ventas
from model.channel import asignacion_ciudades_admin_proyectos, asignacion_canal_admin_proyectos
from model.channel import asignacion_ciudades_admin, asignacion_canal_admin
from model.channel import asignacion_ciudades_distribuidor, asignacion_canal_distribuidor
from database.db import db
from datetime import datetime

from routes.asignacion import asignacion_ciudades_administrador
# moment.need()

registro = APIRouter(route_class=ValidacionToken)

import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST_FTP")
USER = os.getenv("USER_FTP")
PASS = os.getenv("PASS_FTP")

#lista de vendedores
@registro.get("/reporte_ftp", tags=["Vendedor"])
async def get_reporteFtp(request: Request):
    try:
        fecha = datetime.now().strftime("%Y-%m-%d")
        ftp = ftp_connect(HOST, USER, PASS)
        ftplist = ftp_list(ftp, "QlikView")
        ftplistCelula = ftp_list(ftp, "Celula_Ventas")
        print("ftplist",ftplist)
        print("ftplistCelula",ftplistCelula)
        print("ftp",ftp)
        header = request.headers
        decodeToken = decode_token(header["authorization"].split(" ")[1])
        CanalCiudad = await ExtraerCiuCanl(decodeToken["id"],decodeToken["perfil"])
        ciudad = CanalCiudad["ciudad"]
        usuario = fecha+"_"+decodeToken["usuario"]+".xlsx"
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
    
#lista de vendedores
@registro.get("/listar_registro", tags=["Vendedor"])
async def get_registro(request: Request):
    try:
        header = request.headers
        decodeToken = decode_token(header["authorization"].split(" ")[1])
        CanalCiudad = await ExtraerCiuCanl(decodeToken["id"],decodeToken["perfil"])
        ciudad = CanalCiudad["ciudad"]
        data = []
        for i in ciudad:
            query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
                Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
                Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
                Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
                SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
                Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
                Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns([
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
                RegistrarVendedor.c.meta_volumen,
                RegistrarVendedor.c.meta_dolares,
                RegistrarVendedor.c.email,
                RegistrarVendedor.c.dias_inactivo
                ]).where(RegistrarVendedor.c.id_ciudad == i["id_ciudad"])         
            res = db.execute(query).fetchall()
            for i in res:
                data.append(i)

        dataInfo = []
        for i in data:
            if  i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
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
                    "sistema_operativo": i.sistema_operativo
                })

            elif i.id_gerente_regional != None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
                    RegistrarGerenteRegional.c.nombre_gerente,
                ])
                data_gerente_regional = db.execute(query_gerente_regional).fetchone()
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
                    "sistema_operativo": i.sistema_operativo
                })

            elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta == None:
                # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns([
                #     RegistrarGerente.c.nombre_gerente,
                # ])
                # data_gerente = db.execute(query_gerente).fetchone()
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
                    RegistrarGerenteRegional.c.nombre_gerente,
                ])
                data_gerente_regional = db.execute(query_gerente_regional).fetchone()
                query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns([
                    RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                ])
                data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()
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
                    "sistema_operativo": i.sistema_operativo
                })

            elif i.id_gerente_regional != None and i.id_gerente_ciudad != None and i.id_jefe_venta != None:
                print("entro aca", i.id_gerente_regional, i.id_gerente_ciudad, i.id_jefe_venta)
                # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns([
                #     RegistrarGerente.c.nombre_gerente,
                # ])
                # data_gerente = db.execute(query_gerente).fetchone()
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
                    RegistrarGerenteRegional.c.nombre_gerente,
                ])
                data_gerente_regional = db.execute(query_gerente_regional).fetchone()
                print("data_gerente_regional", data_gerente_regional.nombre_gerente)
                query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns([
                    RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                ])
                data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()
                query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns([
                    RegistroJefeVentas.c.nombre_jefe,
                ])
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
                    "sistema_operativo": i.sistema_operativo
                })
            elif i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta != None:

                query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns([
                    RegistroJefeVentas.c.nombre_jefe,
                ])
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
                    "sistema_operativo": i.sistema_operativo
                })

        return {
            "code": "0",
            "data": dataInfo
        }
    except Exception as e:
        return {"error": str(e)}


@registro.get("/listar_registro_id/{id_registrar_vendedor}", tags=["Vendedor"])
async def get_registroID(id_registrar_vendedor: int, request: Request):
    try:
        if id_registrar_vendedor == 0 or id_registrar_vendedor == None: return {"code":"-1","error": "id_registrar_vendedor no puede ser 0 o nulo"}
        header = request.headers
        print("Headre",header["authorization"].split(" ")[1])
        decodeToken = decode_token(header["authorization"].split(" ")[1])
        print("decodeToken",decodeToken)

        query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
            Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
            Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
            Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
            SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
            Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
            Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns([
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
            RegistrarVendedor.c.email,
            RegistrarVendedor.c.dias_inactivo
            ]).where(RegistrarVendedor.c.id_registrar_vendedor == id_registrar_vendedor)       
        data = db.execute(query).fetchall()

        if data == None: return {"code":"-1","error": "No se encontraron datos"}
        if len(data) == 0: return {"code":"-1","error": "No se encontraron datos"}
        print("data",data)

        dataInfo = {}
        for i in data:
            query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
                RegistrarGerenteRegional.c.nombre_gerente,
            ])
            data_gerente_regional = db.execute(query_gerente_regional).fetchone()

            query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns([
                RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
            ])
            data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()

            query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns([
                RegistroJefeVentas.c.nombre_jefe,
            ])
            data_jefe_venta = db.execute(query_jefe_venta).fetchone()

            if  i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
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
            id_lider_peloton=request.id_lider_peloton,
            # ciudad_gestion=request.ciudad_gestion,
            lider_check=request.lider_check,
            meta_volumen=request.meta_volumen,
            meta_dolares=request.meta_dolares,
            fecha_salida=request.fecha_salida,
            sector_residencia=request.sector_residencia,
            email=request.email,
            dias_inactivo=request.dias_inactivo
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_registro", tags=["Vendedor"])
async def put_registro(request: RegistrarVendedorModel):
    try:
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
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_jefe_venta=request.id_jefe_venta,
            id_lider_peloton=request.id_lider_peloton,
            lider_check=request.lider_check,
            meta_volumen=request.meta_volumen,
            meta_dolares=request.meta_dolares,
            fecha_salida=request.fecha_salida,
            sector_residencia=request.sector_residencia,
            email=request.email,
            dias_inactivo=request.dias_inactivo
        ).where(RegistrarVendedor.c.id_registrar_vendedor == request.id_registrar_vendedor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_registro/{id_registrar_vendedor}", tags=["Vendedor"])
async def delete_registro(id_registrar_vendedor: int):
    try:
        query = RegistrarVendedor.delete().where(RegistrarVendedor.c.id_registrar_vendedor == id_registrar_vendedor)
        data = db.execute(query)
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
            Estados, Estados.c.id_estado == RegistrarDistribuidor.c.id_estado).select().with_only_columns([
                RegistrarDistribuidor.c.id_registrar_distribuidor,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarDistribuidor.c.nombre_distribuidor,
                RegistrarDistribuidor.c.responsable,
                RegistrarDistribuidor.c.telefono,
                RegistrarDistribuidor.c.email,
                RegistrarDistribuidor.c.fecha_ingreso,
                RegistrarDistribuidor.c.fecha_salida
            ])       
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
        query = RegistroJefeVentas.select().with_only_columns([
                RegistroJefeVentas.c.id_jefe_venta,
                RegistroJefeVentas.c.id_estado,
                RegistroJefeVentas.c.id_gerente_ciudad,
                RegistroJefeVentas.c.nombre_jefe
            ])        
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            estado = db.execute(Estados.select().where(Estados.c.id_estado == i.id_estado)).first()
            print(i.id_gerente_ciudad)
            if i.id_gerente_ciudad == None:
                infoData.append({
                    "id_jefe_venta": i.id_jefe_venta,
                    "id_estado": i.id_estado,
                    "estado": estado.estado,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_jefe": i.nombre_jefe,
                    "nombre_gerente": "Sin asignar",
                    "ciudades_asignadas": await ListarCiudadesJVCiudad(i.id_jefe_venta),
                    "canales_asignados": await ListarCanalesJVCiudad(i.id_jefe_venta)
                })
            else:
                query = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad)
                data = db.execute(query).first()
                infoData.append({
                    "id_jefe_venta": i.id_jefe_venta,
                    "id_estado": i.id_estado,
                    "estado": estado.estado,
                    "id_gerente_ciudad": i.id_gerente_ciudad,
                    "nombre_jefe": i.nombre_jefe,
                    "nombre_gerente": data.nombre_gerente_ciudad,
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
            # id_jefe_venta=request.id_jefe_venta,
            # id_channel=request.id_channel,
            # id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            id_gerente_ciudad=request.id_gerente_ciudad,
            nombre_jefe=request.nombre_jefe
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
            Estados, Estados.c.id_estado == RegistroAdministrador.c.id_estado).select().with_only_columns([
                RegistroAdministrador.c.id_administrador,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistroAdministrador.c.id_roles,
                RegistroAdministrador.c.email,
                RegistroAdministrador.c.perfil,
                RegistroAdministrador.c.nombre_administrador
            ])           
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
async def get_gerente_ciudad():
    try:
        query = RegistrarGerenteRegional.join(
            Estados, Estados.c.id_estado == RegistrarGerenteRegional.c.id_estado).select().with_only_columns([
                RegistrarGerenteRegional.c.id_gerente_regional,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteRegional.c.nombre_gerente
            ])
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_gerente_regional": i.id_gerente_regional,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "nombre_gerente": i.nombre_gerente,
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
async def post_gerente_ciudad(request: RegistrarGerenteRegionalModel):
    try:
        query = RegistrarGerenteRegional.insert().values(
            id_gerente_regional=request.id_gerente_regional,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente=request.nombre_gerente
        )
        data = db.execute(query).lastrowid
        return {
            "code": "0",
            "id_insert": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.put("/actualizar_gerente_regional", tags=["Gerente Regional"])
async def put_gerente_ciudad(request: RegistrarGerenteRegionalModel):
    try:
        db.execute(RegistrarGerenteRegional.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente=request.nombre_gerente
        ).where(RegistrarGerenteRegional.c.id_gerente_regional == request.id_gerente_regional))
        return {
            "code": "0"
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_gerente_regional/{id_gerente_regional}", tags=["Gerente Regional"])
async def delete_gerente_ciudad(id_gerente_regional: int):
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
            Estados, Estados.c.id_estado == RegistrarGerenteCiudad.c.id_estado).select().with_only_columns([
                RegistrarGerenteCiudad.c.id_gerente_ciudad,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteCiudad.c.nombre_gerente_ciudad
            ])
        data = db.execute(query).fetchall()
        infodata = []
        for i in data:
            infodata.append({
                "id_gerente_ciudad": i.id_gerente_ciudad,
                "id_estado": i.id_estado,
                "estado": i.estado,
                "nombre_gerente_ciudad": i.nombre_gerente_ciudad,
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
            nombre_gerente_ciudad=request.nombre_gerente_ciudad
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
            nombre_gerente_ciudad=request.nombre_gerente_ciudad
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
        query = RegistrarAdminProyectos.join(Estados, Estados.c.id_estado == RegistrarAdminProyectos.c.id_estado).select().with_only_columns([
                RegistrarAdminProyectos.c.id_admin_proyectos,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarAdminProyectos.c.nombre_admin_proyectos
            ])        
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
