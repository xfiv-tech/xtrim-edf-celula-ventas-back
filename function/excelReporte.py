from openpyxl import Workbook
from pydantic import BaseModel

from model.channel import Channel, Ciudad, Estados, Genero, Modalidad, Operador, RegistrarGerente, RegistrarGerenteCiudad, RegistrarGerenteRegional, RegistrarVendedor, RegistroJefeVentas, SistemaOperativo 
from database.db import db

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
    ciudad_gestion: str 
    lider_check: bool 
    meta_volumen: int 
    meta_dolares: float 
    fecha_salida: str 
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



async def get_infoReporte():
    try:
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
            # RegistrarVendedor.c.id_gerente,
            # RegistrarVendedor.c.ciudad_gestion,
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
            ])         
        data = db.execute(query).fetchall()
        dataInfo = []
        for i in data:
            if  i.id_gerente_regional == None and i.id_gerente_ciudad == None and i.id_jefe_venta == None:
                # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns([
                #     RegistrarGerente.c.nombre_gerente,
                # ])
                # data_gerente = db.execute(query_gerente).fetchone()
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
                # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns([
                #     RegistrarGerente.c.nombre_gerente,
                # ])
                # data_gerente = db.execute(query_gerente).fetchone()
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
                    RegistrarGerenteRegional.c.nombre_gerente_regional,
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
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": data_gerente_regional.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente_regional,
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
                    RegistrarGerenteRegional.c.nombre_gerente_regional,
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
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": data_gerente_regional.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente_regional,
                    "id_gerente_ciudad": data_gerente_ciudad.id_gerente_ciudad,
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
                # query_gerente = RegistrarGerente.select().where(RegistrarGerente.c.id_gerente == i.id_gerente).with_only_columns([
                #     RegistrarGerente.c.nombre_gerente,
                # ])
                # data_gerente = db.execute(query_gerente).fetchone()
                query_gerente_regional = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == i.id_gerente_regional).with_only_columns([
                    RegistrarGerenteRegional.c.nombre_gerente_regional,
                ])
                data_gerente_regional = db.execute(query_gerente_regional).fetchone()
                query_gerente_ciudad = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == i.id_gerente_ciudad).with_only_columns([
                    RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
                ])
                data_gerente_ciudad = db.execute(query_gerente_ciudad).fetchone()
                query_jefe_venta = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == i.id_jefe_venta).with_only_columns([
                    RegistroJefeVentas.c.nombre_jefe_venta,
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
                    # "id_gerente": data_gerente.id_gerente,
                    # "nombre_gerente": data_gerente.nombre_gerente,
                    "id_gerente_regional": data_gerente_regional.id_gerente_regional,
                    "nombre_gerente_regional": data_gerente_regional.nombre_gerente,
                    "id_gerente_ciudad": data_gerente_ciudad.id_gerente_ciudad,
                    "nombre_gerente_ciudad": data_gerente_ciudad.nombre_gerente_ciudad,
                    "id_jefe_venta": data_jefe_venta.id_jefe_venta,
                    "nombre_jefe_venta": data_jefe_venta.nombre_jefe_venta,
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

        return dataInfo
    except Exception as e:
        return {"error": str(e)}
    
async def get_tdd_excel_workbook(): 
    wb = Workbook() 
    ws = wb.active 
    data = await get_infoReporte()

    ws.append([
        "CIUDAD","ESTADO","COD. VENDEDOR","VENDEDOR","LIDER DE PELOTON","JEFE DE VENTAS","GERENTE","CANAL DE VENTA","OPERADOR","SISTEMA OPERATIVO","GENERO","MODALIDAD","FECHA INGRESO","FECHA SALIDA","SECTOR RESIDENCIA","EMAIL","DIAS INACTIVO","CELULAR","META VOLUMEN","META DOLARES","USUARIO EQUIFAX","CEDULA"
    ])
    for i in data:
        k = ReporteExcel(**i)
        # print(k)
        ws.append([
            k.ciudad, k.estado, k.codigo_vendedor, k.nombre_vendedor, k.lider_check, k.nombre_jefe_venta, k.nombre_gerente_ciudad, k.channel, k.operador, k.sistema_operativo, k.genero, k.modalidad, k.fecha_ingreso, k.fecha_salida, k.sector_residencia, k.email, k.dias_inactivo, k.telefono, k.meta_volumen, k.meta_dolares, k.usuario_equifax, k.cedula
        ])
    wb.save("reporte_tdd.xlsx")

    